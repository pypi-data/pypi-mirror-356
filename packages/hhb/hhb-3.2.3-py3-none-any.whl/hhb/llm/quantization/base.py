import os
import logging
import gc
import json
import inspect
import functools
import torch
import torch.nn as nn
from collections import defaultdict
from tqdm import tqdm
from typing import List, Union, Dict, Optional
from safetensors.torch import save_file
from typing_extensions import Doc, Annotated
from huggingface_hub import snapshot_download
from transformers.modeling_utils import shard_checkpoint
from transformers import (
    PreTrainedModel,
    PretrainedConfig,
    AutoProcessor,
    CLIPImageProcessor,
    PreTrainedTokenizer,
)
from accelerate.big_modeling import (
    init_empty_weights,
    load_checkpoint_and_dispatch,
)

from awq.modules.linear import (
    WQLinear_GEMM,
    WQLinear_GEMV,
    WQLinear_Marlin,
    WQLinear_Exllama,
    WQLinear_ExllamaV2,
    WQLinear_GEMVFast,
    marlin_post_init,
    exllama_post_init,
    exllamav2_post_init,
)
from awq.utils.module import (
    get_named_linears,
    set_op_by_name,
    exclude_layers_to_not_quantize,
    append_str_prefix,
    get_op_name,
)

from awq.models._config import AwqConfig
from awq.modules.act import ScaledActivation
from awq.utils.module import get_named_linears, set_op_by_name
from awq.utils.calib_data import get_calib_dataset
from awq.quantize.scale import apply_scale, apply_clip
from awq.utils.utils import clear_memory, get_best_device
from .hhb_gemm import HHB_WQLinear_GEMM


class HHBAwqQuantizer:
    def __init__(
        self,
        awq_model,
        model,
        tokenizer,
        w_bit,
        group_size,
        zero_point,
        version,
        calib_data,
        split,
        text_column,
        duo_scaling,
        modules_to_not_convert=None,
        export_compatible=False,
        apply_clip=True,
    ) -> None:
        self.awq_model = awq_model
        self.model = model
        self.tokenizer = tokenizer
        self.w_bit = w_bit
        self.group_size = group_size
        self.zero_point = zero_point
        self.version = version
        self.calib_data = calib_data
        self.split = split
        self.text_column = text_column
        self.duo_scaling = duo_scaling
        self.export_compatible = export_compatible
        self.apply_clip = apply_clip
        self.modules_to_not_convert = (
            modules_to_not_convert if modules_to_not_convert is not None else []
        )
        self.modules, self.module_kwargs, self.inps = self.init_quant()

    def pseudo_quantize_tensor(self, w: torch.Tensor):
        org_w_shape = w.shape
        if self.group_size > 0:
            assert org_w_shape[-1] % self.group_size == 0
            w = w.reshape(-1, self.group_size)
        assert w.dim() == 2
        assert torch.isnan(w).sum() == 0

        # zero point quantization
        if self.zero_point:
            max_val = w.amax(dim=1, keepdim=True)
            min_val = w.amin(dim=1, keepdim=True)
            max_int = 2**self.w_bit - 1
            min_int = 0
            scales = (max_val - min_val).clamp(min=1e-5) / max_int
            zeros = (-torch.round(min_val / scales)).clamp_(min_int, max_int)
            w = (torch.clamp(torch.round(w / scales) + zeros, min_int, max_int) - zeros) * scales
            zeros = zeros.view(org_w_shape[0], -1)
        else:
            max_val = w.abs().amax(dim=1, keepdim=True)
            max_val = max_val.clamp(min=1e-5)
            max_int = 2 ** (self.w_bit - 1) - 1
            min_int = -(2 ** (self.w_bit - 1))
            scales = max_val / max_int
            zeros = None
            w = torch.clamp(torch.round(w / scales), min_int, max_int) * scales

        assert torch.isnan(scales).sum() == 0
        assert torch.isnan(w).sum() == 0

        scales = scales.view(org_w_shape[0], -1)
        w = w.reshape(org_w_shape)

        return w, scales, zeros

    def pseudo_dequantize_tensor(
        self, w: nn.Linear, scales: torch.Tensor, zeros: Optional[torch.Tensor] = None
    ):
        # get repeated count
        repeat_count = w.weight.data.shape[-1] // scales.shape[-1]
        scales = scales.repeat(1, repeat_count).reshape(w.weight.data.shape)

        # dequantize
        if self.zero_point:
            zeros = zeros.repeat(1, repeat_count).reshape(w.weight.data.shape)
            w = (w.weight.data - zeros) * scales
        else:
            w = w.weight.data * scales

        return w

    def quantize(self):
        for i in tqdm(range(len(self.modules)), desc=f"HHB_AWQ[{self.awq_model.model_type}]"):
            # Move module and inputs to correct device
            common_device = next(self.modules[i].parameters()).device
            if common_device is None or str(common_device) == "cpu":
                if torch.cuda.is_available():
                    best_device = "cuda:" + str(i % torch.cuda.device_count())
                else:
                    best_device = get_best_device()

                self.modules[i] = self.modules[i].to(best_device)
                common_device = next(self.modules[i].parameters()).device

            if self.module_kwargs.get("position_ids") is not None:
                self.module_kwargs["position_ids"] = self.module_kwargs["position_ids"].to(
                    common_device
                )

            if self.module_kwargs.get("attention_mask") is not None:
                self.module_kwargs["attention_mask"] = self.module_kwargs["attention_mask"].to(
                    common_device
                )

            self.inps = self.inps.to(common_device)

            # [STEP 1]: Get layer, extract linear modules, extract input features
            named_linears = get_named_linears(self.modules[i])

            # Filter out the linear layers we don't want to exclude
            named_linears = exclude_layers_to_not_quantize(
                named_linears, self.modules_to_not_convert
            )

            input_feat = self._get_input_feat(self.modules[i], named_linears)
            clear_memory()

            # [STEP 2]: Compute and apply scale list
            module_config: List[Dict] = self.awq_model.get_layers_for_scaling(
                self.modules[i], input_feat, self.module_kwargs
            )
            # scales_list = [
            #     self._search_best_scale(self.modules[i], **layer) for layer in module_config
            # ]
            scales_list = []
            for layer in module_config:
                tt = self._search_best_scale(self.modules[i], **layer)
                scales_list.append(tt)
            apply_scale(self.modules[i], scales_list, input_feat_dict=input_feat)
            scales_list = append_str_prefix(
                scales_list, get_op_name(self.model, self.modules[i]) + "."
            )

            # [STEP 3]: Compute and apply clipping list
            if self.apply_clip:
                clip_list = self._search_best_clip(self.modules[i], named_linears, input_feat)
                apply_clip(self.modules[i], clip_list)
                clip_list = append_str_prefix(
                    clip_list, get_op_name(self.model, self.modules[i]) + "."
                )

            # [STEP 4]: Quantize weights
            if not self.export_compatible:
                self._apply_quant(self.modules[i], named_linears)

            clear_memory()

    def pack(self):
        for i in tqdm(range(len(self.modules)), desc="Packing"):
            named_linears = get_named_linears(self.modules[i])
            named_linears = exclude_layers_to_not_quantize(
                named_linears, self.modules_to_not_convert
            )
            self._apply_quant(self.modules[i], named_linears)
            clear_memory()

    def _apply_quant(self, module, named_linears: Dict[str, nn.Linear]):
        for name, linear_layer in named_linears.items():
            # NOTE: small regression in perplexity if linear layer uses .cpu().float()
            linear_layer = linear_layer.to(get_best_device()).half()

            linear_layer.weight.data, scales, zeros = self.pseudo_quantize_tensor(
                linear_layer.weight.data
            )
            self.version = "hhb"

            if self.version == "gemm":
                scales = scales.t().contiguous()
                zeros = zeros.t().contiguous()
                q_linear_module = WQLinear_GEMM

            elif self.version == "gemv":
                q_linear_module = WQLinear_GEMV

            elif self.version == "marlin":
                q_linear_module = WQLinear_Marlin

            elif self.version == "gemv_fast":
                q_linear_module = WQLinear_GEMVFast

            elif self.version == "hhb":
                scales = scales.t().contiguous()
                zeros = zeros.t().contiguous()
                q_linear_module = HHB_WQLinear_GEMM

            else:
                raise ValueError(f"Unknown version {self.version}")

            q_linear = q_linear_module.from_linear(
                linear=linear_layer,
                w_bit=self.w_bit,
                group_size=self.group_size,
                init_only=False,
                scales=scales,
                zeros=zeros,
            )

            linear_layer.cpu()
            q_linear.to(next(module.parameters()).device)
            set_op_by_name(module, name, q_linear)
            clear_memory()

    @torch.no_grad()
    def _search_best_scale(
        self,
        module,
        prev_op,
        layers: List[nn.Linear],
        inp: torch.Tensor,
        module2inspect=None,
        kwargs={},
    ):
        if module2inspect is None:
            assert len(layers) == 1
            module2inspect = layers[0]

        if "use_cache" in kwargs:
            kwargs.pop("use_cache")

        # Put x on the right device
        inp = inp.to(next(module2inspect.parameters()).device)

        # [STEP 1]: Compute per-channel mean of normalised weights
        # All layer weights are concatted together
        weight = torch.cat([_m.weight for _m in layers], dim=0)
        org_shape = weight.shape
        # The weights are reshaped to be organised by quantization group
        weight = weight.view(-1, self.group_size)
        # Calculates the relative magnitude of the weights within each of the quantization groups,
        # and rescales each group individually so that each group has weights on a 0-1 scale.
        w_scale = weight.abs() / weight.abs().amax(dim=1, keepdim=True)
        # Resizes the rescaled weight matrix back up to its original dimensions
        w_scale = w_scale.view(org_shape)
        # Gets the average rescaled magnitude for each output channel
        w_mean = w_scale.mean(0)
        clear_memory(weight)

        # [STEP 2]: Compute per-channel mean of the input activation
        x_mean = inp.abs().view(-1, inp.shape[-1]).mean(0)

        # [STEP 3]: Compute output of module
        with torch.no_grad():
            module_kwargs = self._sanitize_kwargs(kwargs, module2inspect)
            fp16_output = module2inspect(inp, **module_kwargs)
            if isinstance(fp16_output, tuple):
                fp16_output = fp16_output[0]

        # [STEP 4]: Compute loss
        best_scales = self._compute_best_scale(
            inp, w_mean, x_mean, module2inspect, layers, fp16_output, module_kwargs
        )

        return (
            get_op_name(module, prev_op),
            tuple([get_op_name(module, m) for m in layers]),
            best_scales,
        )

    def _compute_best_scale(
        self,
        x,
        w_mean,
        x_mean,
        module2inspect,
        linears2scale: List[nn.Linear],
        fp16_output,
        kwargs={},
    ):
        """
        Compute loss and select best scales

        L(s) = || Q(W * s) (s^-1 * X) - W * X ||
        Q: weight quantization function | pseudo_quantize_tensor(W * s)
        X: inputs from calib dataset    | X
        W: original weights in FP16     | layer
        s: per channel scaling factor   | s^-1 * X
        """
        n_grid = 20
        history = []
        best_ratio = -1
        best_scales = None
        best_error = float("inf")

        org_sd = {k: v.cpu() for k, v in module2inspect.state_dict().items()}

        device = x.device
        x_mean = x_mean.view(-1).to(device)
        w_mean = w_mean.view(-1).to(device)

        for ratio in range(n_grid):
            # create new scales
            ratio = ratio / n_grid

            # NOTE: s^-1 * x is fused here, according to paper
            if self.duo_scaling:
                scales = (x_mean.pow(ratio) / w_mean.pow(1 - ratio)).clamp(min=1e-4)
            else:
                scales = x_mean.pow(ratio).clamp(min=1e-4).view(-1)
            scales = scales / (scales.max() * scales.min()).sqrt()
            scales_view = scales.view(1, -1).to(device)

            # Q(W * s)
            for fc in linears2scale:
                fc.weight.mul_(scales_view)
                fc.weight.data = self.pseudo_quantize_tensor(fc.weight.data)[0] / scales_view

            # W * X
            int_w_output = module2inspect(x, **kwargs)
            if isinstance(int_w_output, tuple):
                int_w_output = int_w_output[0]

            # compute mean squared error (L2 norm)
            loss = (
                (fp16_output - int_w_output).float().pow(2).mean().item()
            )  # NOTE: float prevents overflow

            history.append(loss)
            if loss < best_error:
                best_error = loss
                best_ratio = ratio
                best_scales = scales.clone()
            module2inspect.load_state_dict(org_sd)

        if best_ratio == -1:
            logging.debug(history)
            raise Exception

        assert torch.isnan(best_scales).sum() == 0, best_scales

        return best_scales.detach().cpu()

    @torch.no_grad()
    def _search_best_clip(self, layer, named_linears, input_feat):
        clip_list = []
        avoid_clipping = ["q_", "k_", "query", "key", "Wqkv"]

        for name in named_linears:
            # due to qk bmm, it is hard to clip precisely
            if any([_ in name for _ in avoid_clipping]):
                continue

            named_linears[name].to(get_best_device())
            max_val = self._compute_best_clip(named_linears[name].weight, input_feat[name])
            clip_list.append((name, max_val))
            named_linears[name].cpu()

        return clip_list

    @torch.no_grad()
    def _compute_best_clip(
        self,
        w: torch.Tensor,
        input_feat: torch.Tensor,
        n_grid=20,
        max_shrink=0.5,
        n_sample_token=512,
    ):
        assert w.dim() == 2
        org_w_shape = w.shape
        # w           [co, ci]      -> [co, 1, n_group, group size]
        # input_feat  [n_token, ci] -> [1, n_token, n_group, group size]
        group_size = self.group_size if self.group_size > 0 else org_w_shape[1]
        input_feat = input_feat.view(-1, input_feat.shape[-1])
        input_feat = input_feat.reshape(1, input_feat.shape[0], -1, group_size)
        input_feat = input_feat[:, 0 :: input_feat.shape[1] // n_sample_token]
        w = w.reshape(org_w_shape[0], 1, -1, group_size)

        oc_batch_size = 256 if org_w_shape[0] % 256 == 0 else 64  # prevent OOM
        assert org_w_shape[0] % oc_batch_size == 0
        w_all = w
        best_max_val_all = []

        for i_b in range(org_w_shape[0] // oc_batch_size):
            w = w_all[i_b * oc_batch_size : (i_b + 1) * oc_batch_size]

            org_max_val = w.abs().amax(dim=-1, keepdim=True)  # co, 1, n_group, 1

            best_max_val = org_max_val.clone()
            min_errs = torch.ones_like(org_max_val) * 1e9
            input_feat = input_feat.to(w.device)
            org_out = (input_feat * w).sum(dim=-1)  # co, n_token, n_group

            for i_s in range(int(max_shrink * n_grid)):
                max_val = org_max_val * (1 - i_s / n_grid)
                min_val = -max_val
                cur_w = torch.clamp(w, min_val, max_val)
                q_w = self.pseudo_quantize_tensor(cur_w)[0]
                cur_out = (input_feat * q_w).sum(dim=-1)

                # co, 1, n_group, 1
                err = (cur_out - org_out).pow(2).mean(dim=1).view(min_errs.shape)
                del cur_w
                del cur_out
                cur_best_idx = err < min_errs
                min_errs[cur_best_idx] = err[cur_best_idx]
                best_max_val[cur_best_idx] = max_val[cur_best_idx]
            best_max_val_all.append(best_max_val)

        best_max_val = torch.cat(best_max_val_all, dim=0)

        clear_memory(input_feat)
        clear_memory(org_out)

        return best_max_val.squeeze(1)

    def init_quant(self, n_samples=128, seqlen=512):
        modules = self.awq_model.get_model_layers(self.model)
        samples = get_calib_dataset(
            data=self.calib_data,
            tokenizer=self.tokenizer,
            n_samples=n_samples,
            block_size=seqlen,
            split=self.split,
            text_column=self.text_column,
        )
        samples = torch.cat(samples, dim=0)

        inps = []
        rotary_pos_emb_lt = []
        layer_kwargs = {}

        best_device = get_best_device()
        modules[0] = modules[0].to(best_device)
        self.awq_model.move_embed(self.model, best_device)

        # get input and kwargs to layer 0
        # with_kwargs is only supported in PyTorch 2.0
        # use this Catcher hack for now
        class Catcher(nn.Module):
            def __init__(self, module):
                super().__init__()
                self.module = module

            def forward(self, *args, **kwargs):
                # assume first input to forward is hidden states
                rotary_pos_emb = None
                if len(args) > 0:
                    hidden_states = args[0]
                    if len(args) > 2:
                        rotary_pos_emb = args[2]
                    del args
                else:
                    first_key = list(kwargs.keys())[0]
                    hidden_states = kwargs.pop(first_key)

                inps.append(hidden_states)
                rotary_pos_emb_lt.append(rotary_pos_emb)
                layer_kwargs.update(kwargs)
                raise ValueError  # early exit to break later inference

        # patch layer 0 to catch input and kwargs
        modules[0] = Catcher(modules[0])
        try:
            self.model(samples.to(next(self.model.parameters()).device))
        except ValueError:  # work with early exit
            pass
        modules[0] = modules[0].module  # restore

        # Update the layer kwargs with `prepare_inputs_for_generation` method
        # that takes care of everything to avoid unexpected errors.
        layer_kwargs = self.model.prepare_inputs_for_generation(samples, **layer_kwargs)
        # Pop the input_ids as they are not needed at all.
        layer_kwargs.pop("input_ids")

        del samples
        inps = inps[0]

        modules[0] = modules[0].cpu()
        self.awq_model.move_embed(self.model, "cpu")

        clear_memory()

        if layer_kwargs.get("attention_mask") is not None:
            layer_kwargs["attention_mask"] = layer_kwargs["attention_mask"].to(best_device)
        if self.awq_model.model_type == "chatglm":
            layer_kwargs["rotary_pos_emb"] = rotary_pos_emb_lt[0]
        return modules, layer_kwargs, inps

    def _get_input_feat(self, layer, named_linears):
        # firstly, get input features of all linear layers
        def cache_input_hook(m, x, y, name, feat_dict):
            x = x[0]
            x = x.detach().cpu()
            feat_dict[name].append(x)

        input_feat = defaultdict(list)
        handles = []

        # FIXME: Workaround for Mixtral to use block_sparse_moe input features
        if self.awq_model.model_type == "mixtral":
            named_linears = {
                **named_linears,
                "block_sparse_moe": layer.block_sparse_moe,
            }

        for name in named_linears:
            handles.append(
                named_linears[name].register_forward_hook(
                    functools.partial(cache_input_hook, name=name, feat_dict=input_feat)
                )
            )
        self.inps = self.inps.to(next(layer.parameters()).device)  # in case multi-gpu
        # get output as next layer's input

        # Sanitize the kwargs in case we use transformers version that contains
        # kwargs that are not handled by the module.
        # Useful for trust_remote_code models.
        module_kwargs = self._sanitize_kwargs(self.module_kwargs, layer)
        self.inps = layer(self.inps, **module_kwargs)[0]
        for h in handles:
            h.remove()
        # now solve for scaling and clipping
        input_feat = {k: torch.cat(v, dim=0) for k, v in input_feat.items()}

        return input_feat

    def _sanitize_kwargs(self, inputs_kwargs, module):
        """
        Remove the arguments that are not supported in the module's
        forward pass to avoid breaking behaviour between different versions
        of transformers.

        Args:
            inputs_kwargs (`dict`):
                The input dictionary to pass to the model layer
            module (`torch.nn.Module`):
                Target module to quantize.
        """
        module_signature = inspect.signature(module.forward).parameters
        sanitized_kwargs = {}
        for k, v in inputs_kwargs.items():
            if k in module_signature:
                sanitized_kwargs[k] = v
        return sanitized_kwargs


class HHBBaseAWQForCausalLM(nn.Module):
    def __init__(
        self,
        model: Annotated[PreTrainedModel, Doc("The pretrained or quantized model.")],
        model_type: Annotated[str, Doc("The model type, found in config.json.")],
        is_quantized: Annotated[bool, Doc("Indicates if the current model is quantized.")],
        config: Annotated[PretrainedConfig, Doc("The config of the model.")],
        quant_config: Annotated[AwqConfig, Doc("The quantization config of the model.")],
        processor: Annotated[AutoProcessor, Doc("An optional processor, e.g. for vision models.")],
    ):
        """The base model for all AutoAWQ models."""
        super().__init__()
        self.model: PreTrainedModel = model
        self.model_type: str = model_type
        self.is_quantized: bool = is_quantized
        self.search_result = None
        self.config: PretrainedConfig = config
        self.quant_config: AwqConfig = quant_config
        self.processor: CLIPImageProcessor = processor

    def to(self, device: Annotated[str, Doc("The device to move your model to.")]):
        """A utility function for moving the model to a device."""
        return self.model.to(device)

    def forward(self, *args, **kwargs):
        """A forward function that mimics the torch forward."""
        return self.model(*args, **kwargs)

    def generate(self, *args, **kwargs):
        """A generate function that mimics the HF generate function."""
        with torch.inference_mode():
            return self.model.generate(*args, **kwargs)

    @torch.no_grad()
    def quantize(
        self,
        tokenizer: Annotated[
            PreTrainedTokenizer, Doc("The tokenizer to use for quantization.")
        ] = None,
        quant_config: Annotated[Dict, Doc("The quantization config you want to use.")] = {},
        calib_data: Annotated[
            Union[str, List[str]],
            Doc(
                "The calibration dataset. Either a string pointing to Huggingface or a list of preloaded examples."
            ),
        ] = "pileval",
        split: Annotated[str, Doc("The split of calib_data.")] = "train",
        text_column: Annotated[str, Doc("The text column of calib_data.")] = "text",
        duo_scaling: Annotated[bool, Doc("Whether to scale using both w/x or just x.")] = True,
        export_compatible: Annotated[
            bool,
            Doc(
                "This argument avoids real quantization by only applying the scales without quantizing down to FP16."
            ),
        ] = False,
        apply_clip: Annotated[
            bool,
            Doc(
                "Whether to apply clipping to the model during quantization. Some models may perform better with this set to False."
            ),
        ] = True,
    ):
        """
        The main quantization function that you can use to quantize your model.

        Example:

        ```python
        from awq import AutoAWQForCausalLM
        from transformers import AutoTokenizer

        model_path = "..."
        model = AutoAWQForCausalLM.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained(model_path)

        quant_config = { "zero_point": True, "q_group_size": 128, "w_bit": 4, "version": "GEMM" }
        model.quantize(tokenizer, quant_config)
        ```
        """
        self.quant_config: AwqConfig = AwqConfig.from_dict(quant_config)

        if hasattr(self, "modules_to_not_convert"):
            self.quant_config.modules_to_not_convert = self.modules_to_not_convert

        self.quantizer = HHBAwqQuantizer(
            self,
            self.model,
            tokenizer,
            self.quant_config.w_bit,
            self.quant_config.q_group_size,
            self.quant_config.zero_point,
            self.quant_config.version,
            calib_data,
            split,
            text_column,
            duo_scaling,
            modules_to_not_convert=self.quant_config.modules_to_not_convert,
            export_compatible=export_compatible,
            apply_clip=apply_clip,
        )
        self.quantizer.quantize()

        self.is_quantized = True

    @torch.no_grad()
    def pack(self):
        """
        A utility function for the following scenario. Note that save_quantized will
        overwrite existing weights if you use the same quant_path.

        Example:

        ```python
        model.quantize(
            tokenizer,
            quant_config=quant_config,
            export_compatible=True
        )
        model.save_quantized(...)  # produces GGUF/other compat weights
        model.pack(...) # makes the model CUDA compat
        model.save_quantized(...)  # produces CUDA compat weights
        ```
        """
        self.quantizer.pack()

    @staticmethod
    def fuse_layers(model):
        pass

    def save_quantized(
        self,
        save_dir: Annotated[str, Doc("The directory to save your model to.")],
        safetensors: Annotated[
            bool, Doc("Whether to save the model as safetensors or torch files.")
        ] = True,
        shard_size: Annotated[
            str, Doc("The shard size for sharding large models into multiple chunks.")
        ] = "5GB",
    ):
        save_dir = save_dir[:-1] if save_dir[-1] == "/" else save_dir

        # Save model
        class EmptyModule(nn.Module):
            def __init__(self):
                super(EmptyModule, self).__init__()

            def forward(self, x):
                return x

        # Save model and config files with empty state dict
        self.model.config.quantization_config = self.quant_config.to_transformers_dict()
        self.model.generation_config.do_sample = True
        self.model.save_pretrained(save_dir, state_dict=EmptyModule().state_dict())

        # Vision transformers have a processor
        if self.processor is not None:
            self.processor.save_pretrained(save_dir)

        # Remove empty state dict
        default_paths = [
            f"{save_dir}/model.safetensors",
            f"{save_dir}/pytorch_model.bin",
        ]
        for path in default_paths:
            if os.path.exists(path):
                os.remove(path)

        # model_name has no extension, add it when saving state_dict
        model_name = "model.safetensors" if safetensors else "pytorch_model.bin"

        # shard checkpoint into chunks (10GB default)
        shards, index = shard_checkpoint(
            self.model.state_dict(), max_shard_size=shard_size, weights_name=model_name
        )

        for shard_file, shard in shards.items():
            if safetensors:
                # safetensors must be in the same memory, so we duplicate and use contiguous memory
                shard = {k: v.clone().contiguous() for k, v in shard.items()}
                save_file(shard, os.path.join(save_dir, shard_file), metadata={"format": "pt"})
            else:
                torch.save(shard, os.path.join(save_dir, shard_file))

        # save shard index
        if index is not None:
            with open(f"{save_dir}/{model_name}.index.json", "w+") as file:
                file.write(json.dumps(index, indent=4))

    @classmethod
    def from_pretrained(
        self,
        model_path: Annotated[str, Doc("A Huggingface path or local path to a model.")],
        model_type: Annotated[str, Doc("The model type, loaded from config.json.")],
        torch_dtype: Annotated[
            torch.dtype,
            Doc("The dtype to load the model as. May not work with other values than float16."),
        ] = torch.float16,
        trust_remote_code: Annotated[
            bool,
            Doc(
                "Useful for Huggingface repositories that have not been integrated into transformers yet."
            ),
        ] = True,
        safetensors: Annotated[
            bool, Doc("Whether to download/load safetensors instead of torch weights.")
        ] = True,
        device_map: Annotated[
            Union[str, Dict],
            Doc(
                "A device map that will be passed onto the model loading method from transformers."
            ),
        ] = None,
        download_kwargs: Annotated[
            Dict,
            Doc("Used for configure download model"),
        ] = None,
        **model_init_kwargs: Annotated[
            Dict,
            Doc("Additional kwargs that are passed to the model during initialization."),
        ],
    ):
        """A method for initialization of pretrained models, usually in FP16."""
        # Get weights path and quant config
        model_weights_path, config, quant_config = self._load_config(
            self,
            model_path,
            "",
            safetensors,
            trust_remote_code=trust_remote_code,
            download_kwargs=download_kwargs,
        )

        target_cls_name, target_cls = self._get_target_cls(self, config.model_type)
        processor = None
        if target_cls_name == "AutoModelForVision2Seq":
            processor = AutoProcessor.from_pretrained(model_weights_path)
            processor: CLIPImageProcessor = processor.image_processor

        # If not quantized, must load with AutoModelForCausalLM
        model = target_cls.from_pretrained(
            model_weights_path,
            trust_remote_code=trust_remote_code,
            torch_dtype=torch_dtype,
            use_safetensors=safetensors,
            device_map=device_map,
            **model_init_kwargs,
        )

        model.eval()

        return self(
            model,
            model_type,
            is_quantized=False,
            config=config,
            quant_config=quant_config,
            processor=processor,
        )

    @classmethod
    def from_quantized(
        self,
        model_path: Annotated[str, Doc("A Huggingface path or local path to a model.")],
        model_type: Annotated[str, Doc("The model type, loaded from config.json.")],
        model_filename: Annotated[
            str, Doc("Load a specific model's filename by specifying this argument.")
        ] = "",
        max_seq_len: Annotated[
            int,
            Doc(
                "The maximum sequence cached sequence length of the model. Larger values may increase loading time and memory usage."
            ),
        ] = None,
        torch_dtype: Annotated[
            torch.dtype,
            Doc("The dtype to load the model as. May not work with other values than float16."),
        ] = torch.float16,
        trust_remote_code: Annotated[
            bool,
            Doc(
                "Useful for Huggingface repositories that have not been integrated into transformers yet."
            ),
        ] = True,
        safetensors: Annotated[
            bool, Doc("Whether to download/load safetensors instead of torch weights.")
        ] = True,
        fuse_layers: Annotated[
            bool,
            Doc("Whether to use fused/optimized combination of layers for increased speed."),
        ] = True,
        use_exllama: Annotated[
            bool, Doc("Whether to map the weights to ExLlamaV1 kernels.")
        ] = False,
        use_exllama_v2: Annotated[
            bool, Doc("Whether to map the weights to ExLlamaV2 kernels.")
        ] = False,
        device_map: Annotated[
            Union[str, Dict],
            Doc(
                "A device map that will be passed onto the model loading method from transformers."
            ),
        ] = "balanced",
        max_memory: Annotated[
            Dict[Union[int, str], Union[int, str]],
            Doc(
                'A dictionary device identifier to maximum memory which will be passed onto the model loading method from transformers. For example：{0: "4GB",1: "10GB"'
            ),
        ] = None,
        offload_folder: Annotated[
            str,
            Doc("The folder ot offload the model to."),
        ] = None,
        download_kwargs: Annotated[
            Dict,
            Doc("Used for configure download model"),
        ] = None,
        **config_kwargs: Annotated[
            Dict,
            Doc("Additional kwargs that are passed to the config during initialization."),
        ],
    ):
        """A method for initialization of a quantized model, usually in INT4."""
        # [STEP 1-2] Load weights path and configs
        model_weights_path, config, quant_config = self._load_config(
            self,
            model_path,
            model_filename,
            safetensors,
            trust_remote_code,
            max_seq_len=max_seq_len,
            download_kwargs=download_kwargs,
            **config_kwargs,
        )

        target_cls_name, target_cls = self._get_target_cls(self, config.model_type)

        # [STEP 3] Load model
        with init_empty_weights():
            model = target_cls.from_config(
                config=config,
                torch_dtype=torch_dtype,
                trust_remote_code=trust_remote_code,
            )

        # Prepare WQLinear layers, replace nn.Linear
        self._load_quantized_modules(
            self,
            model,
            quant_config,
            quant_config.version,
            use_exllama=use_exllama,
            use_exllama_v2=use_exllama_v2,
        )

        model.tie_weights()

        # loads the weights into modules and distributes
        # across available devices automatically
        load_checkpoint_and_dispatch(
            model,
            checkpoint=model_weights_path,
            device_map=device_map,
            max_memory=max_memory,
            no_split_module_classes=[self.layer_type],
            offload_folder=offload_folder,
            dtype=torch_dtype,
        )

        # Dispath to devices
        if fuse_layers:
            self.fuse_layers(model)

        if quant_config.version == "marlin":
            model = marlin_post_init(model)

        elif use_exllama:
            # creates q4 handle
            model = exllama_post_init(model)
        elif use_exllama_v2:
            # creates q4 handle and allocates scratch spaces wrt max_input_len and max_batch_size
            model = exllamav2_post_init(
                model,
                max_input_len=max_seq_len or 2048,
                max_batch_size=int(os.getenv("AWQ_BATCH_SIZE", 1)),
            )

        return self(
            model,
            model_type,
            is_quantized=True,
            config=config,
            quant_config=quant_config,
            processor=None,
        )

    def _load_config(
        self,
        model_path,
        model_filename,
        safetensors=True,
        trust_remote_code=True,
        max_seq_len=4096,
        download_kwargs=None,
        **config_kwargs,
    ):
        from transformers import AutoConfig

        # [STEP 1] Download model if path is not a directory
        if not os.path.isdir(model_path):
            ignore_patterns = ["*msgpack*", "*h5*", "optimizer.pt"]
            if safetensors:
                ignore_patterns.extend(["*.pt*", "*.bin*", "consolidated*"])
            else:
                ignore_patterns.append("*.safetensors*")

            if download_kwargs is None:
                download_kwargs = {}

            if "ignore_patterns" in download_kwargs:
                download_kwargs_ignore_patterns = download_kwargs.pop("ignore_patterns")

                if isinstance(download_kwargs_ignore_patterns, str):
                    ignore_patterns.append(download_kwargs_ignore_patterns)
                elif isinstance(download_kwargs_ignore_patterns, list):
                    ignore_patterns.extend(download_kwargs_ignore_patterns)

            model_path = snapshot_download(
                model_path, ignore_patterns=ignore_patterns, **download_kwargs
            )

        if model_filename != "":
            model_weights_path = model_path + f"/{model_filename}"
        else:
            model_weights_path = model_path

        # [STEP 2] Load config and set sequence length
        # TODO: Create BaseAWQConfig class
        quant_config = AwqConfig.from_pretrained(model_path)

        # Load model config and set max generation length
        if max_seq_len is None and hasattr(self, "max_seq_len_key"):
            config = AutoConfig.from_pretrained(
                model_path, trust_remote_code=trust_remote_code, **config_kwargs
            )
            config.max_seq_len = getattr(config, self.max_seq_len_key, 2048)
            # To add the generate support for Multi-modal models as well
            if hasattr(config, "text_config"):
                config.text_config.max_seq_len = getattr(config, self.max_seq_len_key, 2048)
        else:
            max_seq_len = 2048 if max_seq_len is None else max_seq_len
            config = AutoConfig.from_pretrained(
                model_path, trust_remote_code=trust_remote_code, **config_kwargs
            )
            config.max_seq_len = max_seq_len

        return model_weights_path, config, quant_config

    def _load_quantized_modules(self, model, quant_config, version, use_exllama, use_exllama_v2):
        # Real quantization of weights
        assert not (
            version == "gemv" and (use_exllama or use_exllama_v2)
        ), "Exllama kernels only support GEMM version."

        # Get blocks of model
        layers = self.get_model_layers(model)

        for i in tqdm(range(len(layers)), desc="Replacing layers..."):
            layer = layers[i]

            # Get every linear layer in a block
            named_linears = get_named_linears(layer)

            # Filter out the linear layers we don't want to exclude
            named_linears = exclude_layers_to_not_quantize(
                named_linears, quant_config.modules_to_not_convert
            )

            # Replace activation functions
            self._scale_activations(self, layer)

            # Replace nn.Linear with WQLinear
            for name, module in named_linears.items():
                if version == "marlin":
                    q_linear_module = WQLinear_Marlin
                elif use_exllama:
                    q_linear_module = WQLinear_Exllama
                elif use_exllama_v2:
                    q_linear_module = WQLinear_ExllamaV2
                elif version == "gemm":
                    q_linear_module = WQLinear_GEMM
                elif version == "gemv":
                    q_linear_module = WQLinear_GEMV
                elif version == "gemv_fast":
                    q_linear_module = WQLinear_GEMVFast
                elif version == "hhb":
                    q_linear_module = HHB_WQLinear_GEMM

                q_linear = q_linear_module.from_linear(
                    module, quant_config.w_bit, quant_config.q_group_size, True
                )
                q_linear.to(next(layer.parameters()).device)
                set_op_by_name(layer, name, q_linear)

            torch.cuda.empty_cache()
            gc.collect()

    @staticmethod
    def _scale_activations(self, layer):
        scale_dict = self.get_act_for_scaling(layer)

        if scale_dict["is_scalable"]:
            if not isinstance(scale_dict["scale_layer"], ScaledActivation):
                param = next(layer.parameters())

                # get activation scale
                scale_like = torch.ones(
                    scale_dict["scale_shape"], dtype=param.dtype, device=param.device
                )

                # scale activation
                scaled_act = ScaledActivation(scale_dict["scale_layer"], scale_like)
                set_op_by_name(layer, scale_dict["scale_name"], scaled_act)

    def _get_target_cls(self, model_type):
        import transformers

        TRANSFORMERS_AUTO_MAPPING_DICT = {
            "mpt": "AutoModelForCausalLM",
            "llama": "AutoModelForCausalLM",
            "opt": "AutoModelForCausalLM",
            "RefinedWeb": "AutoModelForCausalLM",
            "RefinedWebModel": "AutoModelForCausalLM",
            "falcon": "AutoModelForCausalLM",
            "bloom": "AutoModelForCausalLM",
            "gptj": "AutoModelForCausalLM",
            "gpt_bigcode": "AutoModelForCausalLM",
            "mistral": "AutoModelForCausalLM",
            "mixtral": "AutoModelForCausalLM",
            "gpt_neox": "AutoModelForCausalLM",
            "aquila": "AutoModelForCausalLM",
            "Yi": "AutoModelForCausalLM",
            "qwen": "AutoModelForCausalLM",
            "baichuan": "AutoModelForCausalLM",
            "llava": "AutoModelForVision2Seq",
            "qwen2": "AutoModelForCausalLM",
            "gemma": "AutoModelForCausalLM",
            "stablelm": "AutoModelForCausalLM",
            "starcoder2": "AutoModelForCausalLM",
            "chatglm": "AutoModelForCausalLM",
        }

        target_cls_name = TRANSFORMERS_AUTO_MAPPING_DICT[model_type]
        target_cls = getattr(transformers, target_cls_name)
        return target_cls_name, target_cls

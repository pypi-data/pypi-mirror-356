# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# pylint: disable=invalid-name, unused-argument, too-many-lines, import-outside-toplevel
# pylint: disable=no-else-return, inconsistent-return-statements, no-else-raise
"""
smoothquant for LLM.
"""
import os
import sys
import json
from pathlib import Path
import torch
import torch.nn as nn
import functools
from tqdm import tqdm
import logging
from ..llm_util import (
    csinn_mem_type_enum,
    DtypeToSHLDtype,
)

logger = logging.getLogger("HHB")
LOG = 25

from typing import Dict


def _get_local_smooth_policy():
    from transformers.models.opt.modeling_opt import OPTDecoderLayer
    from transformers.models.bloom.modeling_bloom import BloomBlock
    from transformers.models.llama.modeling_llama import LlamaDecoderLayer, LlamaRMSNorm
    from transformers.models.mistral.modeling_mistral import (
        MistralDecoderLayer,
        MistralRMSNorm,
    )
    from transformers.models.mixtral.modeling_mixtral import (
        MixtralDecoderLayer,
        MixtralRMSNorm,
    )
    from transformers.models.falcon.modeling_falcon import FalconDecoderLayer

    LOCAL_SMOOTH_POLICY: Dict[str, dict] = {
        "opt": {
            "decoder_name": OPTDecoderLayer,
            "norm_type": [nn.LayerNorm],
            "attn_norm": "self_attn_layer_norm",
            "qkv": ["self_attn.q_proj"],
            "qkv_input_scales": ".self_attn.q_proj",
            "ffn_ln": "final_layer_norm",
            "fcs": ["fc1"],
            "fcs_input_scales": ".fc1",
        },
        "bloom": {
            "decoder_name": BloomBlock,
            "norm_type": [nn.LayerNorm],
            "attn_norm": "input_layernorm",
            "qkv": ["self_attention.query_key_value"],
            "qkv_input_scales": ".self_attention.query_key_value",
            "ffn_ln": "post_attention_layernorm",
            "fcs": ["mlp.dense_h_to_4h"],
            "fcs_input_scales": ".mlp.dense_h_to_4h",
        },
        "falcon": {
            "decoder_name": FalconDecoderLayer,
            "norm_type": [nn.LayerNorm],
            "attn_norm": "input_layernorm",
            "qkv": ["self_attention.query_key_value"],
            "qkv_input_scales": ".self_attention.query_key_value",
            "ffn_ln": "post_attention_layernorm",
            "fcs": ["mlp.dense_h_to_4h"],
            "fcs_input_scales": ".mlp.dense_h_to_4h",
        },
        "llama": {
            "decoder_name": LlamaDecoderLayer,
            "norm_type": [LlamaRMSNorm],
            "attn_ln": "input_layernorm",
            "qkv": ["self_attn.q_proj", "self_attn.k_proj", "self_attn.v_proj"],
            "qkv_input_scales": ".self_attn.q_proj",
            "ffn_ln": "post_attention_layernorm",
            "fcs": ["mlp.gate_proj", "mlp.up_proj"],
            "fcs_input_scales": ".mlp.gate_proj",
        },
        "mistral": {
            "decoder_name": MistralDecoderLayer,
            "norm_type": [MistralRMSNorm],
            "attn_ln": "input_layernorm",
            "qkv": ["self_attn.q_proj", "self_attn.k_proj", "self_attn.v_proj"],
            "qkv_input_scales": ".self_attn.q_proj",
            "ffn_ln": "post_attention_layernorm",
            "fcs": ["mlp.gate_proj", "mlp.up_proj"],
            "fcs_input_scales": ".mlp.gate_proj",
        },
        "mixtral": {
            "decoder_name": MixtralDecoderLayer,
            "norm_type": [MixtralRMSNorm],
            "attn_ln": "input_layernorm",
            "qkv": ["self_attn.q_proj", "self_attn.k_proj", "self_attn.v_proj"],
            "qkv_input_scales": ".self_attn.q_proj",
            "ffn_ln": "post_attention_layernorm",
            "fcs": [
                "block_sparse_moe.gate",
                "block_sparse_moe.experts.w1",
                "block_sparse_moe.experts.w3",
            ],
            "fcs_input_scales": ".block_sparse_moe.gate",
        },
    }
    return LOCAL_SMOOTH_POLICY


def _get_remote_smooth_policy():
    REMOTE_SMOOTH_POLICY: Dict[str, dict] = {
        "qwen": {
            "decoder_name": "modeling_qwen.QWenBlock",
            "norm_type": ["modeling_qwen.RMSNorm"],
            "attn_ln": "ln_1",
            "qkv": ["attn.c_attn"],
            "qkv_input_scales": ".attn.c_attn",
            "ffn_ln": "ln_2",
            "fcs": ["mlp.w1", "mlp.w2"],
            "fcs_input_scales": ".mlp.w1",
        },
        "chatglm": {
            "decoder_name": "modeling_chatglm.GLMBlock",
            "norm_type": ["modeling_chatglm.RMSNorm", nn.LayerNorm],
            "attn_ln": "input_layernorm",
            "qkv": ["self_attention.query_key_value"],
            "qkv_input_scales": ".self_attention.query_key_value",
            "ffn_ln": "post_attention_layernorm",
            "fcs": ["mlp.dense_h_to_4h"],
            "fcs_input_scales": ".mlp.dense_h_to_4h",
        },
    }
    return REMOTE_SMOOTH_POLICY


@torch.no_grad()
def _smooth_ln_fcs(ln, fcs, act_scales, alpha=0.5):
    if not isinstance(fcs, list):
        fcs = [fcs]
    for fc in fcs:
        assert isinstance(fc, nn.Linear)
        assert ln.weight.numel() == fc.in_features == act_scales.numel()

    device, dtype = fcs[0].weight.device, fcs[0].weight.dtype
    act_scales = act_scales.to(device=device, dtype=dtype)
    weight_scales = torch.cat([fc.weight.abs().max(dim=0, keepdim=True)[0] for fc in fcs], dim=0)
    weight_scales = weight_scales.max(dim=0)[0].clamp(min=1e-5)

    scales = (
        (act_scales.pow(alpha) / weight_scales.pow(1 - alpha)).clamp(min=1e-5).to(device).to(dtype)
    )

    ln.weight.div_(scales)
    if hasattr(ln, "bias"):
        ln.bias.div_(scales)
    for fc in fcs:
        fc.weight.mul_(scales.view(1, -1))


def _detect_model_type(remote_dir):
    if not os.path.exists(remote_dir):
        raise ValueError(f"{remote_dir} does not exist.")
    config = Path(remote_dir + "/config.json")
    with open(config, "r", encoding="utf-8") as config_file:
        cfg = json.load(config_file)
        if "model_type" not in cfg and (
            "model_config" not in cfg or "model_type" not in cfg["model_config"]
        ):
            raise ValueError(
                f"'model_type' not found in: {config}. "
                f"Please explicitly specify `--model-type` instead."
            )
        model_type = cfg["model_type"] if "model_type" in cfg else cfg["model_config"]["model_type"]
        return model_type


def _norm_type_assert(norm_class, norms_lt, remote_dir=""):
    from transformers.dynamic_module_utils import get_class_from_dynamic_module

    for norm_type_name in norms_lt:
        if isinstance(norm_type_name, str):
            norm_type = get_class_from_dynamic_module(norm_type_name, remote_dir)
            if str(type(norm_class)) == str(norm_type):
                return True
        else:
            if isinstance(norm_class, norm_type_name):
                return True
    return False


@torch.no_grad()
def smooth_lm(model, scales, model_type="auto", alpha=0.5, remote_dir=None):
    """Compute the model weight using smooth quant

    Parameters
    ----------
    model: class
        the model of LLM.
    scales: dict
        the scale parameters of model
    model_type: str
        the type of LLM, Defaults to "auto".
    alpha: float
        the parameter of smooth quant required. Defaults to 0.5.
    remote_dir: str
        the path of LLM. Defaults to None.

    """
    from transformers.dynamic_module_utils import get_class_from_dynamic_module

    assert isinstance(model_type, str)
    if model_type == "auto":
        if remote_dir == None:
            raise ValueError(f"model path is null.")
        model_type = _detect_model_type(remote_dir)

    if model_type in _get_local_smooth_policy().keys():
        smooth_dict = _get_local_smooth_policy()[model_type]
        for name, module in model.named_modules():
            if isinstance(module, smooth_dict["decoder_name"]):
                attn_ln = getattr(module, smooth_dict["attn_ln"])
                assert _norm_type_assert(attn_ln, smooth_dict["norm_type"], remote_dir)
                qkv = []
                for key in smooth_dict["qkv"]:
                    attr_lt = key.split(".")
                    val = module
                    for i in range(len(attr_lt)):
                        val = getattr(val, attr_lt[i])
                    qkv.append(val)
                qkv_input_scales = scales[name + smooth_dict["qkv_input_scales"]]
                _smooth_ln_fcs(attn_ln, qkv, qkv_input_scales, alpha)

                ffn_ln = getattr(module, smooth_dict["ffn_ln"])  # feed forward norm
                assert _norm_type_assert(ffn_ln, smooth_dict["norm_type"], remote_dir)
                fcs = []
                for key in smooth_dict["fcs"]:
                    attr_lt = key.split(".")
                    val = module
                    for i in range(len(attr_lt)):
                        val = getattr(val, attr_lt[i])
                    fcs.append(val)
                fcs_input_scales = scales[name + smooth_dict["fcs_input_scales"]]
                _smooth_ln_fcs(ffn_ln, fcs, fcs_input_scales, alpha)

    elif model_type in _get_remote_smooth_policy().keys():
        for name, module in model.named_modules():
            smooth_dict = _get_remote_smooth_policy()[model_type]
            decoder = get_class_from_dynamic_module(smooth_dict["decoder_name"], remote_dir)
            if str(type(module)) == str(decoder):
                attn_ln = getattr(module, smooth_dict["attn_ln"])
                assert _norm_type_assert(attn_ln, smooth_dict["norm_type"], remote_dir)
                qkv = []
                for key in smooth_dict["qkv"]:
                    attr_lt = key.split(".")
                    val = module
                    for i in range(len(attr_lt)):
                        val = getattr(val, attr_lt[i])
                    qkv.append(val)
                qkv_input_scales = scales[name + smooth_dict["qkv_input_scales"]]
                _smooth_ln_fcs(attn_ln, qkv, qkv_input_scales, alpha)

                ffn_ln = getattr(module, smooth_dict["ffn_ln"])  # feed forward norm
                assert _norm_type_assert(ffn_ln, smooth_dict["norm_type"], remote_dir)
                fcs = []
                for key in smooth_dict["fcs"]:
                    attr_lt = key.split(".")
                    val = module
                    for i in range(len(attr_lt)):
                        val = getattr(val, attr_lt[i])
                    fcs.append(val)
                fcs_input_scales = scales[name + smooth_dict["fcs_input_scales"]]
                _smooth_ln_fcs(ffn_ln, fcs, fcs_input_scales, alpha)

    else:
        raise ValueError(f"model is not supported.")


def get_act_layer_scales(model, tokenizer, dataset, num_samples=512, seq_len=512):
    """get the active layer scale

    Parameters
    ----------
    model: class
        the model of LLM.
    tokenizer: class
        the tokenizer of LLM.
    dataset:  object
        the caliberate dataset
    num_samples: int
        the num of samples. Defaults to 512.
    seq_len: int
        the max length of sequence. Defaults to 512.

    """
    model.eval()
    device = next(model.parameters()).device
    act_scales = {}

    def stat_tensor(name, tensor):
        hidden_dim = tensor.shape[-1]
        tensor = tensor.view(-1, hidden_dim).abs().detach()
        comming_max = torch.max(tensor, dim=0)[0].float().cpu()
        if name in act_scales:
            act_scales[name] = torch.max(act_scales[name], comming_max)
        else:
            act_scales[name] = comming_max

    def stat_input_hook(m, x, y, name):
        if isinstance(x, tuple):
            x = x[0]
        stat_tensor(name, x)

    hooks = []
    for name, m in model.named_modules():
        if isinstance(m, nn.Linear):
            hooks.append(m.register_forward_hook(functools.partial(stat_input_hook, name=name)))

    dataset = dataset.shuffle(seed=42)

    for i in tqdm(range(num_samples)):
        input_ids = tokenizer(
            dataset[i]["text"], return_tensors="pt", max_length=seq_len, truncation=True
        ).input_ids.to(device)
        try:
            input_shape = input_ids.size()
            input_ids = input_ids.view(-1, input_shape[-1])
        except RuntimeError:
            continue
        model(input_ids)

    for h in hooks:
        h.remove()
    return act_scales


def _create_dict_model(model, ft_dict):
    for name, module in model.named_children():
        if name == "":
            continue
        cd_dict = {}
        if any(module.children()):
            _create_dict_model(module, cd_dict)
            ft_dict[name] = cd_dict
        else:
            has_weight = False
            for param_name, _ in module.named_parameters():
                param_dict = {}
                cd_dict[param_name] = param_dict
                has_weight = True
            if not has_weight:
                continue
            ft_dict[name] = cd_dict


def smooth_quantized_convert_model_to_json(
    model, config=None, model_type: str = "", quant_config={}, save_dir="hhb_out"
):
    """_summary_

    Args:
        model (Pytorch model): origin model.
        config (json): config json file of LLM.
        save_dir (str, optional): _description_. Defaults to "hhb_out".

    Returns:
        _type_: _description_
    """
    """
        bits: 4
        W shape: (infeatures, outfeatures), ((4096, 2048), float16)

        quantize:
            Q shape: (infeatures, outfeatures), ((4096, 2048), int4)
            scales shape: per_channel (4096); per_tensor (1)

        pack:
            Q[:, :1024] | (Q[:, 1024:]<<4)
            Q ((4096, 2048), int4) ---> pack_col(Q) ((4096, 1024), int8)
    """

    class ModelConverter:
        """_summary_"""

        def __init__(
            self, model, config, save_path, param_dict, quant_layer_name, quant_config
        ) -> None:
            """ """
            self.model_dict = model.state_dict()
            self.config = config
            self.save_path = save_path
            self.global_dict = param_dict
            self.quant_layer_name = quant_layer_name
            self.quant_config = quant_config

        def _quant_weight(self, weight, quant_config):
            assert isinstance(quant_config, dict), "quant_config type is not dict"
            if quant_config["weight_quant"] == "per_channel":
                return quantize_weight_per_channel_absmax(weight, quant_config["w_bits"], True)
            elif quant_config["weight_quant"] == "per_tensor":
                return quantize_weight_per_tensor_absmax(weight, quant_config["w_bits"], True)
            else:
                raise ValueError(f"unsupported quant_range in smooth_quant")

        def convert_to_json(self):
            bin_file_path = "/".join([self.save_path, "shl_llm_weight.bin"])
            json_file_path = "/".join([self.save_path, "shl_llm_weight.json"])
            data_offset = 0
            time = 0
            with open(bin_file_path, "wb") as weight_file:
                for key, value in self.model_dict.items():
                    time += 1
                    dims = {}
                    for i in range(value.ndim):
                        dims[str(i)] = value.shape[i]
                    save_have = False
                    for element in self.quant_layer_name:
                        if element in key:
                            if not key.endswith(".bias"):
                                data, scale = self._quant_weight(value, self.quant_config)
                                data = data.to(torch.int8)
                                if self.quant_config["w_bits"] == 4:
                                    if data.ndim == 1:
                                        data = (
                                            data[: int(data.shape[0] / 2)]
                                            | (data[int(data.shape[0] / 2) :] << 4)
                                        ).flatten()
                                    elif data.ndim == 2:
                                        data = (
                                            data[:, : int(data.shape[1] / 2)]
                                            | (data[:, int(data.shape[1] / 2) :] << 4)
                                        ).flatten()
                                data = data.to("cpu").numpy()
                                scale = scale.to("cpu").numpy()
                                weight_file.write(data.tobytes())
                                weight_file.write(scale.tobytes())
                                data_offset += data.nbytes
                                data_offset += scale.nbytes
                                save_have = True
                                break
                    if not save_have:
                        data = value.to("cpu").numpy()
                        bytes_to_save = data.tobytes()
                        weight_file.write(bytes_to_save)
                        data_offset += data.nbytes

                    key_split_lt = key.split(".")
                    temp_dict = self.global_dict
                    have_saved_in_dict = True
                    for child_t in key_split_lt:
                        if temp_dict.get(child_t) is None:
                            have_saved_in_dict = False
                            break
                        else:
                            temp_dict = temp_dict[child_t]
                    if not have_saved_in_dict:
                        t_dict = {}
                        temp_dict[key_split_lt[-1]] = t_dict
                    else:
                        t_dict = temp_dict
                    logger.log(
                        LOG,
                        f"[{time:{3}d}/{len(self.model_dict.items())}] Writing tensor: {key:70s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(data.dtype):4}",
                    )
                    t_dict["name"] = key
                    t_dict["data_offset"] = data_offset
                    t_dict["dim"] = dims
                    t_dict["mtype"] = csinn_mem_type_enum.CSINN_MEM_TYPE_SQ.value
                    t_dict["dtype"] = DtypeToSHLDtype[str(data.dtype)]

            content = {}
            content["config_dict"] = {}
            if self.config.get("_name_or_path") is not None:
                del self.config["_name_or_path"]
            content["config_dict"]["model_params"] = self.config
            content["config_dict"]["shl_params"] = {}
            content["config_dict"]["shl_params"]["shl_model_type"] = "weight_only"
            content["config_dict"]["shl_params"]["quant_config"] = self.quant_config
            content["model_dict"] = self.global_dict
            out_file = open(json_file_path, "w")
            json.dump(content, out_file, indent=4)
            print(f"data_offset: {data_offset}")

    from .fake_quant import _get_local_models, _get_remote_models
    from .fake_quant import quantize_weight_per_channel_absmax, quantize_weight_per_tensor_absmax

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    logger.log(LOG, "Convert model to json file")
    if not isinstance(config, dict):
        config = config.to_dict()
    param_dict = {}
    _create_dict_model(model, param_dict)
    assert isinstance(model_type, str)
    if model_type in _get_local_models().keys():
        quant_layer_name = [
            element
            for data in _get_local_models()[model_type]["module"].values()
            for element in data
        ]
    elif model_type in _get_remote_models().keys():
        quant_layer_name = [
            element
            for data in _get_remote_models()[model_type]["module"].values()
            for element in data
        ]
    else:
        raise ValueError(f"unsupported model_type: {model_type}")
    model_converter = ModelConverter(
        model, config, save_dir, param_dict, quant_layer_name, quant_config
    )
    model_converter.convert_to_json()
    logger.log(LOG, "Convert end...")


def hhb_smoothquant(
    pretrained_model_dir=None,
    quant_config_file=None,
    save_dir="hhb_out",
    fake_quantize=False,
    **kwargs,
):
    """Using smooth_quant to quantize the model.

    Parameters
    ----------
    pretrained_model_dir : str
        the path of LLM, Defaults to None
    quant_config_file : str or dict
        the path of config that used in smoothquant. Defaults to None
    save_dir : str
        the save path of quantized model. Defaults to "hhb_out"
    fake_quantize : bool
        whether to return the fake quantized model. Defaults to False
    kwargs : dict
        the parameters of auto gptq needed in func quantize
    """

    from datasets import load_dataset
    from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
    from .fake_quant import smooth_fake_quantize_model

    model_args = kwargs.pop("model_args", {})
    device = kwargs.pop("device", "cpu")
    tokenizer_args = kwargs.pop("tokenizer_args", {})

    act_scales = kwargs.pop("act_scales", None)
    num_samples = kwargs.pop("num_samples", 256)
    seq_len = kwargs.pop("seq_len", 256)
    save_act_value = kwargs.pop("save_act_value", False)
    alpha = kwargs.pop("alpha", 0.5)
    w_bits = kwargs.pop("w_bits", 8)
    a_bits = kwargs.pop("a_bits", 8)
    weight_quant = kwargs.pop("weight_quant", "per_channel")
    act_quant = kwargs.pop("act_quant", "per_token")
    dataset = kwargs.pop("dataset", None)
    model_type = kwargs.pop("model_type", "auto")

    if isinstance(quant_config_file, str):
        if not os.path.exists(quant_config_file) or not quant_config_file.endswith(".json"):
            logger.error("quantization config file {} is not find".format(quant_config_file))
            sys.exit()
        with open(quant_config_file, "r") as config_file:
            quant_args = json.load(config_file)
    elif isinstance(quant_config_file, dict):
        quant_args = quant_config_file
    else:
        raise TypeError(f"Unexpected quantize config: {quant_config_file}")

    if quant_args.get("model_args"):
        model_args = quant_args["model_args"]
    if quant_args.get("device"):
        device = quant_args["device"]
    if quant_args.get("tokenizer_args"):
        tokenizer_args = quant_args["tokenizer_args"]

    model = AutoModelForCausalLM.from_pretrained(
        pretrained_model_dir, trust_remote_code=True, torch_dtype="auto", **model_args
    )
    if device == "cuda":
        model.to("cuda")
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_dir, trust_remote_code=True, model_max_length=512, **tokenizer_args
    )

    if quant_args.get("act_scales"):
        act_scales = quant_args["act_scales"]

    if act_scales is None:
        if quant_args.get("dataset"):
            dataset = quant_args["dataset"]
        else:
            raise ValueError(f"calibrate dataset is required")

        if isinstance(dataset, str):
            calib_dataset = load_dataset(dataset, split="test")
        else:
            calib_dataset = dataset

        if quant_args.get("num_samples"):
            num_samples = quant_args["num_samples"]
        if quant_args.get("seq_len"):
            seq_len = quant_args["seq_len"]
        act_scales = get_act_layer_scales(
            model, tokenizer, calib_dataset, num_samples=num_samples, seq_len=seq_len
        )
        if quant_args.get("save_act_value"):
            save_act_value = quant_args["save_act_value"] == "true"
        if save_act_value:
            logger.log(LOG, f"save act scales to {save_dir}/act_value.pt")
            os.makedirs(os.path.dirname(save_dir + "/act_value.pt"), exist_ok=True)
            torch.save(act_scales, save_dir + "/act_value.pt")
    else:
        if isinstance(act_scales, str):
            logger.log(LOG, f"load act scales from {act_scales}")
            act_scales = torch.load(act_scales)

    if quant_args.get("alpha"):
        alpha = quant_args["alpha"]
    if quant_args.get("model_type"):
        model_type = quant_args["model_type"]
    if model_type == "auto":
        model_type = _detect_model_type(pretrained_model_dir)
    smooth_lm(
        model, act_scales, model_type=model_type, alpha=alpha, remote_dir=pretrained_model_dir
    )

    config = AutoConfig.from_pretrained(pretrained_model_dir, trust_remote_code=True)
    if quant_args.get("w_bits"):
        w_bits = quant_args["w_bits"]
    if quant_args.get("weight_quant"):
        weight_quant = quant_args["weight_quant"]
    quant_config = {
        "w_bits": w_bits,
        "weight_quant": weight_quant,
    }
    smooth_quantized_convert_model_to_json(model, config, model_type, quant_config, save_dir)

    qdq_model = None
    if fake_quantize:
        logger.log(LOG, f"Start fake_quantize")
        if quant_args.get("a_bits"):
            a_bits = quant_args["a_bits"]
        if quant_args.get("act_quant"):
            act_quant = quant_args["act_quant"]
        qdq_model = smooth_fake_quantize_model(
            model,
            model_type=model_type,
            weight_quant=weight_quant,
            act_quant=act_quant,
            w_bits=w_bits,
            a_bits=a_bits,
            remote_dir=pretrained_model_dir,
        )
        logger.log(LOG, f"Fake_quantize end...")
    return qdq_model

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
fake quantization function of smoothquant.
"""
import os
import logging
import json
from pathlib import Path
import torch
from torch import nn
from functools import partial
from typing import Dict

logger = logging.getLogger("HHB")
LOG = 25


def _get_local_models():
    from transformers.models.opt.modeling_opt import (
        OPTAttention,
        OPTDecoderLayer,
    )
    from transformers.models.llama.modeling_llama import (
        LlamaSdpaAttention,
        LlamaMLP,
    )

    from transformers.models.mistral.modeling_mistral import (
        MistralAttention,
        MistralMLP,
    )

    from transformers.models.mixtral.modeling_mixtral import (
        MixtralAttention,
        MixtralSparseMoeBlock,
        MixtralBLockSparseTop2MLP,
    )
    from transformers.models.falcon.modeling_falcon import (
        FalconAttention,
        FalconMLP,
    )

    LOCAL_MODELS: Dict[str, dict] = {
        "opt": {
            "quantize_bmm_input": ["q_proj", "k_proj", "v_proj"],
            "module": {
                OPTAttention: ["fc1", "fc2"],
                OPTDecoderLayer: ["q_proj", "k_proj", "v_proj", "out_proj"],
            },
        },
        "llama": {
            "quantize_bmm_input": ["q_proj", "k_proj", "v_proj"],
            "module": {
                LlamaSdpaAttention: ["q_proj", "k_proj", "v_proj", "o_proj"],
                LlamaMLP: ["gate_proj", "up_proj", "down_proj"],
            },
        },
        "mistral": {
            "quantize_bmm_input": ["q_proj", "k_proj", "v_proj"],
            "module": {
                MistralAttention: ["q_proj", "k_proj", "v_proj", "o_proj"],
                MistralMLP: ["gate_proj", "up_proj", "down_proj"],
            },
        },
        "mixtral": {
            "quantize_bmm_input": ["q_proj", "k_proj", "v_proj"],
            "module": {
                MixtralAttention: ["q_proj", "k_proj", "v_proj", "o_proj"],
                MixtralSparseMoeBlock: ["gate"],
                MixtralBLockSparseTop2MLP: ["w1", "w2", "w3"],
            },
        },
        "falcon": {
            "quantize_bmm_input": ["query_key_value"],
            "module": {
                FalconAttention: ["query_key_value", "dense"],
                FalconMLP: ["dense_h_to_4h", "dense_4h_to_h"],
            },
        },
    }
    return LOCAL_MODELS


def _get_remote_models():
    REMOTE_MODELS: Dict[str, dict] = {
        "qwen": {
            "quantize_bmm_input": ["c_attn"],
            "module": {
                "modeling_qwen.QWenMLP": ["w1", "w2"],
                "modeling_qwen.QWenAttention": ["c_attn", "c_proj"],
            },
        },
        "chatglm": {
            "quantize_bmm_input": ["query_key_value"],
            "module": {
                "modeling_chatglm.MLP": ["dense_h_to_4h", "dense_4h_to_h"],
                "modeling_chatglm.SelfAttention": ["query_key_value", "dense"],
            },
        },
    }
    return REMOTE_MODELS


@torch.no_grad()
def quantize_weight_per_channel_absmax(w, n_bits=8, real_quant=False):
    # w: (out_features, in_features)
    assert n_bits == 8 or n_bits == 4, "only support n_bits in [4, 8]"
    scales = w.abs().max(dim=-1, keepdim=True)[0]
    q_min = -(2 ** (n_bits - 1))
    q_max = 2 ** (n_bits - 1) - 1
    scales = torch.clamp(scales / q_max, min=1e-5)
    if n_bits == 8:
        q_w = torch.clamp(torch.round(w / scales), q_min, q_max)
    elif n_bits == 4:
        q_w = torch.clamp(torch.round(w / scales + 8), 0, 15)
    if real_quant:
        return q_w, scales
    return q_w * scales


@torch.no_grad()
def quantize_weight_per_tensor_absmax(w, n_bits=8, real_quant=False):
    # w: (out_features, in_features)
    assert n_bits == 8 or n_bits == 4, "only support n_bits in [4, 8]"
    scales = w.abs().max()
    q_min = -(2 ** (n_bits - 1))
    q_max = 2 ** (n_bits - 1) - 1
    scales = torch.clamp(scales / q_max, min=1e-5)
    if n_bits == 8:
        q_w = torch.clamp(torch.round(w / scales), q_min, q_max)
    elif n_bits == 4:
        q_w = torch.clamp(torch.round(w / scales + 8), 0, 15)
    if real_quant:
        return q_w, scales
    return q_w * scales


@torch.no_grad()
def quantize_activation_per_token_absmax(t, n_bits=8):
    t_shape = t.shape
    t.view(-1, t_shape[-1])
    scales = t.abs().max(dim=-1, keepdim=True)[0]
    q_max = 2 ** (n_bits - 1) - 1
    scales.clamp_(min=1e-5).div_(q_max)
    t.div_(scales).round_().mul_(scales)
    return t


@torch.no_grad()
def quantize_activation_per_tensor_absmax(t, n_bits=8):
    t_shape = t.shape
    t.view(-1, t_shape[-1])
    scales = t.abs().max()
    q_max = 2 ** (n_bits - 1) - 1
    scales.clamp_(min=1e-5).div_(q_max)
    t.div_(scales).round_().mul_(scales)
    return t


class WQAQLinear(nn.Module):
    def __init__(
        self,
        in_features,
        out_features,
        bias=True,
        act_quant="per_token",
        quantize_output=False,
        a_bits=8,
    ):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features

        self.register_buffer(
            "weight",
            torch.randn(
                self.out_features,
                self.in_features,
                dtype=torch.float16,
                requires_grad=False,
            ),
        )
        if bias:
            self.register_buffer(
                "bias",
                torch.zeros((1, self.out_features), dtype=torch.float16, requires_grad=False),
            )
        else:
            self.register_buffer("bias", None)

        if act_quant == "per_token":
            self.act_quant_name = "per_token"
            self.act_quant = partial(quantize_activation_per_token_absmax, n_bits=a_bits)
        elif act_quant == "per_tensor":
            self.act_quant_name = "per_tensor"
            self.act_quant = partial(quantize_activation_per_tensor_absmax, n_bits=a_bits)
        else:
            raise ValueError(f"Invalid act_quant: {act_quant}")

        if quantize_output:
            self.output_quant_name = self.act_quant_name
            self.output_quant = self.act_quant
        else:
            self.output_quant_name = "None"
            self.output_quant = lambda x: x

    def to(self, *args, **kwargs):
        super(WQAQLinear, self).to(*args, **kwargs)
        self.weight = self.weight.to(*args, **kwargs)
        if self.bias is not None:
            self.bias = self.bias.to(*args, **kwargs)
        return self

    @torch.no_grad()
    def forward(self, x):
        q_x = self.act_quant(x)
        y = torch.functional.F.linear(q_x, self.weight, self.bias)
        q_y = self.output_quant(y)
        return q_y

    @staticmethod
    def from_float(
        module,
        weight_quant="per_channel",
        act_quant="per_token",
        quantize_output=False,
        w_bits=8,
        a_bits=8,
    ):
        assert isinstance(module, torch.nn.Linear)
        new_module = WQAQLinear(
            module.in_features,
            module.out_features,
            module.bias is not None,
            act_quant=act_quant,
            quantize_output=quantize_output,
            a_bits=a_bits,
        )
        if weight_quant == "per_channel":
            new_module.weight = quantize_weight_per_channel_absmax(
                module.weight, n_bits=w_bits
            )  # use 8-bit integer for weight
        elif weight_quant == "per_tensor":
            new_module.weight = quantize_weight_per_tensor_absmax(module.weight, n_bits=w_bits)
        else:
            raise ValueError(f"Invalid weight_quant: {weight_quant}")
        new_module.weight_quant_name = weight_quant  # type: ignore
        if module.bias is not None:
            new_module.bias = module.bias
        return new_module

    def __repr__(self):
        return f"WQAQLinear({self.in_features}, {self.out_features}, bias={self.bias is not None}, weight_quant={self.weight_quant_name}, act_quant={self.act_quant_name}, output_quant={self.output_quant_name})"


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


def smooth_fake_quantize_model(
    model,
    model_type="auto",
    weight_quant="per_channel",
    act_quant="per_token",
    quantize_bmm_input=False,
    w_bits=8,
    a_bits=8,
    remote_dir=None,
):

    assert isinstance(model_type, str)
    if model_type == "auto":
        if remote_dir == None:
            raise ValueError(f"model path is null.")
        model_type = _detect_model_type(remote_dir)

    if model_type in _get_local_models().keys():
        quant_block_dict = _get_local_models()[model_type]
        for name, module in model.named_modules():
            for module_class_type in quant_block_dict["module"].keys():
                if isinstance(module, module_class_type):
                    logger.log(LOG, f"Quantize the module {name}")
                    for attr_name in quant_block_dict["module"][module_class_type]:
                        if attr_name in quant_block_dict["quantize_bmm_input"]:
                            quantize_bmm_input = True
                        attr = getattr(module, attr_name)
                        new_attr = WQAQLinear.from_float(
                            attr,
                            weight_quant=weight_quant,
                            act_quant=act_quant,
                            quantize_output=quantize_bmm_input,
                            w_bits=w_bits,
                            a_bits=a_bits,
                        )
                        setattr(module, attr_name, new_attr)
    elif model_type in _get_remote_models().keys():
        from transformers.dynamic_module_utils import get_class_from_dynamic_module

        quant_class_dict = _get_remote_models()[model_type]["module"]
        for class_name in quant_class_dict.keys():
            cls = get_class_from_dynamic_module(class_name, remote_dir)  # type: ignore
            for name, module in model.named_modules():
                if str(type(module)) == str(cls):
                    logger.log(LOG, f"Quantize the module {name}")
                    for attr_name in quant_class_dict[class_name]:
                        if attr_name in _get_remote_models()[model_type]["quantize_bmm_input"]:
                            quantize_bmm_input = True
                        attr = getattr(module, attr_name)
                        new_attr = WQAQLinear.from_float(
                            attr,
                            weight_quant=weight_quant,
                            act_quant=act_quant,
                            quantize_output=quantize_bmm_input,
                            w_bits=w_bits,
                            a_bits=a_bits,
                        )
                        setattr(module, attr_name, new_attr)
    else:
        raise ValueError(f"model is not supported.")

    return model

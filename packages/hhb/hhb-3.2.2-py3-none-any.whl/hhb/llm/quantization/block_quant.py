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
Quantization tools of LLM.
"""
import ctypes
import logging
import sys
import json
import torch
import numpy as np
from collections import OrderedDict
from tvm.relay.backend.contrib.csinn_backend import llm_quantize_block, llm_dequantize_block

from ..llm_util import (
    csinn_mem_type_enum,
    DtypeToSHLDtype,
    QtypeToSHLMemtype,
    QtypeToSHLDtype,
    unify_layer_name,
)

logger = logging.getLogger("HHB")
LOG = 25


def quantize_model_with_kosmos(
    model, config, quantization_scheme, save_dir="hhb_out", fake_quantize=False
):
    """parse llm, convert model to json

    Args:
        model (_type_): _description_
        config (_type_, optional): _description_. Defaults to None.
        quantization_scheme (str, optional): _description_. Defaults to "float32".
        save_path (str, optional): _description_. Defaults to "hhb_out".

    Returns:
        _type_: _description_
    """

    class Quantizer:
        """_summary_"""

        def __init__(self, model, config, qtype, ftype, save_path, **kwargs) -> None:
            """ """
            self.model = model
            self.model_dict = model.state_dict()
            self.config = config
            self.qtype = qtype
            self.ftype = ftype
            self.save_path = save_path
            self.fake_quantize = kwargs.pop("fake_quantize", False)

        def quantize_dequantize_internal(self, data, qtype):
            """_summary_

            Args:
                data (torch.Tensor, numpy.ndarray): float weight
                mtype (csinn_mem_type_enum): _description_

            Returns:
                int : length of quantized weight, scale, zero_point
            """
            if isinstance(type(data), np.ndarray):
                data = data.numpy()
            dtype = DtypeToSHLDtype[str(data.dtype)]
            dim_count = data.ndim
            data_ptr = data.ctypes.data_as(ctypes.c_void_p)
            dim = np.array([data.shape[i] for i in range(dim_count)], dtype=np.int32)
            dim_ptr = dim.ctypes.data_as(ctypes.c_void_p)
            mtype = QtypeToSHLMemtype[str(qtype)]
            quantized_data = llm_quantize_block(data_ptr, dtype, dim_count, dim_ptr, mtype)
            quantized_data = np.frombuffer(quantized_data, dtype=np.uint8)
            quantized_data_ptr = quantized_data.ctypes.data_as(ctypes.c_void_p)
            dequantized_data = llm_dequantize_block(
                quantized_data_ptr,
                mtype,
                dim_count,
                dim_ptr,
                dtype,
            )
            result = np.frombuffer(dequantized_data, dtype=data.dtype).reshape(data.shape)
            return result

        def quantize_block_internal(self, weight_file, data, qtype):
            """_summary_

            Args:
                weight_file (_io.BufferedWriter): bin_file of quantized weight, scale, zero_point
                data (torch.Tensor, numpy.ndarray): float weight
                mtype (csinn_mem_type_enum): _description_

            Returns:
                int : length of quantized weight, scale, zero_point
            """
            if isinstance(type(data), np.ndarray):
                data = data.numpy()
            dtype = DtypeToSHLDtype[str(data.dtype)]
            dim_count = data.ndim
            data_ptr = data.ctypes.data_as(ctypes.c_void_p)
            dim = np.array([data.shape[i] for i in range(dim_count)], dtype=np.int32)
            dim_ptr = dim.ctypes.data_as(ctypes.c_void_p)
            mtype = QtypeToSHLMemtype[str(qtype)]
            result = llm_quantize_block(data_ptr, dtype, dim_count, dim_ptr, mtype)
            weight_file.write(result)
            return len(result)

        def quantize(self):
            if self.fake_quantize:
                new_dict = OrderedDict()
            bin_file_path = "/".join([self.save_path, "shl_llm_weight_quantize.bin"])
            json_file_path = "/".join([self.save_path, "shl_llm_weight_quantize.json"])
            data_offset = 0
            content = {}
            model = {}
            tensor_none = {}

            text_layers = []
            text_num_layers = 0
            if self.config.get("text_config") is not None:
                if self.config["text_config"].get("layers") is not None:
                    text_num_layers = self.config["text_config"]["layers"]
                else:
                    logger.error("text_num_layers is required")
                    sys.exit(0)
            for i in range(text_num_layers):
                text_layers.append(tensor_none.copy())

            vision_num_layers = 0
            if self.config.get("vision_config") is not None:
                if self.config["vision_config"].get("num_hidden_layers") is not None:
                    vision_num_layers = self.config["vision_config"]["num_hidden_layers"]
                else:
                    logger.error("vision_num_layers is required")
                    sys.exit(0)
            image_layers = []
            for i in range(vision_num_layers):
                image_layers.append(tensor_none.copy())

            time = 0
            with open(bin_file_path, "wb") as weight_file:
                for key, value in self.model.state_dict().items():
                    time += 1
                    tensor = {}
                    tensor["data_offset"] = data_offset
                    dims = {}
                    for i in range(value.ndim):
                        dims[str(i)] = value.shape[i]
                    tensor["dim"] = dims
                    tensor["dim_count"] = value.ndim
                    data = value.to("cpu").numpy()
                    name = key
                    # print(key)
                    # text
                    if "embed_tokens" in key:
                        name = "embed_tokens"
                        if self.qtype in ["q8_0", "q4_0", "q4_1", "q4_k", "q2_k", "nf4_0"]:
                            data = data.astype(np.float16)
                            logger.log(
                                LOG,
                                f"[{time:{3}d}/{len(self.model_dict.items())}] Quantize layer: {key:65s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(value.dtype):4} -> {str(self.qtype):4}",
                            )
                            offset = self.quantize_block_internal(
                                weight_file,
                                data,
                                self.qtype,
                            )
                            if self.fake_quantize:
                                new_dict[key] = torch.from_numpy(
                                    self.quantize_dequantize_internal(data, self.qtype)
                                )
                            tensor["dtype"] = QtypeToSHLDtype[self.qtype]
                            tensor["mtype"] = QtypeToSHLMemtype[self.qtype]
                            tensor["name"] = key
                            model["embed_tokens"] = tensor
                            data_offset += offset
                        else:
                            if self.fake_quantize:
                                new_dict[key] = value
                            if self.ftype == "fp16":
                                data = data.astype(np.float16)
                                tensor["dtype"] = DtypeToSHLDtype["float16"]
                            else:
                                tensor["dtype"] = DtypeToSHLDtype["float32"]
                            bytes_to_save = data.tobytes()
                            weight_file.write(bytes_to_save)
                            offset = data.nbytes
                            tensor[
                                "mtype"
                            ] = csinn_mem_type_enum.CSINN_MEM_TYPE_CPU_NOT_ALIGNED.value
                            tensor["name"] = key
                            model[name] = tensor
                            data_offset += offset

                    elif "model.layer_norm" in key:
                        if self.fake_quantize:
                            new_dict[key] = value
                        if "weight" in key:
                            name = "layer_norm"
                        elif "bias" in key:
                            name = "layer_norm_b"
                        if self.ftype == "fp16":
                            data = data.astype(np.float16)
                            tensor["dtype"] = DtypeToSHLDtype["float16"]
                        else:
                            tensor["dtype"] = DtypeToSHLDtype["float32"]
                        logger.log(
                            LOG,
                            f"[{time:{3}d}/{len(self.model_dict.items())}] Quantize layer: {key:65s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(value.dtype):4} -> {str(data.dtype):4}",
                        )
                        bytes_to_save = data.tobytes()
                        weight_file.write(bytes_to_save)
                        offset = data.nbytes
                        tensor["mtype"] = csinn_mem_type_enum.CSINN_MEM_TYPE_CPU_NOT_ALIGNED.value
                        tensor["name"] = key
                        model[name] = tensor
                        data_offset += offset

                    elif "lm_head" in key:
                        name = "lm_head"
                        if self.qtype in ["q8_0", "q4_0", "q4_1", "q4_k", "q2_k", "nf4_0"]:
                            logger.log(
                                LOG,
                                f"[{time:{3}d}/{len(self.model_dict.items())}] Quantize layer: {key:65s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(value.dtype):4} -> {str(self.qtype):4}",
                            )
                            data = data.astype(np.float16)
                            offset = self.quantize_block_internal(
                                weight_file,
                                data,
                                self.qtype,
                            )
                            if self.fake_quantize:
                                new_dict[key] = torch.from_numpy(
                                    self.quantize_dequantize_internal(data, self.qtype)
                                )
                            tensor["dtype"] = QtypeToSHLDtype[self.qtype]
                            tensor["mtype"] = QtypeToSHLMemtype[self.qtype]
                            tensor["name"] = key
                            model[name] = tensor
                            data_offset += offset
                        else:
                            if self.fake_quantize:
                                new_dict[key] = value
                            if self.ftype == "fp16":
                                data = data.astype(np.float16)
                                tensor["dtype"] = DtypeToSHLDtype["float16"]
                            else:
                                tensor["dtype"] = DtypeToSHLDtype["float32"]
                            bytes_to_save = data.tobytes()
                            weight_file.write(bytes_to_save)
                            offset = data.nbytes
                            tensor[
                                "mtype"
                            ] = csinn_mem_type_enum.CSINN_MEM_TYPE_CPU_NOT_ALIGNED.value
                            tensor["name"] = key
                            model[name] = tensor
                            data_offset += offset
                    elif "text_model.model.layers" in key:
                        layer_numer = int(key.split(".")[3])
                        if (
                            self.qtype in ["q8_0", "q4_0", "q4_1", "q4_k", "q2_k", "nf4_0"]
                            and value.ndim == 2
                        ):
                            logger.log(
                                LOG,
                                f"[{time:{3}d}/{len(self.model_dict.items())}] Quantize layer: {key:65s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(value.dtype):4} -> {str(self.qtype):4}",
                            )
                            data = data.astype(np.float16)
                            offset = self.quantize_block_internal(
                                weight_file,
                                data,
                                self.qtype,
                            )
                            if self.fake_quantize:
                                new_dict[key] = torch.from_numpy(
                                    self.quantize_dequantize_internal(data, self.qtype)
                                )
                            tensor["dtype"] = QtypeToSHLDtype[self.qtype]
                            tensor["mtype"] = QtypeToSHLMemtype[self.qtype]
                            tensor["name"] = key
                            text_layers[layer_numer][key] = tensor
                            data_offset += offset

                        else:
                            if self.fake_quantize:
                                new_dict[key] = value
                            if self.ftype == "fp16":
                                data = data.astype(np.float16)
                                tensor["dtype"] = DtypeToSHLDtype["float16"]
                            else:
                                tensor["dtype"] = DtypeToSHLDtype["float32"]
                            logger.log(
                                LOG,
                                f"[{time:{3}d}/{len(self.model_dict.items())}] Quantize layer: {key:65s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(value.dtype):4} -> {str(data.dtype):4}",
                            )
                            bytes_to_save = data.tobytes()
                            weight_file.write(bytes_to_save)
                            offset = data.nbytes
                            tensor[
                                "mtype"
                            ] = csinn_mem_type_enum.CSINN_MEM_TYPE_CPU_NOT_ALIGNED.value
                            tensor["name"] = key
                            text_layers[layer_numer][key] = tensor
                            data_offset += offset
                    # vision
                    # vision model's weight do not quant to int
                    elif (
                        "class_embedding" in key
                        or "patch_embedding" in key
                        or "position_embedding" in key
                        or "pre_layrnorm" in key
                        or "post_layernorm" in key
                    ):

                        if "class_embedding" in key:
                            name = "class_embedding"
                        elif "patch_embedding" in key:
                            name = "patch_embedding"
                        elif "position_embedding" in key:
                            name = "position_embedding"
                        elif "pre_layrnorm" in key:
                            if "weight" in key:
                                name = "pre_layrnorm"
                            elif "bias" in key:
                                name = "pre_layrnorm_b"
                        elif "post_layernorm" in key:
                            if "weight" in key:
                                name = "post_layernorm"
                            elif "bias" in key:
                                name = "post_layernorm_b"
                        if self.fake_quantize:
                            new_dict[key] = value
                        if self.ftype == "fp16":
                            data = data.astype(np.float16)
                            tensor["dtype"] = DtypeToSHLDtype["float16"]
                        else:
                            tensor["dtype"] = DtypeToSHLDtype["float32"]
                        logger.log(
                            LOG,
                            f"[{time:{3}d}/{len(self.model_dict.items())}] Quantize layer: {key:65s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(value.dtype):4} -> {str(data.dtype):4}",
                        )
                        bytes_to_save = data.tobytes()
                        weight_file.write(bytes_to_save)
                        offset = data.nbytes
                        tensor["mtype"] = csinn_mem_type_enum.CSINN_MEM_TYPE_CPU_NOT_ALIGNED.value
                        tensor["name"] = key
                        model[name] = tensor
                        data_offset += offset

                    elif "vision_model.model.encoder.layers" in key:
                        if self.fake_quantize:
                            new_dict[key] = value
                        layer_numer = int(key.split(".")[4])
                        if self.ftype == "fp16":
                            data = data.astype(np.float16)
                            tensor["dtype"] = DtypeToSHLDtype["float16"]
                        else:
                            tensor["dtype"] = DtypeToSHLDtype["float32"]
                        logger.log(
                            LOG,
                            f"[{time:{3}d}/{len(self.model_dict.items())}] Quantize layer: {key:65s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(value.dtype):4} -> {str(data.dtype):4}",
                        )

                        tensor["mtype"] = csinn_mem_type_enum.CSINN_MEM_TYPE_CPU_NOT_ALIGNED.value
                        tensor["name"] = key
                        bytes_to_save = data.tobytes()
                        weight_file.write(bytes_to_save)
                        offset = data.nbytes
                        tensor["name"] = key
                        image_layers[layer_numer][key] = tensor
                        data_offset += offset
                    # image2text
                    # image2text model's weight do not quant to int
                    elif "latent_query" in key or "dense" in key or "x_attn" in key:
                        if self.fake_quantize:
                            new_dict[key] = value
                        if "latent_query" in key:
                            name = "latent_query"
                        elif "dense" in key:
                            if "weight" in key:
                                name = "dense"
                            elif "bias" in key:
                                name = "dense_b"
                        elif "x_attn.q_proj" in key:
                            if "weight" in key:
                                name = "i2t_q_proj"
                            elif "bias" in key:
                                name = "i2t_q_proj_b"
                        elif "x_attn.k_proj" in key:
                            if "weight" in key:
                                name = "i2t_k_proj"
                            elif "bias" in key:
                                name = "i2t_k_proj_b"
                        elif "x_attn.v_proj" in key:
                            if "weight" in key:
                                name = "i2t_v_proj"
                            elif "bias" in key:
                                name = "i2t_v_proj_b"
                        elif "x_attn.out_proj" in key:
                            if "weight" in key:
                                name = "i2t_out_proj"
                            elif "bias" in key:
                                name = "i2t_out_proj_b"
                        if self.ftype == "fp16":
                            data = data.astype(np.float16)
                            tensor["dtype"] = DtypeToSHLDtype["float16"]
                        else:
                            tensor["dtype"] = DtypeToSHLDtype["float32"]
                        logger.log(
                            LOG,
                            f"[{time:{3}d}/{len(self.model_dict.items())}] Quantize layer: {key:65s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(value.dtype):4} -> {str(data.dtype):4}",
                        )
                        bytes_to_save = data.tobytes()
                        weight_file.write(bytes_to_save)
                        offset = data.nbytes
                        tensor["mtype"] = csinn_mem_type_enum.CSINN_MEM_TYPE_CPU_NOT_ALIGNED.value
                        tensor["name"] = key
                        model[name] = tensor
                        data_offset += offset
                    else:
                        print("Unsupported layers")
                        print(key)

            weight_file.close()

            logger.log(LOG, "data_offset:{}".format(data_offset))
            content["config"] = {}
            if self.config.get("_name_or_path") is not None:
                del self.config["_name_or_path"]
            content["config"]["model_params"] = self.config
            content["config"]["shl_params"] = {}
            content["config"]["shl_params"]["shl_model_type"] = "weight_only"
            model["text_layer"] = text_layers
            model["image_layer"] = image_layers
            model["layers_num"] = self.config["num_layers"]
            content["model"] = model
            out_file = open(json_file_path, "w")
            json.dump(content, out_file, indent=4)
            if self.fake_quantize:
                self.model.load_state_dict(new_dict)
                torch.save(
                    self.model.state_dict(),
                    "/".join([self.save_path, "pytorch_model.fake_quant_" + self.qtype + ".bin"]),
                )

    logger.log(LOG, "Quantize model to {}".format(quantization_scheme))

    qtype = "q8_0"
    ftype = "fp32"
    if quantization_scheme in ["q8_0_fp16", "q8_0_fp32", "q4_0_fp16", "q4_0_fp32"]:
        qtype = quantization_scheme[:4]
        ftype = quantization_scheme[5:]
    else:
        logger.log(LOG, "Quantize model is not supported")
        return
    model_quantizer = Quantizer(
        model, config.to_dict(), qtype, ftype, save_dir, fake_quantize=fake_quantize
    )
    model_quantizer.quantize()
    return model_quantizer.model


class LlmRecipeConfig:
    def __init__(self, **kwargs) -> None:
        """_summary_"""
        self.unquantize_layer_type_lt = kwargs.pop("unquantize_layer_type_lt", [])
        self.unquantize_layer_name_lt = kwargs.pop("unquantize_layer_name_lt", [])
        self.q8_0_quant_type_lt = kwargs.pop("q8_0_quant_type_lt", [])
        self.q8_0_quant_name_lt = kwargs.pop("q8_0_quant_name_lt", [])
        self.nf4_0_quant_type_lt = kwargs.pop("nf4_0_quant_type_lt", [])
        self.nf4_0_quant_name_lt = kwargs.pop("nf4_0_quant_name_lt", [])
        self.q4_0_quant_type_lt = kwargs.pop("q4_0_quant_type_lt", [])
        self.q4_0_quant_name_lt = kwargs.pop("q4_0_quant_name_lt", [])
        self.q4_1_quant_type_lt = kwargs.pop("q4_1_quant_type_lt", [])
        self.q4_1_quant_name_lt = kwargs.pop("q4_1_quant_name_lt", [])
        self.q4_k_quant_type_lt = kwargs.pop("q4_k_quant_type_lt", [])
        self.q4_k_quant_name_lt = kwargs.pop("q4_k_quant_name_lt", [])
        self.q2_k_quant_type_lt = kwargs.pop("q2_k_quant_type_lt", [])
        self.q2_k_quant_name_lt = kwargs.pop("q2_k_quant_name_lt", [])

        self.quant_recipe = {
            "unquantize": {
                "type": self.unquantize_layer_type_lt,
                "name": self.unquantize_layer_name_lt,
            },
            "q8_0": {"type": self.q8_0_quant_type_lt, "name": self.q8_0_quant_name_lt},
            "nf4_0": {"type": self.nf4_0_quant_type_lt, "name": self.nf4_0_quant_name_lt},
            "q4_0": {"type": self.q4_0_quant_type_lt, "name": self.q4_0_quant_name_lt},
            "q4_1": {"type": self.q4_1_quant_type_lt, "name": self.q4_1_quant_name_lt},
            "q4_k": {"type": self.q4_k_quant_type_lt, "name": self.q4_k_quant_name_lt},
            "q2_k": {"type": self.q2_k_quant_type_lt, "name": self.q2_k_quant_name_lt},
        }

    def set_recipe_dict(self):
        return self.quant_recipe


def _create_dict_model(model, model_name, default_quant_mode, ft_dict, quant_recipe):
    for name, module in model.named_children():
        if name == "":
            continue

        cd_dict = {}
        sub_layer_name = ".".join([model_name, name])
        cd_dict["name"] = sub_layer_name

        if any(module.children()):

            for quant_name, quant_op_dict in quant_recipe.items():
                if sub_layer_name in quant_op_dict["name"] or name in quant_op_dict["type"]:
                    default_quant_mode = quant_name
                    break
            cd_dict["qtype"] = default_quant_mode
            ft_dict[name] = cd_dict
            _create_dict_model(module, sub_layer_name, default_quant_mode, cd_dict, quant_recipe)

        else:
            qtype = default_quant_mode
            for quant_name, quant_op_dict in quant_recipe.items():
                if sub_layer_name in quant_op_dict["name"] or name in quant_op_dict["type"]:
                    qtype = quant_name
                    break
            cd_dict["qtype"] = qtype
            hase_weight = False
            for param_name, param in module.named_parameters():
                sub2_layer_name = sub_layer_name + "." + param_name
                for quant_name, quant_op_dict in quant_recipe.items():
                    if (
                        sub2_layer_name in quant_op_dict["name"]
                        or param_name in quant_op_dict["type"]
                    ):
                        qtype = quant_name
                        break
                param_dict = {}
                param_dict["name"] = sub2_layer_name
                param_dict["qtype"] = qtype
                # param_dict["shape"] = param.shape
                cd_dict[param_name] = param_dict
                hase_weight = True
            if not hase_weight:
                continue
            ft_dict[name] = cd_dict
    return


def hhb_quantize_model_use_recipe(
    model, config, quant_mode, quant_recipe, save_dir="hhb_out", fake_quantize=False
):
    """_summary_

    Args:
        model (_type_): _description_
        recipe (_type_): _description_
    """

    class Quantizer:
        """_summary_"""

        def __init__(
            self, model, recipe, global_dict, config, quant_mode, save_dir, **kwargs
        ) -> None:
            self.model = model
            self.recipe = recipe
            self.global_dict = global_dict
            self.config = config
            self.qtype = quant_mode
            self.save_path = save_dir
            self.fake_quantize = kwargs.pop("fake_quantize", False)

        def quantize_dequantize_internal(self, data, qtype):
            """_summary_

            Args:
                data (torch.Tensor, numpy.ndarray): float weight
                mtype (csinn_mem_type_enum): _description_

            Returns:
                int : length of quantized weight, scale, zero_point
            """
            if isinstance(type(data), np.ndarray):
                data = data.numpy()
            dtype = DtypeToSHLDtype[str(data.dtype)]
            dim_count = data.ndim
            data_ptr = data.ctypes.data_as(ctypes.c_void_p)
            dim = np.array([data.shape[i] for i in range(dim_count)], dtype=np.int32)
            dim_ptr = dim.ctypes.data_as(ctypes.c_void_p)
            mtype = QtypeToSHLMemtype[str(qtype)]
            quantized_data = llm_quantize_block(data_ptr, dtype, dim_count, dim_ptr, mtype)
            quantized_data = np.frombuffer(quantized_data, dtype=np.uint8)
            quantized_data_ptr = quantized_data.ctypes.data_as(ctypes.c_void_p)
            dequantized_data = llm_dequantize_block(
                quantized_data_ptr,
                mtype,
                dim_count,
                dim_ptr,
                dtype,
            )
            result = np.frombuffer(dequantized_data, dtype=data.dtype).reshape(data.shape)
            return result

        def quantize_block_internal(self, weight_file, data, qtype):
            """_summary_

            Args:
                weight_file (_io.BufferedWriter): bin_file of quantized weight, scale, zero_point
                data (torch.Tensor, numpy.ndarray): float weight
                mtype (csinn_mem_type_enum): _description_

            Returns:
                int : length of quantized weight, scale, zero_point
            """
            if isinstance(type(data), np.ndarray):
                data = data.numpy()
            dtype = DtypeToSHLDtype[str(data.dtype)]
            dim_count = data.ndim
            data_ptr = data.ctypes.data_as(ctypes.c_void_p)
            dim = np.array([data.shape[i] for i in range(dim_count)], dtype=np.int32)
            dim_ptr = dim.ctypes.data_as(ctypes.c_void_p)
            mtype = QtypeToSHLMemtype[str(qtype)]
            result = llm_quantize_block(data_ptr, dtype, dim_count, dim_ptr, mtype)
            weight_file.write(result)
            return len(result)

        def quantize(self):
            if self.fake_quantize:
                new_dict = OrderedDict()
            bin_file_path = "/".join([self.save_path, "shl_llm_weight_quantize.bin"])
            json_file_path = "/".join([self.save_path, "shl_llm_weight_quantize.json"])
            data_offset = 0
            time = 0
            type_detected = False
            with open(bin_file_path, "wb") as weight_file:
                for key, value in self.model.state_dict().items():
                    time += 1
                    dims = {}
                    for i in range(value.ndim):
                        dims[str(i)] = value.shape[i]
                    if not type_detected:
                        if value.dtype != torch.float16 and value.dtype != torch.float32:
                            logger.log(
                                LOG,
                                f"HHB only support data type in ['float16','float32'], but get type {value.dtype}",
                            )
                            sys.exit(0)
                        type_detected = True
                    data = value.to("cpu").numpy()
                    data = data.astype(np.float16)

                    key_split_lt = key.split(".")
                    temp_dict = self.global_dict
                    have_saved_in_dict = True
                    for child_t in key_split_lt:
                        if temp_dict.get(child_t) is None:
                            have_saved_in_dict = False
                            break
                        else:
                            temp_dict = temp_dict[child_t]

                    if have_saved_in_dict == True:
                        if temp_dict["qtype"] != "unquantize":
                            logger.log(
                                LOG,
                                f"[{time:{3}d}/{len(self.model.state_dict().items())}] Quantize layer: {key:65s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(value.dtype):4} -> {temp_dict['qtype']}",
                            )
                            offset = self.quantize_block_internal(
                                weight_file,
                                data,
                                temp_dict["qtype"],
                            )
                            if self.fake_quantize:
                                new_dict[key] = torch.from_numpy(
                                    self.quantize_dequantize_internal(data, temp_dict["qtype"])
                                )
                            temp_dict["data_offset"] = data_offset
                            temp_dict["dim"] = dims
                            temp_dict["dtype"] = QtypeToSHLDtype[temp_dict["qtype"]]
                            temp_dict["mtype"] = QtypeToSHLMemtype[temp_dict["qtype"]]
                            temp_dict["name"] = key
                            data_offset += offset
                        else:
                            if self.fake_quantize:
                                new_dict[key] = value
                            logger.log(
                                LOG,
                                f"[{time:{3}d}/{len(self.model.state_dict().items())}] Quantize layer: {key:65s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(value.dtype):4} -> {str(value.dtype):4}",
                            )
                            temp_dict["data_offset"] = data_offset
                            temp_dict["dim"] = dims
                            temp_dict["dtype"] = DtypeToSHLDtype[str(data.dtype)]
                            temp_dict[
                                "mtype"
                            ] = csinn_mem_type_enum.CSINN_MEM_TYPE_CPU_NOT_ALIGNED.value
                            temp_dict["name"] = key
                            bytes_to_save = data.tobytes()
                            weight_file.write(bytes_to_save)
                            data_offset += data.nbytes
                    else:
                        param_dict = {}
                        sub_layer_name = ".".join([model_name, key])
                        param_dict["name"] = sub_layer_name
                        qtype = self.qtype
                        for quant_name, quant_op_dict in self.recipe.items():
                            for t in key_split_lt:
                                if (
                                    sub_layer_name in quant_op_dict["name"]
                                    or t in quant_op_dict["type"]
                                ):
                                    qtype = quant_name
                                    break
                        param_dict["qtype"] = qtype
                        param_dict["shape"] = value.shape

                        if param_dict["qtype"] != "unquantize":
                            logger.log(
                                LOG,
                                f"[{time:{3}d}/{len(self.model.state_dict().items())}] Quantize layer: {key:65s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(value.dtype):4} -> {str(param_dict['qtype']):4}",
                            )
                            offset = self.quantize_block_internal(
                                weight_file,
                                data,
                                param_dict["qtype"],
                            )
                            if self.fake_quantize:
                                new_dict[key] = torch.from_numpy(
                                    self.quantize_dequantize_internal(data, param_dict["qtype"])
                                )
                            param_dict["data_offset"] = data_offset
                            param_dict["dim"] = dims
                            param_dict["dtype"] = QtypeToSHLDtype[param_dict["qtype"]]
                            param_dict["mtype"] = QtypeToSHLMemtype[param_dict["qtype"]]
                            param_dict["name"] = key
                            data_offset += offset
                        else:
                            if self.fake_quantize:
                                new_dict[key] = value
                            logger.log(
                                LOG,
                                f"[{time:{3}d}/{len(self.model.state_dict().items())}] Quantize layer: {key:65s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(value.dtype):4} -> {str(value.dtype):4}",
                            )
                            param_dict["data_offset"] = data_offset
                            param_dict["dim"] = dims
                            param_dict["dtype"] = DtypeToSHLDtype[str(data.dtype)]
                            param_dict[
                                "mtype"
                            ] = csinn_mem_type_enum.CSINN_MEM_TYPE_CPU_NOT_ALIGNED.value
                            param_dict["name"] = key
                            bytes_to_save = data.tobytes()
                            weight_file.write(bytes_to_save)
                            offset = data.nbytes
                            data_offset += offset

                        temp_dict[key_split_lt[-1]] = param_dict

            content = {}
            content["config_dict"] = {}
            if self.config.get("_name_or_path") is not None:
                del self.config["_name_or_path"]
            content["config_dict"]["model_params"] = self.config
            content["config_dict"]["shl_params"] = {}
            content["config_dict"]["shl_params"]["shl_model_type"] = "weight_only"
            content["model_dict"] = self.global_dict
            out_file = open(json_file_path, "w")
            json.dump(content, out_file, indent=4)
            out_file.close()
            if self.fake_quantize:
                self.model.load_state_dict(new_dict)
                torch.save(
                    self.model.state_dict(),
                    "/".join([self.save_path, "pytorch_model.fake_quant_" + self.qtype + ".bin"]),
                )

    logger.log(LOG, "Quantize model to {}".format(quant_mode))

    global_dict = {}
    model_config_dict = config.to_dict()
    model_name: str = "LLM"
    if model_config_dict.get("model_type") is not None:
        model_name = model_config_dict["model_type"]
    if "q8_0" in quant_mode:
        quant_mode = "q8_0"
    elif "q4_0" in quant_mode:
        quant_mode = "q4_0"

    _create_dict_model(model, model_name, quant_mode, global_dict, quant_recipe)
    model_quantizer = Quantizer(
        model,
        quant_recipe,
        global_dict,
        config.to_dict(),
        quant_mode,
        save_dir,
        fake_quantize=fake_quantize,
    )
    model_quantizer.quantize()
    return model_quantizer.model


def hhb_quant_by_block(model, config, quantization_scheme, save_dir="hhb_out", fake_quantize=False):
    """parse llm, convert model to json

    Args:
        model (_type_): _description_
        config (_type_, optional): _description_. Defaults to None.
        quantization_scheme (str, optional): _description_. Defaults to "float32".
        save_path (str, optional): _description_. Defaults to "hhb_out".

    Returns:
        _type_: _description_
    """

    class Quantizer:
        """_summary_"""

        def __init__(self, model, config, qtype, save_path, **kwargs) -> None:
            """ """
            self.model = model
            self.config = config
            self.qtype = qtype
            self.save_path = save_path
            self.fake_quantize = kwargs.pop("fake_quantize", False)

        def quantize_dequantize_internal(self, data, qtype):
            """_summary_

            Args:
                data (torch.Tensor, numpy.ndarray): float weight
                mtype (csinn_mem_type_enum): _description_

            Returns:
                int : length of quantized weight, scale, zero_point
            """
            if isinstance(type(data), np.ndarray):
                data = data.numpy()
            dtype = DtypeToSHLDtype[str(data.dtype)]
            dim_count = data.ndim
            data_ptr = data.ctypes.data_as(ctypes.c_void_p)
            dim = np.array([data.shape[i] for i in range(dim_count)], dtype=np.int32)
            dim_ptr = dim.ctypes.data_as(ctypes.c_void_p)
            mtype = QtypeToSHLMemtype[str(qtype)]
            quantized_data = llm_quantize_block(data_ptr, dtype, dim_count, dim_ptr, mtype)
            quantized_data = np.frombuffer(quantized_data, dtype=np.uint8)
            quantized_data_ptr = quantized_data.ctypes.data_as(ctypes.c_void_p)
            dequantized_data = llm_dequantize_block(
                quantized_data_ptr,
                mtype,
                dim_count,
                dim_ptr,
                dtype,
            )
            result = np.frombuffer(dequantized_data, dtype=data.dtype).reshape(data.shape)
            return result

        def quantize_block_internal(self, weight_file, data, qtype):
            """_summary_

            Args:
                weight_file (_io.BufferedWriter): bin_file of quantized weight, scale, zero_point
                data (torch.Tensor, numpy.ndarray): float weight
                mtype (csinn_mem_type_enum): _description_

            Returns:
                int : length of quantized weight, scale, zero_point
            """
            if isinstance(type(data), np.ndarray):
                data = data.numpy()
            dtype = DtypeToSHLDtype[str(data.dtype)]
            dim_count = data.ndim
            data_ptr = data.ctypes.data_as(ctypes.c_void_p)
            dim = np.array([data.shape[i] for i in range(dim_count)], dtype=np.int32)
            dim_ptr = dim.ctypes.data_as(ctypes.c_void_p)
            mtype = QtypeToSHLMemtype[str(qtype)]
            result = llm_quantize_block(data_ptr, dtype, dim_count, dim_ptr, mtype)
            weight_file.write(result)
            return len(result)

        def quantize(self):
            if self.fake_quantize:
                new_dict = OrderedDict()
            bin_file_path = "/".join([self.save_path, "shl_llm_weight_quantize.bin"])
            json_file_path = "/".join([self.save_path, "shl_llm_weight_quantize.json"])

            data_offset = 0
            content = {}
            model = {}
            tensor_none = {}
            layers = []
            if self.config.get("num_layers") is None:
                if self.config.get("num_hidden_layers") is not None:
                    self.config["num_layers"] = self.config["num_hidden_layers"]
                else:
                    logger.error("num_layers is must")
                    sys.exit(0)
            for i in range(self.config["num_layers"]):
                layers.append(tensor_none.copy())

            type_detected = False
            time = 0
            with open(bin_file_path, "wb") as weight_file:
                for key, value in self.model.state_dict().items():
                    time += 1
                    name = unify_layer_name(key)
                    tensor = {}
                    tensor["data_offset"] = data_offset
                    dims = {}
                    for i in range(value.ndim):
                        dims[str(i)] = value.shape[i]
                    tensor["dim"] = dims
                    tensor["dim_count"] = value.ndim
                    if not type_detected:
                        if value.dtype != torch.float16 and value.dtype != torch.float32:
                            logger.log(
                                LOG,
                                f"HHB only support data type in ['float16','float32'], but get type {value.dtype}",
                            )
                            sys.exit(0)
                        type_detected = True
                    data = value.to("cpu").numpy()
                    if name in ["embd_weight", "output_layer", "pos_embd_weight"]:
                        if self.qtype in ["q8_0", "q4_0", "q4_1", "q4_k", "q2_k", "nf4_0"]:
                            logger.log(
                                LOG,
                                f"[{time:{3}d}/{len(self.model.state_dict().items())}] Quantize layer: {key:65s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(value.dtype):4} -> {str(self.qtype):4}",
                            )
                            offset = self.quantize_block_internal(
                                weight_file,
                                data,
                                self.qtype,
                            )
                            tensor["dtype"] = QtypeToSHLDtype[self.qtype]
                            tensor["mtype"] = QtypeToSHLMemtype[self.qtype]
                            if self.fake_quantize:
                                new_dict[key] = torch.from_numpy(
                                    self.quantize_dequantize_internal(data, self.qtype)
                                )
                        else:
                            logger.error("Unsupported quantization scheme")
                            sys.exit()
                        tensor["name"] = key
                        model[name] = tensor
                        data_offset += offset
                    elif name == "output_norm":
                        logger.log(
                            LOG,
                            f"[{time:{3}d}/{len(self.model.state_dict().items())}] Quantize layer: {key:65s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(value.dtype):4} -> {str(value.dtype):4}",
                        )
                        tensor["dtype"] = DtypeToSHLDtype[str(data.dtype)]
                        tensor["mtype"] = csinn_mem_type_enum.CSINN_MEM_TYPE_CPU_NOT_ALIGNED.value
                        tensor["name"] = key
                        bytes_to_save = data.tobytes()
                        weight_file.write(bytes_to_save)
                        offset = data.nbytes
                        tensor["name"] = key
                        model[name] = tensor
                        data_offset += offset
                        if self.fake_quantize:
                            new_dict[key] = value
                    elif name.isdigit():
                        if (
                            self.qtype in ["q8_0", "q4_0", "q4_1", "q4_k", "q2_k", "nf4_0"]
                            and value.ndim == 2
                        ):
                            logger.log(
                                LOG,
                                f"[{time:{3}d}/{len(self.model.state_dict().items())}] Quantize layer: {key:65s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(value.dtype):4} -> {str(self.qtype):4}",
                            )
                            offset = self.quantize_block_internal(
                                weight_file,
                                data,
                                self.qtype,
                            )
                            tensor["dtype"] = QtypeToSHLDtype[self.qtype]
                            tensor["mtype"] = QtypeToSHLMemtype[self.qtype]
                            if self.fake_quantize:
                                new_dict[key] = torch.from_numpy(
                                    self.quantize_dequantize_internal(data, self.qtype)
                                )
                        elif self.qtype in ["q8_0", "q4_0", "q4_1", "q4_k", "q2_k", "nf4_0"]:
                            logger.log(
                                LOG,
                                f"[{time:{3}d}/{len(self.model.state_dict().items())}] Quantize layer: {key:65s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(value.dtype):4} -> {str(value.dtype):4}",
                            )
                            tensor["dtype"] = DtypeToSHLDtype[str(data.dtype)]
                            tensor[
                                "mtype"
                            ] = csinn_mem_type_enum.CSINN_MEM_TYPE_CPU_NOT_ALIGNED.value
                            bytes_to_save = data.tobytes()
                            weight_file.write(bytes_to_save)
                            offset = data.nbytes
                            if self.fake_quantize:
                                new_dict[key] = value
                        else:
                            logger.error("Unsupported quantization scheme")
                            sys.exit()
                        tensor["name"] = key
                        layers[int(name)][key] = tensor
                        data_offset += offset
                    else:
                        if self.fake_quantize:
                            new_dict[key] = value
                        logger.log(LOG, name + "can not be converted.")
                        # sys.exit()

            weight_file.close()

            logger.log(LOG, "data_offset:{}".format(data_offset))
            content["config"] = {}
            if self.config.get("_name_or_path") is not None:
                del self.config["_name_or_path"]
            content["config"]["model_params"] = self.config
            content["config"]["shl_params"] = {}
            content["config"]["shl_params"]["shl_model_type"] = "weight_only"
            model["layer"] = layers
            model["layers_num"] = self.config["num_layers"]
            content["model"] = model
            out_file = open(json_file_path, "w")
            json.dump(content, out_file, indent=4)
            if self.fake_quantize:
                self.model.load_state_dict(new_dict)
                torch.save(
                    self.model.state_dict(),
                    "/".join([self.save_path, "pytorch_model.fake_quant_" + self.qtype + ".bin"]),
                )

    logger.log(LOG, "Quantize model to {}".format(quantization_scheme))
    model_quantizer = Quantizer(
        model, config.to_dict(), quantization_scheme, save_dir, fake_quantize=fake_quantize
    )
    model_quantizer.quantize()
    return model_quantizer.model

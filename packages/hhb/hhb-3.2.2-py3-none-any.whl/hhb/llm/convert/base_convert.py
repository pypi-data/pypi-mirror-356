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
import os
import sys
import json
import logging
import torch
import signal

from ..llm_util import (
    csinn_mem_type_enum,
    DtypeToSHLDtype,
    unify_layer_name,
)

from .llm_convert_for_llama2 import convert_model_llama_reference

TIME_OUT_REMOTE_CODE = 15
logger = logging.getLogger("HHB")
LOG = 25


def convert_model_with_llama(model_path, output_file) -> None:
    convert_model_llama_reference(model_path, output_file)


def convert_model_with_kosmos(model, config=None, save_dir="hhb_out"):
    """_summary_

    Args:
        model (Pytorch model): origin model.
        config (json): config json file of LLM.
        save_dir (str, optional): _description_. Defaults to "hhb_out".

    Returns:
        _type_: _description_
    """

    class ModelConverter:
        """_summary_"""

        def __init__(self, model_dict, config, save_path) -> None:
            """ """
            self.model_dict = model_dict
            self.config = config
            self.save_path = save_path

        def convert_to_json(self):
            bin_file_path = "/".join([self.save_path, "shl_llm_weight.bin"])
            json_file_path = "/".join([self.save_path, "shl_llm_weight.json"])
            content = {}
            content["config"] = {}
            if self.config.get("_name_or_path") is not None:
                del self.config["_name_or_path"]
            content["config"]["model_params"] = self.config
            content["config"]["shl_params"] = {}
            content["config"]["shl_params"]["shl_model_type"] = "weight_only"
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
            data_offset = 0

            def extract_weight(key, value, name):
                nonlocal data_offset
                data = value.float().numpy()
                tensor = {}
                tensor["data_offset"] = data_offset
                dims = {}
                for i in range(value.ndim):
                    dims[str(i)] = value.shape[i]
                tensor["dim"] = dims
                tensor["dim_count"] = value.ndim
                tensor["dtype"] = DtypeToSHLDtype[str(data.dtype)]
                tensor["mtype"] = csinn_mem_type_enum.CSINN_MEM_TYPE_CPU_NOT_ALIGNED.value
                tensor["name"] = key
                bytes_to_save = data.tobytes()
                f.write(bytes_to_save)
                data_offset += data.nbytes
                model[name] = tensor

            time = 1
            with open(bin_file_path, "wb") as f:
                for key, value in self.model_dict.items():
                    logger.log(
                        LOG,
                        f"[{time:{3}d}/{len(self.model_dict.items())}] Writing tensor: {key:65s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(value.dtype):4}",
                    )
                    time += 1
                    # text
                    if "embed_tokens" in key:
                        extract_weight(key, value, "embed_tokens")
                    elif "model.layer_norm" in key:
                        if "weight" in key:
                            extract_weight(key, value, "layer_norm")
                        elif "bias" in key:
                            extract_weight(key, value, "layer_norm_b")
                    elif "lm_head" in key:
                        extract_weight(key, value, "lm_head")
                    elif "text_model.model.layers" in key:
                        layer_numer = int(key.split(".")[3])
                        data = value.to("cpu").float().numpy()
                        tensor = {}
                        tensor["data_offset"] = data_offset
                        dims = {}
                        for i in range(value.ndim):
                            dims[str(i)] = value.shape[i]
                        tensor["dim"] = dims
                        tensor["dim_count"] = value.ndim
                        tensor["dtype"] = DtypeToSHLDtype[str(data.dtype)]
                        tensor["mtype"] = csinn_mem_type_enum.CSINN_MEM_TYPE_CPU_NOT_ALIGNED.value
                        tensor["name"] = key
                        bytes_to_save = data.tobytes()
                        f.write(bytes_to_save)
                        data_offset += data.nbytes
                        text_layers[layer_numer][key] = tensor
                    # vision
                    elif "class_embedding" in key:
                        extract_weight(key, value, "class_embedding")
                    elif "patch_embedding" in key:
                        extract_weight(key, value, "patch_embedding")
                    elif "position_embedding" in key:
                        extract_weight(key, value, "position_embedding")
                    elif "pre_layrnorm" in key:
                        if "weight" in key:
                            extract_weight(key, value, "pre_layrnorm")
                        elif "bias" in key:
                            extract_weight(key, value, "pre_layrnorm_b")
                    elif "post_layernorm" in key:
                        if "weight" in key:
                            extract_weight(key, value, "post_layernorm")
                        elif "bias" in key:
                            extract_weight(key, value, "post_layernorm_b")
                    elif "vision_model.model.encoder.layers" in key:
                        layer_numer = int(key.split(".")[4])
                        data = value.float().numpy()
                        tensor = {}
                        tensor["data_offset"] = data_offset
                        dims = {}
                        for i in range(value.ndim):
                            dims[str(i)] = value.shape[i]
                        tensor["dim"] = dims
                        tensor["dim_count"] = value.ndim
                        tensor["dtype"] = DtypeToSHLDtype[str(data.dtype)]
                        tensor["mtype"] = csinn_mem_type_enum.CSINN_MEM_TYPE_CPU_NOT_ALIGNED.value
                        tensor["name"] = key
                        bytes_to_save = data.tobytes()
                        f.write(bytes_to_save)
                        data_offset += data.nbytes
                        image_layers[layer_numer][key] = tensor
                    # image2text
                    elif "latent_query" in key:
                        extract_weight(key, value, "latent_query")
                    elif "dense" in key:
                        if "weight" in key:
                            extract_weight(key, value, "dense")
                        elif "bias" in key:
                            extract_weight(key, value, "dense_b")
                    elif "x_attn.q_proj" in key:
                        if "weight" in key:
                            extract_weight(key, value, "i2t_q_proj")
                        elif "bias" in key:
                            extract_weight(key, value, "i2t_q_proj_b")
                    elif "x_attn.k_proj" in key:
                        if "weight" in key:
                            extract_weight(key, value, "i2t_k_proj")
                        elif "bias" in key:
                            extract_weight(key, value, "i2t_k_proj_b")
                    elif "x_attn.v_proj" in key:
                        if "weight" in key:
                            extract_weight(key, value, "i2t_v_proj")
                        elif "bias" in key:
                            extract_weight(key, value, "i2t_v_proj_b")
                    elif "x_attn.out_proj" in key:
                        if "weight" in key:
                            extract_weight(key, value, "i2t_out_proj")
                        elif "bias" in key:
                            extract_weight(key, value, "i2t_out_proj_b")
                    else:
                        print("Unsupported layers")
                        print(key)
            print(data_offset)
            model["text_layer"] = text_layers
            model["image_layer"] = image_layers
            model["layers_num"] = 24
            content["model"] = model
            out_file = open(json_file_path, "w")
            json.dump(content, out_file, indent=4)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    logger.log(LOG, "Convert model to json file")
    if not isinstance(config, dict):
        config = config.to_dict()
    model_converter = ModelConverter(model.state_dict(), config, save_dir)
    model_converter.convert_to_json()
    logger.log(LOG, "Convert end...")


def convert_model_to_json(model, config=None, save_dir="hhb_out"):
    """_summary_

    Args:
        model (Pytorch model): origin model.
        config (json): config json file of LLM.
        save_dir (str, optional): _description_. Defaults to "hhb_out".

    Returns:
        _type_: _description_
    """

    class ModelConverter:
        """_summary_"""

        def __init__(self, model_dict, config, save_path) -> None:
            """ """
            self.model_dict = model_dict
            self.config = config
            self.save_path = save_path

        def convert_to_json(self):
            bin_file_path = "/".join([self.save_path, "shl_llm_weight.bin"])
            json_file_path = "/".join([self.save_path, "shl_llm_weight.json"])
            data_offset = 0
            content = {}
            model = {}
            tensor_none = {}
            layers = []
            if self.config.get("num_layers") is None:
                if self.config.get("num_hidden_layers") is not None:
                    self.config["num_layers"] = self.config["num_hidden_layers"]
                else:
                    logger.error("num_layers is required")
                    sys.exit(0)
            for i in range(self.config["num_layers"]):
                layers.append(tensor_none.copy())
            keep_bfloat16_all = None
            time = 0
            with open(bin_file_path, "wb") as weight_file:
                for key, value in self.model_dict.items():
                    name = unify_layer_name(key)
                    time += 1
                    tensor = {}
                    tensor["data_offset"] = data_offset
                    dims = {}
                    for i in range(value.ndim):
                        dims[str(i)] = value.shape[i]
                    tensor["dim"] = dims
                    tensor["dim_count"] = value.ndim

                    if value.dtype == torch.bfloat16:
                        tensor["torch_dtype"] = DtypeToSHLDtype["bfloat16"]

                        def _raise_timeout_error(signum, frame):
                            raise ValueError(
                                f"HHB will convert type of norm lyaers to float32, and convert type of decoder layers to float16"
                                f"when torch_type == torch.bfloat16\n"
                                f"please choose yes while you want to keep bfloat16 all"
                            )

                        try:
                            signal.signal(signal.SIGALRM, _raise_timeout_error)
                            signal.alarm(TIME_OUT_REMOTE_CODE)
                            while keep_bfloat16_all is None:
                                answer = input(
                                    f"HHB will convert type of norm lyaers to float32, and convert type of decoder layers to float16"
                                    f"when torch_type == torch.bfloat16\n"
                                    f"Do you wish to save weight as bf16? [y/N] "
                                )
                                if answer.lower() in ["yes", "y", "1"]:
                                    keep_bfloat16_all = True
                                elif answer.lower() in ["no", "n", "0", ""]:
                                    keep_bfloat16_all = False
                            signal.alarm(0)
                        except Exception:
                            raise ValueError(
                                f"Please choose the argument `keep_bfloat16_all` to allow custom code to be run."
                            )
                        if keep_bfloat16_all:
                            logger.log(
                                LOG,
                                f"[{time:{3}d}/{len(self.model_dict.items())}] Writing tensor: {key:70s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(value.dtype):4}",
                            )
                            tensor["dtype"] = DtypeToSHLDtype["bfloat16"]
                            data = value.to(torch.float32).to("cpu").numpy().ravel().tobytes()
                            bytes_to_save = b"".join(
                                [data[i : 2 + i] for i in range(2, len(data), 4)]
                            )
                            weight_file.write(bytes_to_save)
                            data_offset += len(bytes_to_save)
                        else:
                            if value.ndim == 2:
                                tensor["dtype"] = DtypeToSHLDtype["float16"]
                                try:
                                    data = value.to(torch.float32).half().to("cpu").numpy()
                                    logger.log(
                                        LOG,
                                        f"[{time:{3}d}/{len(self.model_dict.items())}] Writing tensor: {key:70s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(data.dtype):4}",
                                    )
                                except RuntimeWarning:
                                    data = value.to(torch.float32).to("cpu").numpy()
                                    logger.log(
                                        LOG,
                                        f"[{time:{3}d}/{len(self.model_dict.items())}] Writing tensor: {key:70s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(data.dtype):4}",
                                    )
                                bytes_to_save = data.tobytes()
                                weight_file.write(bytes_to_save)
                                data_offset += data.nbytes
                            else:
                                tensor["dtype"] = DtypeToSHLDtype["float32"]
                                data = value.to(torch.float32).to("cpu").numpy()
                                logger.log(
                                    LOG,
                                    f"[{time:{3}d}/{len(self.model_dict.items())}] Writing tensor: {key:70s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(data.dtype):4}",
                                )
                                bytes_to_save = data.tobytes()
                                weight_file.write(bytes_to_save)
                                data_offset += data.nbytes
                    else:
                        data = value.to("cpu").numpy()
                        tensor["torch_dtype"] = DtypeToSHLDtype[str(data.dtype)]
                        logger.log(
                            LOG,
                            f"[{time:{3}d}/{len(self.model_dict.items())}] Writing tensor: {key:70s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(data.dtype):4}",
                        )
                        tensor["dtype"] = DtypeToSHLDtype[str(data.dtype)]

                        bytes_to_save = data.tobytes()
                        weight_file.write(bytes_to_save)
                        data_offset += data.nbytes

                    tensor["mtype"] = csinn_mem_type_enum.CSINN_MEM_TYPE_CPU_NOT_ALIGNED.value
                    tensor["name"] = key
                    if name.isdigit():
                        layers[int(name)][key] = tensor
                    elif name:
                        model[name] = tensor

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

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    logger.log(LOG, "Convert model to json file")
    if not isinstance(config, dict):
        config = config.to_dict()
    model_converter = ModelConverter(model.state_dict(), config, save_dir)
    model_converter.convert_to_json()
    logger.log(LOG, "Convert end...")


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


def convert_model_to_hhb(model, config=None, save_dir="hhb_out"):
    """_summary_

    Args:
        model (Pytorch model): origin model.
        config (json): config json file of LLM.
        save_dir (str, optional): _description_. Defaults to "hhb_out".

    Returns:
        _type_: _description_
    """

    class ModelConverter:
        """_summary_"""

        def __init__(self, model, config, save_path, param_dict) -> None:
            """ """
            self.model_dict = model.state_dict()
            self.config = config
            self.save_path = save_path
            self.global_dict = param_dict

        def convert_to_json(self):
            bin_file_path = "/".join([self.save_path, "shl_llm_weight.bin"])
            json_file_path = "/".join([self.save_path, "shl_llm_weight.json"])
            data_offset = 0
            time = 0
            keep_bfloat16_all = None
            with open(bin_file_path, "wb") as weight_file:
                for key, value in self.model_dict.items():
                    time += 1
                    dims = {}
                    for i in range(value.ndim):
                        dims[str(i)] = value.shape[i]
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

                    if value.dtype == torch.bfloat16:
                        t_dict["torch_dtype"] = DtypeToSHLDtype["bfloat16"]

                        def _raise_timeout_error(signum, frame):
                            raise ValueError(
                                f"HHB will convert type of norm lyaers to float32, and convert type of decoder layers to float16"
                                f"when torch_type == torch.bfloat16\n"
                                f"please choose yes while you want to keep bfloat16 all"
                            )

                        try:
                            signal.signal(signal.SIGALRM, _raise_timeout_error)
                            signal.alarm(TIME_OUT_REMOTE_CODE)
                            while keep_bfloat16_all is None:
                                answer = input(
                                    f"HHB will convert type of norm lyaers to float32, and convert type of decoder layers to float16"
                                    f"when torch_type == torch.bfloat16\n"
                                    f"Do you wish to save weight as bf16? [y/N] "
                                )
                                if answer.lower() in ["yes", "y", "1"]:
                                    keep_bfloat16_all = True
                                elif answer.lower() in ["no", "n", "0", ""]:
                                    keep_bfloat16_all = False
                            signal.alarm(0)
                        except Exception:
                            raise ValueError(
                                f"Please choose the argument `keep_bfloat16_all` to allow custom code to be run."
                            )
                        if keep_bfloat16_all:
                            logger.log(
                                LOG,
                                f"[{time:{3}d}/{len(self.model_dict.items())}] Writing tensor: {key:70s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(value.dtype):4}",
                            )
                            t_dict["dtype"] = DtypeToSHLDtype["bfloat16"]
                            data = value.to(torch.float32).to("cpu").numpy().ravel().tobytes()
                            bytes_to_save = b"".join(
                                [data[i : 2 + i] for i in range(2, len(data), 4)]
                            )
                            weight_file.write(bytes_to_save)
                            data_offset += len(bytes_to_save)
                        else:
                            if value.ndim == 2:
                                t_dict["dtype"] = DtypeToSHLDtype["float16"]
                                try:
                                    data = value.to(torch.float32).half().to("cpu").numpy()
                                    logger.log(
                                        LOG,
                                        f"[{time:{3}d}/{len(self.model_dict.items())}] Writing tensor: {key:70s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(data.dtype):4}",
                                    )
                                except RuntimeWarning:
                                    data = value.to(torch.float32).to("cpu").numpy()
                                    logger.log(
                                        LOG,
                                        f"[{time:{3}d}/{len(self.model_dict.items())}] Writing tensor: {key:70s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(data.dtype):4}",
                                    )
                                bytes_to_save = data.tobytes()
                                weight_file.write(bytes_to_save)
                                data_offset += data.nbytes
                            else:
                                t_dict["dtype"] = DtypeToSHLDtype["float32"]
                                data = value.to(torch.float32).to("cpu").numpy()
                                logger.log(
                                    LOG,
                                    f"[{time:{3}d}/{len(self.model_dict.items())}] Writing tensor: {key:70s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(data.dtype):4}",
                                )
                                bytes_to_save = data.tobytes()
                                weight_file.write(bytes_to_save)
                                data_offset += data.nbytes
                    else:
                        data = value.to("cpu").numpy()
                        logger.log(
                            LOG,
                            f"[{time:{3}d}/{len(self.model_dict.items())}] Writing tensor: {key:70s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(data.dtype):4}",
                        )
                        t_dict["name"] = key
                        t_dict["data_offset"] = data_offset
                        t_dict["dim"] = dims
                        t_dict["mtype"] = csinn_mem_type_enum.CSINN_MEM_TYPE_CPU_NOT_ALIGNED.value
                        t_dict["dtype"] = DtypeToSHLDtype[str(data.dtype)]
                        bytes_to_save = data.tobytes()
                        weight_file.write(bytes_to_save)
                        data_offset += data.nbytes

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
            print(f"data_offset: {data_offset}")

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    logger.log(LOG, "Convert model to json file")
    if not isinstance(config, dict):
        config = config.to_dict()
    param_dict = {}
    _create_dict_model(model, param_dict)
    model_converter = ModelConverter(model, config, save_dir, param_dict)
    model_converter.convert_to_json()
    logger.log(LOG, "Convert end...")

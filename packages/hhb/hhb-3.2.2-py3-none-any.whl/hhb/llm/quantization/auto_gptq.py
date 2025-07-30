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
from ..llm_util import (
    csinn_mem_type_enum,
    DtypeToSHLDtype,
)

logger = logging.getLogger("HHB")
LOG = 25


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


def autogptq_quantized_convert_model_to_json(model, config=None, save_dir="hhb_out"):
    """_summary_

    Args:
        model (Pytorch model): origin model.
        config (json): config json file of LLM.
        save_dir (str, optional): _description_. Defaults to "hhb_out".

    Returns:
        _type_: _description_
    """

    """
    group_size: 128
    bits: 4
    W shape: (infeatures, outfeatures), ((4096, 4096), float16)

    quantize:
        Q shape: (infeatures, outfeatures), ((4096, 4096), int4)
        scales shape: (infeatures, outfeatures//group_size), ((4096, 32), float16)
        zeros shape: (infeatures, outfeatures//group_size), ((4096, 32), int4)

    pack:
        Q ((4096, 4096), int4) ---> pack_col(Q) ((4096, 512), int32) ---> Q.t() ((512, 4096), int32)
        scales ((4096, 32), float16) ---> scales.t() ((32, 4096), float16)
        zeros ((4096, 32), int4) ---> zeros.t() ((32, 4096), int4) ---> pack_col(zeros) ((32, 512), int32)

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
            quant_sym = (
                False
                if self.config["quantization_config"].get("sym")
                and self.config["quantization_config"]["sym"] == "false"
                else True
            )
            with open(bin_file_path, "wb") as weight_file:
                for key, value in self.model_dict.items():
                    if key.endswith("g_idx"):
                        logger.log(
                            LOG,
                            f"[{time:{3}d}/{len(self.model_dict.items())}] Jump tensor {key}",
                        )
                        time += 1
                        continue
                    if key.endswith("qzeros"):
                        if quant_sym:
                            logger.log(
                                LOG,
                                f"[{time:{3}d}/{len(self.model_dict.items())}] Jump tensor {key}",
                            )
                            time += 1
                            continue

                    time += 1
                    data = value.to("cpu").numpy()
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
                    logger.log(
                        LOG,
                        f"[{time:{3}d}/{len(self.model_dict.items())}] Writing tensor: {key:70s} | size: {' x '.join([(str(shape)) for shape in value.shape]):16} | type: {str(data.dtype):4}",
                    )
                    t_dict["name"] = key
                    t_dict["data_offset"] = data_offset
                    t_dict["dim"] = dims
                    t_dict["mtype"] = csinn_mem_type_enum.CSINN_MEM_TYPE_GPTQ.value
                    t_dict["dtype"] = DtypeToSHLDtype[str(data.dtype)]
                    bytes_to_save = data.tobytes()
                    weight_file.write(bytes_to_save)
                    data_offset += data.nbytes

            content = {}
            content["config_dict"] = {}
            if self.config.get("_name_or_path") is not None:
                del self.config["_name_or_path"]
            if self.config.get("quantization_config") is not None:
                if not isinstance(self.config["quantization_config"].get("tokenizer"), str):
                    del self.config["quantization_config"]["tokenizer"]
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


def get_samples_from_dataset(dataset, pretrained_model_dir, nsamples=128, seqlen=2048, seed=0):
    """ """
    from .get_examples import get_wikitext2, get_c4, get_c4_new, get_ptb, get_ptb_new

    StrToDataloader = {
        "wikitext": get_wikitext2,
        "c4": get_c4,
        "c4-new": get_c4_new,
        "ptb": get_ptb,
        "ptb-new": get_ptb_new,
    }
    support_dataset = ["wikitext", "c4", "c4-new", "ptb", "ptb-new"]
    for dataname in support_dataset:
        if dataname in dataset:
            examples, _ = StrToDataloader[dataname](
                dataset, nsamples, seed, seqlen, pretrained_model_dir
            )
    if examples == []:
        raise ValueError(
            f"""You have entered a string value for dataset. You can only choose between
            ['wikitext2','c4','c4-new','ptb','ptb-new'], but we found {dataset}"""
        )


def hhb_autogptq(
    pretrained_model_dir,
    quantization_config_args,
    save_dir="hhb_out",
    fake_quantize=False,
    **kwargs,
):
    """Using auto gptq to quantize the model.

    Parameters
    ----------
    pretrained_model_dir : str
        the path of LLM, Defaults to None
    quantization_config_args : str or dict
        the path of config that used in auto_gptq
    save_dir : str
        the save path of quantized model. Defaults to "hhb_out"
    fake_quantize : bool
        whether to return the fake quantized model. Defaults to False
    kwargs : dict
        the parameters of auto gptq needed in func quantize
    """

    from transformers import AutoTokenizer, AutoModelForCausalLM, GPTQConfig

    quantize_config = kwargs.pop("quantize_config", None)
    model_init_kwargs = kwargs.pop("model_init_kwargs", {})

    config_args = {}
    if isinstance(quantization_config_args, str):
        if not os.path.exists(quantization_config_args) or not quantization_config_args.endswith(
            ".json"
        ):
            logger.error("quantization config file {} is not find".format(quantization_config_args))
            sys.exit()
        with open(quantization_config_args, "r") as config_file:
            config_args = json.load(config_file)

    elif isinstance(quantization_config_args, dict):
        config_args = quantization_config_args
    else:
        raise TypeError(f"Unexpected quantize config: {quantization_config_args}")

    if not config_args.get("quantize_config"):
        raise ValueError(f"Quantization config is required")

    _quant_config_args = config_args["quantize_config"]
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_dir, trust_remote_code=True)
    if quantize_config == None:
        quantize_config = GPTQConfig(
            bits=_quant_config_args["bits"] if _quant_config_args.get("bits") else 8,
            tokenizer=tokenizer,
            dataset=_quant_config_args["dataset"] if _quant_config_args.get("dataset") else [],
            group_size=_quant_config_args["group_size"]
            if _quant_config_args.get("group_size")
            else 128,
            damp_percent=_quant_config_args["damp_percent"]
            if _quant_config_args.get("damp_percent")
            else 0.01,
            desc_act=_quant_config_args["desc_act"] == "true"
            if _quant_config_args.get("desc_act")
            else False,
            sym=_quant_config_args["sym"] == "true" if _quant_config_args.get("sym") else True,
            true_sequential=_quant_config_args["true_sequential"] == "true"
            if _quant_config_args.get("true_sequential")
            else True,
            use_cuda_fp16=_quant_config_args["use_cuda_fp16"] == "true"
            if _quant_config_args.get("use_cuda_fp16")
            else True,
            model_seqlen=_quant_config_args["model_seqlen"]
            if _quant_config_args.get("model_seqlen")
            else None,
            block_name_to_quantize=_quant_config_args["block_name_to_quantize"]
            if _quant_config_args.get("block_name_to_quantize")
            else None,
            module_name_preceding_first_block=_quant_config_args[
                "module_name_preceding_first_block"
            ]
            if _quant_config_args.get("module_name_preceding_first_block")
            else None,
            batch_size=_quant_config_args["batch_size"]
            if _quant_config_args.get("batch_size")
            else 1,
            pad_token_id=_quant_config_args["pad_token_id"]
            if _quant_config_args.get("pad_token_id")
            else None,
            use_exllama=_quant_config_args["use_exllama"]
            if _quant_config_args.get("use_exllama")
            else None,
            max_input_length=_quant_config_args["max_input_length"]
            if _quant_config_args.get("max_input_length")
            else None,
            exllama_config=_quant_config_args["exllama_config"]
            if _quant_config_args.get("exllama_config")
            else None,
            cache_block_outputs=_quant_config_args["cache_block_outputs"] == "true"
            if _quant_config_args.get("cache_block_outputs")
            else True,
            modules_in_block_to_quantize=_quant_config_args["modules_in_block_to_quantize"]
            if _quant_config_args.get("modules_in_block_to_quantize")
            else None,
            kwargs=_quant_config_args["kwargs"] if _quant_config_args.get("kwargs") else {},
        )

    if config_args.get("model_init_kwargs"):
        model_init_kwargs = config_args["model_init_kwargs"]
        if not isinstance(model_init_kwargs, dict):
            raise ValueError(f"model_init_kwargs required type is dict")

    model = AutoModelForCausalLM.from_pretrained(
        pretrained_model_dir,
        quantization_config=quantize_config,
        trust_remote_code=True,
        **model_init_kwargs,
    )

    logger.log(LOG, "Quantize with AutoGPTQ")

    if config_args.get("fake_quantize"):
        fake_quantize = config_args["fake_quantize"] == "true"

    if fake_quantize:
        import torch
        from os.path import join

        logger.log(LOG, "Save quantized model in original format")
        model_base_name = f"gptq_model-{quantize_config.bits}bit-{quantize_config.group_size}g"
        model_save_name = model_base_name + ".bin"
        torch.save(model.state_dict(), join(save_dir, model_save_name))

    logger.log(LOG, "Save quantized model in hhb_json format")
    if model.config.to_dict().get("quant_config") is None:
        model_quantized_config = model.config.to_dict()
        model_quantized_config["quantization_config"] = quantize_config.to_dict()
    autogptq_quantized_convert_model_to_json(model, model_quantized_config, save_dir)

    return model

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
""" llm import """
import os
import sys
import json
import logging

logger = logging.getLogger("HHB")
LOG = 25

BASE_QUANT_MODE: set = {
    "q8_0",
    "q4_0",
    "q4_1",
    "q4_k",
    "q2_k",
    "nf4_0",
    "q8_0_fp32",
    "q8_0_fp16",
    "q4_0_fp32",
    "q4_0_fp16",
}
ADVANCE_QUANT_MODE: set = {
    "auto_gptq",
    "smooth_quant",
    "awq",
}


def llm_import(name_or_dir, save_dir):
    """import LLM from format {float32, float16, int8, int4}

    Args:
        name_or_dir (list, str): The path of origin model.
        save_dir (str): The save path of converted model.
    """
    from ..llm.convert.base_convert import (
        convert_model_to_json,
        convert_model_with_kosmos,
        convert_model_with_llama,
        convert_model_to_hhb,
    )
    from transformers import AutoModel, AutoModelForCausalLM, AutoConfig, AutoModelForVision2Seq

    if isinstance(name_or_dir, list):
        name_or_dir = name_or_dir[0]
    if not os.path.exists(name_or_dir):
        raise ValueError(f"Path not found of model: {name_or_dir}")

    if not isinstance(save_dir, str):
        logger.warning("save_path only support type string, not {}".format(type(save_dir)))

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    try:
        config = AutoConfig.from_pretrained(name_or_dir, trust_remote_code=True)
    except OSError:
        logger.error("Model is not supported Now in HHB.")
        sys.exit(0)

    if config.to_dict().get("architectures") is not None:
        if "kosmos" in config.to_dict().get("architectures")[0].lower():
            try:
                model = AutoModelForVision2Seq.from_pretrained(name_or_dir)
            except ValueError:
                raise ("HHB error.")  # type: ignore
            convert_model_with_kosmos(model, model.config, save_dir)
            return

    try:
        model = AutoModelForCausalLM.from_pretrained(
            name_or_dir, trust_remote_code=True, torch_dtype="auto"
        )
    except ValueError:
        model = AutoModel.from_pretrained(name_or_dir, trust_remote_code=True, torch_dtype="auto")
    # convert_model_to_json(model, model.config, save_dir)
    ## to support more LM, we replace the weight convert func 'convert_model_to_json' to
    ## 'convert_model_to_hhb', this will only affect the json format.
    convert_model_to_hhb(model, model.config, save_dir)


def advanced_quantize(
    pretrained_model_dir, quant_mode, quant_config_file, save_dir, fake_quantize, **kwargs
):
    """_summary_

    Args:
        pretrained_model_dir (str): path of LLM
        qunat_config_file (str): path of quantizate config
        save_dir (str): path of output
    """
    if (
        ("llama" in pretrained_model_dir.lower()) and ("hf" not in pretrained_model_dir.lower())
    ) and (
        ("llama" in pretrained_model_dir.lower()) and ("ms" not in pretrained_model_dir.lower())
    ):
        raise AttributeError(
            "HHB advanced quantize method require the input model format is HF or MS, you can convert llama to llama-hf/llama-ms firstly, and reload."
        )
    qdq_model = None
    if quant_mode == "auto_gptq":
        from ..llm.quantization.auto_gptq import hhb_autogptq

        qdq_model = hhb_autogptq(
            pretrained_model_dir,
            quant_config_file,
            save_dir=save_dir,
            fake_quantize=fake_quantize,
            **kwargs,
        )
        return qdq_model

    elif quant_mode == "smooth_quant":
        from ..llm.quantization.smooth_quant import hhb_smoothquant

        qdq_model = hhb_smoothquant(
            pretrained_model_dir,
            quant_config_file,
            save_dir=save_dir,
            fake_quantize=fake_quantize,
            **kwargs,
        )

    elif quant_mode == "awq":
        from ..llm.quantization.awq import hhb_awq

        qdq_model = hhb_awq(
            pretrained_model_dir,
            quant_config_file,
            save_dir=save_dir,
            fake_quantize=fake_quantize,
            **kwargs,
        )

    return qdq_model


def based_quantize(
    name_or_dir, quant_mode, quant_recipe=None, save_dir="hhb_out", fake_quantize=False, **kwargs
):
    """_summary_

    Args:
        name_or_dir (str): path of LLM
        quant_mode (str): quantize mode of LLM, now only support 'q8_0, q4_0'.
        save_dir (str, optional): _description_. Defaults to "hhb_out".
    """
    from ..llm.quantization.block_quant import (
        hhb_quant_by_block,
        quantize_model_with_kosmos,
        hhb_quantize_model_use_recipe,
    )
    from ..llm.quantization.llm_quantize_for_llama2 import quantize_model_with_llama
    from transformers import AutoModel, AutoModelForCausalLM, AutoConfig, AutoModelForVision2Seq

    try:
        config = AutoConfig.from_pretrained(name_or_dir, trust_remote_code=True)
    except OSError:

        if "llama" in name_or_dir.lower():
            if quant_mode not in ["q8_0", "q4_0", "q4_1", "q4_k", "q2_k", "nf4_0"]:
                logger.log(LOG, f"Quantize model {quant_mode} is not supported with llama")
                return
            if not fake_quantize:
                quantize_model_with_llama(name_or_dir, quant_mode, save_dir)
                return None
        else:
            logger.error("Model is not supported Now in HHB.")
            sys.exit(0)

    if config.to_dict().get("architectures") is not None:
        if "llama" in config.to_dict().get("architectures")[0].lower():
            if quant_mode not in ["q8_0", "q4_0", "q4_1", "q4_k", "q2_k", "nf4_0"]:
                logger.log(LOG, f"Quantize model {quant_mode} is not supported with llama")
                return
            if not fake_quantize:
                quantize_model_with_llama(name_or_dir, quant_mode, save_dir)
                return None

        if "kosmos" in config.to_dict().get("architectures")[0].lower():
            try:
                model = AutoModelForVision2Seq.from_pretrained(name_or_dir)
            except ValueError:
                raise ("HHB error.")  # type: ignore
            if quant_mode not in ["q8_0_fp16", "q8_0_fp32", "q4_0_fp16", "q4_0_fp32"]:
                logger.log(LOG, f"Quantize model {quant_mode} is not supported with kosmos")
                return
            if quant_recipe is not None:
                if isinstance(quant_recipe, str):
                    with open(quant_recipe, "r") as file:
                        quant_recipe = json.load(file)
                    file.close()
                elif not isinstance(quant_recipe, dict):
                    logger.log(LOG, f"quantize_recipe {quant_mode} is not supported type")
                    return
                qdq_model = hhb_quantize_model_use_recipe(
                    model, model.config, quant_mode, quant_recipe, save_dir, fake_quantize
                )
            else:
                qdq_model = quantize_model_with_kosmos(
                    model, model.config, quant_mode, save_dir, fake_quantize
                )
            return qdq_model

    try:
        model = AutoModelForCausalLM.from_pretrained(
            name_or_dir, trust_remote_code=True, torch_dtype="auto"
        )
    except ValueError:
        model = AutoModel.from_pretrained(name_or_dir, trust_remote_code=True, torch_dtype="auto")

    if quant_recipe is not None:
        if isinstance(quant_recipe, str):
            with open(quant_recipe, "r") as file:
                quant_recipe = json.load(file)
        elif not isinstance(quant_recipe, dict):
            logger.log(LOG, f"quantize_recipe {quant_mode} is not supported type")
            return
        qdq_model = hhb_quantize_model_use_recipe(
            model, model.config, quant_mode, quant_recipe, save_dir, fake_quantize
        )
        return qdq_model
    else:
        qdq_model = hhb_quant_by_block(model, model.config, quant_mode, save_dir, fake_quantize)
        return qdq_model


def llm_quantize(
    name_or_dir,
    quant_mode,
    quant_config_file=None,
    quant_recipe_file=None,
    fake_quantize=False,
    save_dir="hhb_out",
    **kwargs,
):
    """_summary_

    Args:
        name_or_dir (_type_): _description_
        quant_mode (_type_): (BASE_QUANT_MODE | ADVANCE_QUANT_MODE)
        qunat_config_file (_type_, optional): _description_. Defaults to None.
        qunat_recipe_file (_type_, optional): _description_. Defaults to None.
        fake_quantize (bool, optional): _description_. Defaults to False.
        save_dir (str, optional): _description_. Defaults to "hhb_out".
    """

    if isinstance(name_or_dir, list):
        name_or_dir = name_or_dir[0]

    if not isinstance(save_dir, str):
        logger.warning("save_path only support type string, not {}".format(type(save_dir)))
    else:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

    if quant_mode in BASE_QUANT_MODE:
        qdq_model = based_quantize(
            name_or_dir, quant_mode, quant_recipe_file, save_dir, fake_quantize, **kwargs
        )
        return qdq_model

    elif quant_mode in ADVANCE_QUANT_MODE:
        qdq_model = advanced_quantize(
            name_or_dir, quant_mode, quant_config_file, save_dir, fake_quantize, **kwargs
        )
        return qdq_model
    else:
        raise ValueError(f"unsupported quantize mode.")

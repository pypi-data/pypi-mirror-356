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


def _get_awq_causal_lm_model_map():
    import awq.models as awq_models
    import hhb.llm.quantization.models as hhb_awq_models

    AWQ_CAUSAL_LM_MODEL_MAP = {
        "mpt": awq_models.MptAWQForCausalLM,
        "llama": awq_models.LlamaAWQForCausalLM,
        "opt": awq_models.OptAWQForCausalLM,
        "RefinedWeb": awq_models.FalconAWQForCausalLM,
        "RefinedWebModel": awq_models.FalconAWQForCausalLM,
        "falcon": awq_models.FalconAWQForCausalLM,
        "bloom": awq_models.BloomAWQForCausalLM,
        "gptj": awq_models.GPTJAWQForCausalLM,
        "gpt_bigcode": awq_models.GptBigCodeAWQForCausalLM,
        "mistral": awq_models.MistralAWQForCausalLM,
        "mixtral": awq_models.MixtralAWQForCausalLM,
        "gpt_neox": awq_models.GPTNeoXAWQForCausalLM,
        "aquila": awq_models.AquilaAWQForCausalLM,
        "Yi": awq_models.YiAWQForCausalLM,
        "qwen": hhb_awq_models.HHBQwenAWQForCausalLM,
        "baichuan": awq_models.BaichuanAWQForCausalLM,
        "llava": awq_models.LlavaAWQForCausalLM,
        "qwen2": hhb_awq_models.HHBQwen2AWQForCausalLM,
        "gemma": awq_models.GemmaAWQForCausalLM,
        "stablelm": awq_models.StableLmAWQForCausalLM,
        "starcoder2": awq_models.Starcoder2AWQForCausalLM,
        "chatglm": hhb_awq_models.HHBChatGLMAWQForCausalLM,
    }
    return AWQ_CAUSAL_LM_MODEL_MAP


def check_and_get_model_type(model_dir, trust_remote_code=True, **model_init_kwargs):
    from transformers import AutoConfig

    config = AutoConfig.from_pretrained(
        model_dir, trust_remote_code=trust_remote_code, **model_init_kwargs
    )
    if config.model_type not in _get_awq_causal_lm_model_map().keys():
        raise TypeError(f"{config.model_type} isn't supported yet.")
    model_type = config.model_type
    return model_type


class HHBAutoAWQForCausalLM:
    from .base import HHBBaseAWQForCausalLM

    def __init__(self):

        raise EnvironmentError(
            "You must instantiate HHBAutoAWQForCausalLM with\n"
            "HHBAutoAWQForCausalLM.from_quantized or HHBAutoAWQForCausalLM.from_pretrained"
        )

    @classmethod
    def from_pretrained(
        self,
        model_path,
        trust_remote_code=True,
        safetensors=True,
        device_map=None,
        download_kwargs=None,
        **model_init_kwargs,
    ) -> HHBBaseAWQForCausalLM:

        model_type = check_and_get_model_type(model_path, trust_remote_code, **model_init_kwargs)

        return _get_awq_causal_lm_model_map()[model_type].from_pretrained(
            model_path,
            model_type,
            trust_remote_code=trust_remote_code,
            safetensors=safetensors,
            device_map=device_map,
            download_kwargs=download_kwargs,
            **model_init_kwargs,
        )

    @classmethod
    def from_quantized(
        self,
        quant_path,
        quant_filename="",
        max_seq_len=2048,
        trust_remote_code=True,
        fuse_layers=True,
        use_exllama=False,
        use_exllama_v2=False,
        batch_size=1,
        safetensors=True,
        device_map="balanced",
        max_memory=None,
        offload_folder=None,
        download_kwargs=None,
        **config_kwargs,
    ) -> HHBBaseAWQForCausalLM:
        os.environ["AWQ_BATCH_SIZE"] = str(batch_size)
        model_type = check_and_get_model_type(quant_path, trust_remote_code)

        if config_kwargs.get("max_new_tokens") is not None:
            max_seq_len = config_kwargs["max_new_tokens"]
            logging.warning(
                "max_new_tokens argument is deprecated... gracefully "
                "setting max_seq_len=max_new_tokens."
            )

        return _get_awq_causal_lm_model_map()[model_type].from_quantized(
            quant_path,
            model_type,
            quant_filename,
            max_seq_len,
            trust_remote_code=trust_remote_code,
            fuse_layers=fuse_layers,
            use_exllama=use_exllama,
            use_exllama_v2=use_exllama_v2,
            safetensors=safetensors,
            device_map=device_map,
            max_memory=max_memory,
            offload_folder=offload_folder,
            download_kwargs=download_kwargs,
            **config_kwargs,
        )


def awq_quantized_convert_model_to_json(model, config=None, save_dir="hhb_out"):
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
            quant_asym = (
                True
                if self.config["quantization_config"].get("zero_point")
                and self.config["quantization_config"]["zero_point"] == True
                else False
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
                        if not quant_asym:
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
                    t_dict["mtype"] = csinn_mem_type_enum.CSINN_MEM_TYPE_AWQ.value
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


def hhb_awq(
    pretrained_model_dir=None,
    quant_config_file=None,
    save_dir="hhb_out",
    fake_quantize=False,
    **kwargs,
):

    from transformers import AutoTokenizer

    trust_remote_code = kwargs.pop("trust_remote_code", True)
    safetensors = kwargs.pop("safetensors", True)
    device_map = kwargs.pop("device_map", None)
    download_kwargs = kwargs.pop("download_kwargs", None)
    model_init_kwargs = kwargs.pop("model_init_kwargs", {})
    quant_config = kwargs.pop("quant_config", {})
    calib_data = kwargs.pop("calib_data", "")
    split = kwargs.pop("split", "train")
    text_column = kwargs.pop("text_column", "text")
    duo_scaling = kwargs.pop("duo_scaling", True)
    export_compatible = kwargs.pop("export_compatible", False)
    apply_clip = kwargs.pop("apply_clip", True)
    shard_size = kwargs.pop("shard_size", "5GB")

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

    if quant_args.get("trust_remote_code"):
        trust_remote_code = quant_args["trust_remote_code"]
    if quant_args.get("safetensors"):
        safetensors = quant_args["safetensors"]
    if quant_args.get("device_map"):
        device_map = quant_args["device_map"]
    if quant_args.get("download_kwargs"):
        download_kwargs = quant_args["download_kwargs"]
    if quant_args.get("model_init_kwargs"):
        model_init_kwargs = quant_args["model_init_kwargs"]
    if quant_args.get("quant_config"):
        quant_config = quant_args["quant_config"]
    if quant_args.get("split"):
        split = quant_args["split"]
    if quant_args.get("calib_data"):
        calib_data = quant_args["calib_data"]
    if quant_args.get("text_column"):
        text_column = quant_args["text_column"]
    if quant_args.get("duo_scaling"):
        duo_scaling = quant_args["duo_scaling"]
    if quant_args.get("export_compatible"):
        export_compatible = quant_args["export_compatible"]
    if quant_args.get("apply_clip"):
        apply_clip = quant_args["apply_clip"]
    if quant_args.get("shard_size"):
        shard_size = quant_args["shard_size"]

    model = HHBAutoAWQForCausalLM.from_pretrained(
        model_path=pretrained_model_dir,
        trust_remote_code=trust_remote_code,
        safetensors=safetensors,
        device_map=device_map,
        download_kwargs=download_kwargs,
        **model_init_kwargs,
    )
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_dir, trust_remote_code=True)
    model.quantize(
        tokenizer,
        quant_config=quant_config,
        calib_data=calib_data,
        split=split,
        text_column=text_column,
        duo_scaling=duo_scaling,
        export_compatible=export_compatible,
        apply_clip=apply_clip,
    )

    if fake_quantize:
        model.save_quantized(save_dir, safetensors=safetensors, shard_size=shard_size)
        tokenizer.save_pretrained(save_dir)

    if model.config.to_dict().get("quant_config") is None:
        model_quantized_config = model.config.to_dict()
        model_quantized_config["quantization_config"] = quant_config

    awq_quantized_convert_model_to_json(model, model_quantized_config, save_dir)

    return model

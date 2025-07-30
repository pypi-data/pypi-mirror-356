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
""" HHB Python API of LLM """
from .core.llm_manage import llm_import, llm_quantize


class LLM(object):
    """Object for compiling llm models into specific format."""

    def __init__(self, name_or_dir=None, save_dir="hhb_out", **kwargs) -> None:
        self.name_or_dir = name_or_dir
        self.save_dir = save_dir
        self.quant_mode = kwargs.pop("quant_mode", "unset")
        self.quant_config = kwargs.pop("quant_config", None)
        self.quant_recipe = kwargs.pop("quant_recipe", None)
        self.fake_quantize = kwargs.pop("fake_quantize", False)

    def convert(self, name_or_dir="", save_dir="hhb_out"):
        """Convert a LLM model from pytorch to bin.

        Parameters
        ----------
        name_or_dir : str or list[str]
            Path to a LLM model file.
        save_dir : str, optional
            A save path for converted model weight bin and json file
        """

        if name_or_dir == "":
            name_or_dir = self.name_or_dir
        llm_import(name_or_dir, save_dir)

    def quantize(
        self,
        name_or_dir="",
        quant_mode=None,
        quant_config=None,
        quant_recipe=None,
        fake_quantize=None,
        save_dir="",
        **kwargs,
    ):
        """Quantize a LLM model.

        Parameters
        ----------
        name_or_dir : str or list[str]
            Path to a LLM model file.
        save_dir : str, optional
            A save path for converted model weight bin and json file
        quant_mode : str
            quantize mode for LLM, it in list ["q8_0", "q4_0", "nf4_0", "q4_1", "q4_k", "q2_k", "smooth_quant", "auto_gptq"]
        qunat_config : str, optional
            A config file path for auto_gptq, the format is 'json'.
        qunat_recipe : str, optional
            A recipe file path for mix quantize, the format is 'json'.
        fake_quantize : bool, optional
            Parameter to define whether save qdq weight of LLM
        """

        if name_or_dir == "":
            name_or_dir = self.name_or_dir
        if not quant_mode:
            quant_mode = self.quant_mode
        if not quant_config:
            quant_config = self.quant_config
        if not quant_recipe:
            quant_recipe = self.quant_recipe
        if not fake_quantize:
            fake_quantize = self.fake_quantize
        if save_dir == "":
            save_dir = self.save_dir

        qdq_model = llm_quantize(
            name_or_dir, quant_mode, quant_config, quant_recipe, fake_quantize, save_dir, **kwargs
        )
        return qdq_model

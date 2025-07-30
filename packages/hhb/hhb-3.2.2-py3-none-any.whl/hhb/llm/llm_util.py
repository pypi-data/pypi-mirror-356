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
"""llm utils."""
import logging
from enum import Enum

logger = logging.getLogger("HHB")
LOG = 25


class csinn_dtype_enum(Enum):
    CSINN_DTYPE_BOOL = 0  # < Boolean
    CSINN_DTYPE_INT4 = 1  # < Signed 4 bit fixed-point
    CSINN_DTYPE_UINT8 = 2  # < Unsigned 8 bit fixed-point
    CSINN_DTYPE_INT8 = 3  # < Signed 8 bit fixed-point
    CSINN_DTYPE_UINT16 = 4  # < Unsigned 16 bit fixed-point
    CSINN_DTYPE_INT16 = 5  # < Signed 16 bit fixed-point
    CSINN_DTYPE_UINT32 = 6  # < Unsigned 32 bit fixed-point
    CSINN_DTYPE_INT32 = 7  # < Signed 32 bit fixed-point
    CSINN_DTYPE_FLOAT16 = 8  # < Half-precision floating-point
    CSINN_DTYPE_BFLOAT16 = 9  # < Brain floating-point
    CSINN_DTYPE_FLOAT32 = 10  # < Single-precision floating-point
    CSINN_DTYPE_FLOAT64 = 11  # < Double-precision floating-point
    CSINN_DTYPE_INT64 = 12  # < Signed 64 bit fixed-point
    CSINN_DTYPE_SIZE = 13


#  CSI-NN data memory type
class csinn_mem_type_enum(Enum):
    CSINN_MEM_TYPE_CPU_NOT_ALIGNED = 0  # < Default storage
    CSINN_MEM_TYPE_CPU_ALIGNED = 1  # < Aligned storage
    CSINN_MEM_TYPE_DMABUF = 2  # < DMA buf
    CSINN_MEM_TYPE_ASP42 = 3  # < Structed sparsity 4:2
    CSINN_MEM_TYPE_ASP41 = 4  # < Structed sparsity 4:1
    # < Accelerator driver or others alloced CPU memory
    CSINN_MEM_TYPE_CPU_ACC = 5
    CSINN_MEM_TYPE_BLOCK_Q2_K = 6  # < Block quantization from llama.cpp
    CSINN_MEM_TYPE_BLOCK_Q4_0 = 7  # < Block quantization from llama.cpp
    CSINN_MEM_TYPE_BLOCK_Q8_0 = 8  # < Block quantization from llama.cpp
    CSINN_MEM_TYPE_BLOCK_Q8_0_REARRANGE = 9
    CSINN_MEM_TYPE_BLOCK_Q4_0_REARRANGE = 10
    CSINN_MEM_TYPE_BLOCK_Q4_1 = 11  # < Block quantization from llama.cpp
    CSINN_MEM_TYPE_BLOCK_Q4_K = 12  # < Block quantization from llama.cpp
    CSINN_MEM_TYPE_BLOCK_NF4_0 = 13  # < Block quantization from llama.cpp
    CSINN_MEM_TYPE_GPTQ = 14  # < Block quantization from llama.cpp
    CSINN_MEM_TYPE_SQ = 15
    CSINN_MEM_TYPE_AWQ = 16


DtypeToSHLDtype = {
    "int4": csinn_dtype_enum.CSINN_DTYPE_INT4.value,
    "int8": csinn_dtype_enum.CSINN_DTYPE_INT8.value,
    "uint16": csinn_dtype_enum.CSINN_DTYPE_UINT16.value,
    "int16": csinn_dtype_enum.CSINN_DTYPE_INT16.value,
    "uint32": csinn_dtype_enum.CSINN_DTYPE_UINT32.value,
    "int32": csinn_dtype_enum.CSINN_DTYPE_INT32.value,
    "float16": csinn_dtype_enum.CSINN_DTYPE_FLOAT16.value,
    "bfloat16": csinn_dtype_enum.CSINN_DTYPE_BFLOAT16.value,
    "float32": csinn_dtype_enum.CSINN_DTYPE_FLOAT32.value,
    "int64": csinn_dtype_enum.CSINN_DTYPE_INT64.value,
}


QtypeToSHLMemtype = {
    "q8_0": csinn_mem_type_enum.CSINN_MEM_TYPE_BLOCK_Q8_0.value,
    "q4_0": csinn_mem_type_enum.CSINN_MEM_TYPE_BLOCK_Q4_0.value,
    "q4_1": csinn_mem_type_enum.CSINN_MEM_TYPE_BLOCK_Q4_1.value,
    "q4_k": csinn_mem_type_enum.CSINN_MEM_TYPE_BLOCK_Q4_K.value,
    "q2_k": csinn_mem_type_enum.CSINN_MEM_TYPE_BLOCK_Q2_K.value,
    "nf4_0": csinn_mem_type_enum.CSINN_MEM_TYPE_BLOCK_NF4_0.value,
    "cpu_not_aligned": csinn_mem_type_enum.CSINN_MEM_TYPE_CPU_NOT_ALIGNED.value,
    "auto_gptq": csinn_mem_type_enum.CSINN_MEM_TYPE_GPTQ.value,
    "smooth_quant": csinn_mem_type_enum.CSINN_MEM_TYPE_SQ.value,
}

QtypeToSHLDtype = {
    "q8_0": csinn_dtype_enum.CSINN_DTYPE_INT8.value,
    "q4_0": csinn_dtype_enum.CSINN_DTYPE_INT4.value,
    "q4_1": csinn_dtype_enum.CSINN_DTYPE_INT4.value,
    "q4_k": csinn_dtype_enum.CSINN_DTYPE_INT4.value,
    "q2_k": csinn_dtype_enum.CSINN_DTYPE_UINT8.value,
    "nf4_0": csinn_dtype_enum.CSINN_DTYPE_INT4.value,
}


def unify_layer_name(layer_name):

    """
    Supported model: chatglm, llama2, Qwen

    """
    LayerNameToUnify = {
        "embd_weight": ["embedding", "embed_tokens", "wte"],
        "pos_embd_weight": [
            "rotary_pos_emb",
        ],
        "output_norm": ["final_layernorm", "model.norm", "ln_f"],
        "output_layer": ["output_layer", "lm_head", "lm_head"],
    }
    for key, val in LayerNameToUnify.items():
        for name in val:
            if name in layer_name:
                logger.log(LOG, f"Rename layer: {layer_name:65s} ->| {key}")
                return key
    layer_numer = layer_name.split(".")
    for d in layer_numer:
        if d.isdigit():
            return d
    return layer_name

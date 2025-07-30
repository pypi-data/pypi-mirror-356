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
"""A schedule rule for thead"""

from tvm import dlight as dl


vector_schedule = dl.ApplyDefaultSchedule(  # pylint: disable=not-callable
    dl.riscv.Arithmetic(),
    dl.riscv.Memcpy_Ops(),
    dl.riscv.Global_MaxPool(),
    dl.riscv.Global_AvgPool(),
    dl.riscv.Sqrt(),
    dl.riscv.Transpose(),
    dl.riscv.AvgPool(),
    dl.riscv.MaxPool(),
    dl.riscv.Relu(),
    dl.riscv.Gemm(),
    dl.riscv.Softmax(),
    dl.riscv.Conv2d(),
    dl.riscv.Erf(),
    dl.riscv.Mean(),
    dl.riscv.Concat(),
    dl.riscv.Cast(),
    dl.riscv.Leaky_Relu(),
    dl.riscv.LayerNorm(),
    dl.riscv.Sigmoid(),
)

matrix_schedule = dl.ApplyDefaultSchedule(  # pylint: disable=not-callable
    dl.riscv.MatmulMatrix(),
    dl.riscv.Conv2dMatrix(),
    dl.riscv.Arithmetic(),
    dl.riscv.Memcpy_Ops(),
    dl.riscv.Global_MaxPool(),
    dl.riscv.Global_AvgPool(),
    dl.riscv.Sqrt(),
    dl.riscv.Transpose(),
    dl.riscv.AvgPool(),
    dl.riscv.MaxPool(),
    dl.riscv.Relu(),
    dl.riscv.Softmax(),
    dl.riscv.Erf(),
    dl.riscv.Mean(),
    dl.riscv.Concat(),
    # dl.riscv.Cast(),
    dl.riscv.Leaky_Relu(),
    dl.riscv.LayerNorm(),
    dl.riscv.Sigmoid(),
)


def get_board_schedule(cpu_type):
    """get schedule for cpu"""

    if cpu_type in ["c907fdvm"]:
        return matrix_schedule
    elif cpu_type in ["c920", "c908v"]:
        return vector_schedule
    else:
        assert False, "AOT mode unsupported cpu type: {}".format(cpu_type)

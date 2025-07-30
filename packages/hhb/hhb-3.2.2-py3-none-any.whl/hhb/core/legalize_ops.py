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
"""Manage legalize ops for thead."""

import tvm
from typing import Any
from tvm import relax, te, tir
from tvm import topi
import tvm.relay
from tvm.topi.riscv.conv2d_gemm import conv2d_gemm
from tvm.topi.riscv.conv2d_gemm_vector import (
    conv2d_gemm_vector,
    conv2d_winograd_vector,
    conv2d_gemm_1x1,
)
from tvm.topi.riscv.softmax import fast_softmax
from tvm.topi.riscv.dense import matmul as rv_matmul
from tvm.relax.transform import LegalizeOps
from tvm.relax.transform.legalize_ops.common import _try_convert_to_scalar_const
from tvm.relax.expr import Expr


def legalize_conv2d_matrix(bb: relax.BlockBuilder, args, attrs) -> relax.Expr:
    return bb.call_te(
        conv2d_gemm,
        args[0],
        args[1],
        attrs.strides,
        attrs.padding,
        attrs.dilation,
        attrs.groups,
        attrs.data_layout,
        attrs.out_dtype,
        True,
    )


class LegalizeOpsMatrix:
    def __init__(self):
        self.op_legalize_map = {"relax.nn.conv2d": legalize_conv2d_matrix}

    def __call__(self, mod):
        return LegalizeOps(self.op_legalize_map)(mod)


def legalize_conv2d_vector(bb: relax.BlockBuilder, call: relax.Call) -> relax.Expr:
    return bb.call_te(
        conv2d_gemm_vector,
        call.args[0],
        call.args[1],
        call.attrs.strides,
        call.attrs.padding,
        call.attrs.dilation,
        call.attrs.groups,
        call.attrs.data_layout,
        call.attrs.out_dtype,
    )


def translate_conv_winograd(bb: relax.BlockBuilder, new_args, attrs) -> relax.Expr:
    return bb.call_te(
        conv2d_winograd_vector,
        new_args[0],
        new_args[1],
        attrs["strides"],
        attrs["padding"],
        attrs["dilation"],
        attrs["out_dtype"],
        4,
        True,
    )


def translate_conv_without_weight_transform(bb: relax.BlockBuilder, new_args, attrs) -> relax.Expr:
    return bb.call_te(
        conv2d_gemm_1x1,
        new_args[0],
        new_args[1],
        attrs["strides"],
        attrs["padding"],
        attrs["dilation"],
        pre_compute=True,
        out_channel=attrs.get_int("channels"),
    )


def translate_conv_without_weight_transform_matrix(
    bb: relax.BlockBuilder, new_args, attrs
) -> relax.Expr:
    return bb.call_te(
        conv2d_gemm,
        new_args[0],
        new_args[1],
        attrs.strides,
        attrs.padding,
        attrs.dilation,
        attrs.groups,
        attrs.data_layout,
        attrs.out_dtype,
        True,
    )


def translate_conv(bb: relax.BlockBuilder, new_args, attrs) -> relax.Expr:
    return bb.call_te(
        conv2d_gemm_vector,
        new_args[0],
        new_args[1],
        attrs["strides"],
        attrs["padding"],
        attrs["dilation"],
        attrs["groups"],
        attrs["data_layout"],
        attrs["out_dtype"],
    )


def translate_fast_softmax(bb: relax.BlockBuilder, new_args, attrs) -> relax.Expr:
    return bb.call_te(
        fast_softmax,
        new_args[0],
        attrs["axis"],
    )


def translate_fast_sigmoid(bb: relax.BlockBuilder, new_args, attrs) -> relax.Expr:
    return bb.call_te(
        topi.fast_sigmoid,
        new_args[0],
    )


def translate_fast_exp(bb: relax.BlockBuilder, new_args, attrs) -> relax.Expr:
    return bb.call_te(
        topi.fast_exp,
        new_args[0],
    )


def translate_fast_erf(bb: relax.BlockBuilder, new_args, attrs) -> relax.Expr:
    return bb.call_te(
        topi.fast_erf,
        new_args[0],
    )


def translate_fast_tanh(bb: relax.BlockBuilder, new_args, attrs) -> relax.Expr:
    return bb.call_te(
        topi.fast_tanh,
        new_args[0],
    )


def translate_concatenate(bb: relax.BlockBuilder, new_args, attrs) -> relax.Expr:
    return bb.call_te(
        topi.concatenate,
        new_args,
        attrs["axis"],
    )


def translate_batch_matmul(bb: relax.BlockBuilder, new_args, attrs) -> relax.Expr:
    def te_matmul(a: te.Tensor, b: te.Tensor) -> te.Tensor:
        a_shape = list(a.shape)
        b_shape = list(b.shape)
        a_prepended = False
        b_appended = False
        if len(a_shape) == 1:
            a_prepended = True
            a_shape.insert(0, 1)
        if len(b_shape) == 1:
            b_appended = True
            b_shape.append(1)

        is_a_larger = len(a_shape) > len(b_shape)
        offset = len(a_shape) - len(b_shape) if is_a_larger else len(b_shape) - len(a_shape)

        a_relax = relax.Var("a", relax.TensorStructInfo(a.shape))
        b_relax = relax.Var("b", relax.TensorStructInfo(b.shape))
        output_shape = (
            tvm.ir.Op.get("relax.matmul")
            .get_attr("FInferStructInfo")(relax.op.matmul(a_relax, b_relax), bb)
            .shape
        )

        def matmul_compute(*idx_spatial):
            k = te.reduce_axis((0, a_shape[-1]), name="k")

            def multiply_compute(idx_reduce):
                a_indices = []
                b_indices = []

                for i in range(offset):
                    if is_a_larger:
                        a_indices.append(idx_spatial[i])
                    else:
                        b_indices.append(idx_spatial[i])
                for i in range(offset, len(output_shape) - (2 - a_prepended - b_appended)):
                    a_dim = a_shape[i if is_a_larger else i - offset]
                    b_dim = b_shape[i if not is_a_larger else i - offset]
                    dim_equal = a_dim == b_dim
                    if not isinstance(dim_equal, tir.IntImm) or dim_equal == 0:
                        a_dim_is_one = isinstance(a_dim, tir.IntImm) and a_dim == 1
                        b_dim_is_one = isinstance(b_dim, tir.IntImm) and b_dim == 1
                        a_indices.append(0 if a_dim_is_one else idx_spatial[i])
                        b_indices.append(0 if b_dim_is_one else idx_spatial[i])
                    else:
                        a_indices.append(idx_spatial[i])
                        b_indices.append(idx_spatial[i])

                if not a_prepended:
                    a_indices.append(idx_spatial[-2 + b_appended])
                a_indices.append(idx_reduce)
                b_indices.append(idx_reduce)
                if not b_appended:
                    b_indices.append(idx_spatial[-1])

                dtype = attrs["out_dtype"]
                if dtype != "":
                    return a(*a_indices).astype(dtype) * b(*b_indices).astype(dtype)
                return a(*a_indices) * b(*b_indices)

            return te.sum(multiply_compute(k), axis=k)

        return te.compute(
            output_shape,
            lambda *idx: matmul_compute(*idx),  # pylint: disable=unnecessary-lambda
            name="matmul",
        )

    lhs, rhs = new_args
    lhs_sinfo = lhs.struct_info
    rhs_sinfo = rhs.struct_info
    assert lhs_sinfo.dtype and rhs_sinfo.dtype, "The dtype of both operands must be known."
    return bb.call_te(te_matmul, lhs, rhs, primfunc_name_hint="matmul")


def translate_dense(bb: relax.BlockBuilder, new_args, attrs) -> relax.Expr:
    lhs, rhs = new_args
    out_dtype = attrs["out_dtype"]
    if not out_dtype:
        out_dtype = "float32"
    return bb.call_te(rv_matmul, lhs, rhs, None, out_dtype, False, True, primfunc_name_hint="dense")


def translate_adaptive_avg_pool1d(bb: relax.BlockBuilder, new_args, attrs) -> relax.Expr:
    return bb.call_te(
        topi.nn.adaptive_pool1d,
        new_args[0],
        attrs.output_size,
        "avg",
        attrs.layout,
    )


def translate_power(bb: relax.BlockBuilder, new_args, attrs) -> relax.Expr:
    # To simplify the created PrimFunc, we first check if arg1 is a constant scalar.
    # If it is not, we then check if arg0 is a constant scalar.
    arg0 = new_args[0]
    arg1 = _try_convert_to_scalar_const(new_args[1])
    if isinstance(arg1, Expr):  # type: ignore
        arg0 = _try_convert_to_scalar_const(arg0)
    return bb.call_te(
        topi.power,
        arg0,
        arg1,
    )


def translate_layer_norm(bb: relax.BlockBuilder, new_args, attrs) -> relax.Expr:
    axis = attrs["axis"]
    if isinstance(axis, int):
        axis = [axis]
    return bb.call_te(
        topi.nn.layer_norm,
        new_args[0],
        new_args[1],
        new_args[2],
        axis,
        attrs["epsilon"],
    )


def get_relay_to_tir_table(target):
    if target == "c907":
        table = {
            "nn.softmax": translate_fast_softmax,
            "sigmoid": translate_fast_sigmoid,
            "exp": translate_fast_exp,
            "erf": translate_fast_erf,
            "tanh": translate_fast_tanh,
            "concatenate": translate_concatenate,
            "nn.batch_matmul": translate_batch_matmul,
            "nn.dense": translate_dense,
            "nn.conv2d": legalize_conv2d_matrix,
            "nn.adaptive_avg_pool1d": translate_adaptive_avg_pool1d,
            "power": translate_power,
            "nn.layer_norm": translate_layer_norm,
        }
    else:
        table = {
            "nn.contrib_conv2d_winograd_without_weight_transform": translate_conv_winograd,
            "nn.contrib_conv2d_gemm_without_weight_transform": translate_conv_without_weight_transform,
            "nn.softmax": translate_fast_softmax,
            "sigmoid": translate_fast_sigmoid,
            "exp": translate_fast_exp,
            "erf": translate_fast_erf,
            "tanh": translate_fast_tanh,
            "concatenate": translate_concatenate,
            "nn.batch_matmul": translate_batch_matmul,
            "nn.dense": translate_dense,
            "nn.conv2d": translate_conv,
            "nn.adaptive_avg_pool1d": translate_adaptive_avg_pool1d,
            "power": translate_power,
            "nn.layer_norm": translate_layer_norm,
        }
    return table


class LegalizeOpsVector:
    def __init__(self):
        self.op_legalize_map = {"relax.nn.conv2d": legalize_conv2d_vector}

    def __call__(self, mod):
        return LegalizeOps(self.op_legalize_map)(mod)

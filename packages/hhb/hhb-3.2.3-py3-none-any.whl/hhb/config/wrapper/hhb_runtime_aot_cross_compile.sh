#!/bin/bash
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

riscv64-unknown-linux-gnu-g++  \
    -std=c++17 -O2 -g -mabi=lp64d -mrvv-v0p10-compatible \
    -mcpu=#_hhb_target_mcpu_# \
    -I#_hhb_tvm_inc_# \
    -I#_hhb_dmlc_inc_# \
    -I#_hhb_dlpack_inc_# \
    -I#_hhb_cmd_parse_inc_# \
    -I#_hhb_x86_inc_backend_# \
    -I#_hhb_x86_inc_csinn_# \
    -I#_hhb_x86_inc_graph_# \
    -I#_hhb_x86_inc_# \
    -DDMLC_USE_LOGGING_LIBRARY=\<tvm/runtime/logging.h\> \
    ./hhb_runtime_device_aot.cc -c -o ./runtime.o \

riscv64-unknown-linux-gnu-gcc  \
    ./runtime.o -o ./deploy \
    -Wl,--gc-sections  -O2 -g -mabi=lp64d  \
    -L#_hhb_decode_lib_# \
    -L#_hhb_runtime_lib_# \
    -L#_hhb_shl_##_hhb_target_cpu_#/lib \
    -lshl -lprebuilt_runtime -ljpeg -lpng -lz -lstdc++ -lm \
    -L. -ltvm_runtime -ldl -lpthread

rm runtime.o
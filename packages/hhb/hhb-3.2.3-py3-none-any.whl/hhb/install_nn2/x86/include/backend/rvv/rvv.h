/*
 * Copyright (C) 2016-2024 T-Head Semiconductor Co., Ltd. All rights reserved.
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Licensed under the Apache License, Version 2.0 (the License); you may
 * not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an AS IS BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef INCLUDE_SHL_RVV_H_
#define INCLUDE_SHL_RVV_H_

#if __riscv_vector
#include <riscv_vector.h>

#if (__riscv_v == 1000000)
#define RVV_1_0_0
#elif (__riscv_v == 7000)
#define RVV_0_7_1
#endif

#ifdef __riscv_xtheadvdot
#ifndef SHL_DISABLE_VDOT
#define XTHEADVDOT
#define SHL_USE_DOT_INT8  // default: support int8 dot
// #define SHL_USE_DOT_INT4     // easter eggs
#endif  // SHL_DISABLE_VDOT
#endif  // __riscv_xtheadvdot

#endif  // __riscv_vector

#include "csi_nn.h"
#include "reference/ref.h"
#include "shl_gref.h"

#ifdef __cplusplus
extern "C" {
#endif

/********************************** initialization ******************************/
int shl_rvv_conv2d_init_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_tensor *kernel, struct csinn_tensor *bias,
                             struct csinn_conv2d_params *params);
int shl_rvv_conv2d_init_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_tensor *kernel, struct csinn_tensor *bias,
                             struct csinn_conv2d_params *params);
int shl_rvv_conv2d_init_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_tensor *kernel, struct csinn_tensor *bias,
                             struct csinn_conv2d_params *params);

int shl_rvv_conv1d_init_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_tensor *kernel, struct csinn_tensor *bias,
                             struct csinn_conv1d_params *params);
int shl_rvv_conv1d_init_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_tensor *kernel, struct csinn_tensor *bias,
                             struct csinn_conv1d_params *params);
int shl_rvv_conv1d_init_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_tensor *kernel, struct csinn_tensor *bias,
                             struct csinn_conv1d_params *params);

int shl_rvv_depthwise_conv2d_init_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                       struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                       struct csinn_conv2d_params *params);
int shl_rvv_depthwise_conv2d_init_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                       struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                       struct csinn_conv2d_params *params);
int shl_rvv_depthwise_conv2d_init_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                       struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                       struct csinn_conv2d_params *params);
int shl_rvv_depthwise_conv2d_init_int4(struct csinn_tensor *input, struct csinn_tensor *output,
                                       struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                       struct csinn_conv2d_params *params);

int shl_rvv_deconv2d_init_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                               struct csinn_tensor *kernel, struct csinn_tensor *bias,
                               struct csinn_conv2d_params *params);
int shl_rvv_deconv2d_init_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                               struct csinn_tensor *kernel, struct csinn_tensor *bias,
                               struct csinn_conv2d_params *params);

int shl_rvv_avgpool2d_init_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                struct csinn_pool_params *params);
int shl_rvv_avgpool2d_init_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                struct csinn_pool_params *params);
int shl_rvv_avgpool2d_init_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                struct csinn_pool_params *params);
int shl_rvv_global_avgpool2d_init_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                       struct csinn_pool_params *params);
int shl_rvv_global_avgpool2d_init_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                       struct csinn_pool_params *params);
int shl_rvv_global_avgpool2d_init_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                       struct csinn_pool_params *params);

int shl_rvv_maxpool2d_init_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                struct csinn_pool_params *params);
int shl_rvv_maxpool2d_init_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                struct csinn_pool_params *params);
int shl_rvv_maxpool2d_init_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                struct csinn_pool_params *params);

int shl_rvv_global_maxpool2d_init_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                       struct csinn_pool_params *params);
int shl_rvv_global_maxpool2d_init_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                       struct csinn_pool_params *params);
int shl_rvv_global_maxpool2d_init_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                       struct csinn_pool_params *params);

int shl_rvv_fullyconnected_init_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                     struct csinn_tensor *weights, struct csinn_tensor *bias,
                                     struct csinn_fc_params *params);

int shl_rvv_fullyconnected_init_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                     struct csinn_tensor *weights, struct csinn_tensor *bias,
                                     struct csinn_fc_params *params);

int shl_rvv_fullyconnected_init_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                     struct csinn_tensor *weights, struct csinn_tensor *bias,
                                     struct csinn_fc_params *params);

int shl_rvv_data_convert_init(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_siso_params *params);

int shl_rvv_matmul_init_fp32(struct csinn_tensor *mat0, struct csinn_tensor *mat1,
                             struct csinn_tensor *output, struct csinn_matmul_params *params);
int shl_rvv_matmul_init_fp16(struct csinn_tensor *mat0, struct csinn_tensor *mat1,
                             struct csinn_tensor *output, struct csinn_matmul_params *params);
int shl_rvv_matmul_init_int8(struct csinn_tensor *mat0, struct csinn_tensor *mat1,
                             struct csinn_tensor *output, struct csinn_matmul_params *params);

/************************************ convolution *********************************/
/********************************* common im2col+gemm *****************************/
int shl_rvv_common_conv_gemm_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                  struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                  struct csinn_conv2d_params *params,
                                  void (*reorder_input)(float *, float *, int, int, int),
                                  void (*gemm)(float *, const float *, const float *, float *, int,
                                               int, int, int));
int shl_rvv_common_conv_gemm_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                  struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                  struct csinn_conv2d_params *params,
                                  void (*reorder_input)(__fp16 *, __fp16 *, int, int, int),
                                  void (*gemm)(__fp16 *, const __fp16 *, const __fp16 *, __fp16 *,
                                               int, int, int, int));
int shl_rvv_common_conv_gemm_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                  struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                  struct csinn_conv2d_params *params,
                                  void (*reorder_input)(int8_t *, int8_t *, int, int, int),
                                  void (*gemm)(int8_t *, const int8_t *, const int8_t *, int32_t *,
                                               int, int, int, int, int32_t, int32_t *, int32_t *));

int shl_rvv_common_conv_gemm_packn_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                        struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                        struct csinn_conv2d_params *params,
                                        void (*reorder_input)(float *, float *, int, int, int),
                                        void (*gemm)(float *, const float *, const float *, float *,
                                                     int, int, int, bool));
int shl_rvv_common_conv_gemm_packn_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                        struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                        struct csinn_conv2d_params *params,
                                        void (*reorder_input)(__fp16 *, __fp16 *, int, int, int),
                                        void (*gemm)(__fp16 *, const __fp16 *, const __fp16 *,
                                                     __fp16 *, int, int, int, bool));
int shl_rvv_common_conv_gemm_packn_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                        struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                        struct csinn_conv2d_params *params,
                                        void (*reorder_input)(int8_t *, int8_t *, int, int, int),
                                        void (*gemm)(int8_t *, const int8_t *, const int8_t *,
                                                     int32_t *, int, int, int, int32_t, int32_t *,
                                                     int32_t *));

int shl_rvv_common_conv_gemm_pack1ton_fp32(
    struct csinn_tensor *input, struct csinn_tensor *output, struct csinn_tensor *kernel,
    struct csinn_tensor *bias, struct csinn_conv2d_params *params,
    void (*reorder_input)(float *, float *, int, int, int, int),
    void (*gemm)(float *, const float *, const float *, float *, int, int, int, bool));
int shl_rvv_common_conv_gemm_pack1ton_fp16(
    struct csinn_tensor *input, struct csinn_tensor *output, struct csinn_tensor *kernel,
    struct csinn_tensor *bias, struct csinn_conv2d_params *params,
    void (*reorder_input)(__fp16 *, __fp16 *, int, int, int, int),
    void (*gemm)(__fp16 *, const __fp16 *, const __fp16 *, __fp16 *, int, int, int, bool));
int shl_rvv_common_conv_gemm_pack1ton_int8(
    struct csinn_tensor *input, struct csinn_tensor *output, struct csinn_tensor *kernel,
    struct csinn_tensor *bias, struct csinn_conv2d_params *params,
    void (*reorder_input)(int8_t *, int8_t *, int, int, int, int),
    void (*gemm)(int8_t *, const int8_t *, const int8_t *, int32_t *, int, int, int, int32_t,
                 int32_t *, int32_t *));

int shl_rvv_common_conv_gemm_packnto1_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                           struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                           struct csinn_conv2d_params *params,
                                           void (*reorder_input)(float *, float *, int, int, int),
                                           void (*gemm)(float *, const float *, const float *,
                                                        float *, int, int, int, bool));
int shl_rvv_common_conv_gemm_packnto1_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                           struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                           struct csinn_conv2d_params *params,
                                           void (*reorder_input)(__fp16 *, __fp16 *, int, int, int),
                                           void (*gemm)(__fp16 *, const __fp16 *, const __fp16 *,
                                                        __fp16 *, int, int, int, bool));
int shl_rvv_common_conv_gemm_packnto1_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                           struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                           struct csinn_conv2d_params *params,
                                           void (*reorder_input)(int8_t *, int8_t *, int, int, int),
                                           void (*gemm)(int8_t *, const int8_t *, const int8_t *,
                                                        int32_t *, int, int, int, int32_t,
                                                        int32_t *, int32_t *));

int shl_rvv_common_conv1x1_gemm_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                     struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                     struct csinn_conv2d_params *params,
                                     void (*reorder_input)(float *, float *, int, int, int),
                                     void (*gemm)(float *, const float *, const float *, float *,
                                                  int, int, int, int));
int shl_rvv_common_conv1x1_gemm_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                     struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                     struct csinn_conv2d_params *params,
                                     void (*reorder_input)(__fp16 *, __fp16 *, int, int, int),
                                     void (*gemm)(__fp16 *, const __fp16 *, const __fp16 *,
                                                  __fp16 *, int, int, int, int));
int shl_rvv_common_conv1x1_gemm_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                     struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                     struct csinn_conv2d_params *params,
                                     void (*reorder_input)(int8_t *, int8_t *, int, int, int),
                                     void (*gemm)(int8_t *, const int8_t *, const int8_t *,
                                                  int32_t *, int, int, int, int, int32_t, int32_t *,
                                                  int32_t *));

int shl_rvv_common_conv1x1_gemm_packn_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                           struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                           struct csinn_conv2d_params *params,
                                           void (*reorder_input)(float *, float *, int, int, int),
                                           void (*gemm)(float *, const float *, const float *,
                                                        float *, int, int, int, bool));
int shl_rvv_common_conv1x1_gemm_packn_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                           struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                           struct csinn_conv2d_params *params,
                                           void (*reorder_input)(__fp16 *, __fp16 *, int, int, int),
                                           void (*gemm)(__fp16 *, const __fp16 *, const __fp16 *,
                                                        __fp16 *, int, int, int, bool));
int shl_rvv_common_conv1x1_gemm_packn_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                           struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                           struct csinn_conv2d_params *params,
                                           void (*reorder_input)(int8_t *, int8_t *, int, int, int),
                                           void (*gemm)(int8_t *, const int8_t *, const int8_t *,
                                                        int32_t *, int, int, int, int32_t,
                                                        int32_t *, int32_t *));

int shl_rvv_common_conv1x1_gemm_pack1ton_fp32(
    struct csinn_tensor *input, struct csinn_tensor *output, struct csinn_tensor *kernel,
    struct csinn_tensor *bias, struct csinn_conv2d_params *params,
    void (*reorder_input)(float *, float *, int, int, int, int),
    void (*gemm)(float *, const float *, const float *, float *, int, int, int, bool));
int shl_rvv_common_conv1x1_gemm_pack1ton_fp16(
    struct csinn_tensor *input, struct csinn_tensor *output, struct csinn_tensor *kernel,
    struct csinn_tensor *bias, struct csinn_conv2d_params *params,
    void (*reorder_input)(__fp16 *, __fp16 *, int, int, int, int),
    void (*gemm)(__fp16 *, const __fp16 *, const __fp16 *, __fp16 *, int, int, int, bool));
int shl_rvv_common_conv1x1_gemm_pack1ton_int8(
    struct csinn_tensor *input, struct csinn_tensor *output, struct csinn_tensor *kernel,
    struct csinn_tensor *bias, struct csinn_conv2d_params *params,
    void (*reorder_input)(int8_t *, int8_t *, int, int, int, int),
    void (*gemm)(int8_t *, const int8_t *, const int8_t *, int32_t *, int, int, int, int32_t,
                 int32_t *, int32_t *));

int shl_rvv_common_conv1x1_gemm_packnto1_fp32(
    struct csinn_tensor *input, struct csinn_tensor *output, struct csinn_tensor *kernel,
    struct csinn_tensor *bias, struct csinn_conv2d_params *params,
    void (*reorder_input)(float *, float *, int, int, int),
    void (*gemm)(float *, const float *, const float *, float *, int, int, int, bool));
int shl_rvv_common_conv1x1_gemm_packnto1_fp16(
    struct csinn_tensor *input, struct csinn_tensor *output, struct csinn_tensor *kernel,
    struct csinn_tensor *bias, struct csinn_conv2d_params *params,
    void (*reorder_input)(__fp16 *, __fp16 *, int, int, int),
    void (*gemm)(__fp16 *, const __fp16 *, const __fp16 *, __fp16 *, int, int, int, bool));
int shl_rvv_common_conv1x1_gemm_packnto1_int8(
    struct csinn_tensor *input, struct csinn_tensor *output, struct csinn_tensor *kernel,
    struct csinn_tensor *bias, struct csinn_conv2d_params *params,
    void (*reorder_input)(int8_t *, int8_t *, int, int, int),
    void (*gemm)(int8_t *, const int8_t *, const int8_t *, int32_t *, int, int, int, int32_t,
                 int32_t *, int32_t *));

/*********************************** im2col + gemm ********************************/
void shl_rvv_conv1d_im2col_gemm_reorder_kernel_fp32(struct csinn_tensor *kernel,
                                                    struct csinn_conv1d_params *params);
void shl_rvv_conv1d_im2col_gemm_reorder_kernel_fp16(struct csinn_tensor *kernel,
                                                    struct csinn_conv1d_params *params);
void shl_rvv_conv1d_im2col_gemm_reorder_kernel_fp16_w_int8(struct csinn_tensor *kernel,
                                                           struct csinn_conv1d_params *params);
void shl_rvv_conv1d_im2col_gemm_dequantize_per_channel_i8_to_f16(struct csinn_tensor *kernel,
                                                                 struct csinn_conv1d_params *params,
                                                                 __fp16 *kernel_fp16);
void shl_rvv_conv_im2col_gemm_reorder_kernel_fp32(struct csinn_tensor *kernel,
                                                  struct csinn_conv2d_params *params);
void shl_rvv_conv_im2col_gemm_reorder_kernel_fp16(struct csinn_tensor *kernel,
                                                  struct csinn_conv2d_params *params);
void shl_rvv_conv_im2col_gemm_reorder_kernel_fp16_w_int8(struct csinn_tensor *kernel,
                                                         struct csinn_conv2d_params *params);
void shl_rvv_conv_im2col_gemm_dequantize_per_channel_i8_to_f16(struct csinn_tensor *kernel,
                                                               struct csinn_conv2d_params *params,
                                                               __fp16 *kernel_fp16);
void shl_rvv_conv_im2col_gemm_reorder_kernel_int8(struct csinn_tensor *kernel,
                                                  struct csinn_conv2d_params *params);

int shl_rvv_conv1d_im2col_gemm_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                    struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                    struct csinn_conv1d_params *params);
int shl_rvv_conv1d_im2col_gemm_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                    struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                    struct csinn_conv1d_params *params);
int shl_rvv_conv_im2col_gemm_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                  struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                  struct csinn_conv2d_params *params);
int shl_rvv_conv_im2col_gemm_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                  struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                  struct csinn_conv2d_params *params);
int shl_rvv_conv_im2col_gemm_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                  struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                  struct csinn_conv2d_params *params);

void shl_rvv_conv_im2col_gemm_reorder_kernel_packn_fp32(struct csinn_tensor *kernel,
                                                        struct csinn_conv2d_params *params);
void shl_rvv_conv_im2col_gemm_reorder_kernel_packn_fp16(struct csinn_tensor *kernel,
                                                        struct csinn_conv2d_params *params);
void shl_rvv_conv_im2col_gemm_reorder_kernel_packn_fp16_w_int8(struct csinn_tensor *kernel,
                                                               struct csinn_conv2d_params *params);
void shl_rvv_conv_im2col_gemm_packn_dequantize_per_channel_i8_to_f16(
    struct csinn_tensor *kernel, struct csinn_conv2d_params *params, __fp16 *kernel_fp16);
void shl_rvv_conv_im2col_gemm_reorder_kernel_packn_int8(struct csinn_tensor *kernel,
                                                        struct csinn_conv2d_params *params);

int shl_rvv_conv_im2col_gemm_packn_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                        struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                        struct csinn_conv2d_params *params);
int shl_rvv_conv_im2col_gemm_packn_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                        struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                        struct csinn_conv2d_params *params);
int shl_rvv_conv_im2col_gemm_packn_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                        struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                        struct csinn_conv2d_params *params);

void shl_rvv_conv_im2col_gemm_reorder_kernel_pack1ton_fp32(struct csinn_tensor *kernel,
                                                           struct csinn_conv2d_params *params);
void shl_rvv_conv_im2col_gemm_reorder_kernel_pack1ton_fp16(struct csinn_tensor *kernel,
                                                           struct csinn_conv2d_params *params);
void shl_rvv_conv_im2col_gemm_reorder_kernel_pack1ton_fp16_w_int8(
    struct csinn_tensor *kernel, struct csinn_conv2d_params *params);
void shl_rvv_conv_im2col_gemm_pack1ton_dequantize_per_channel_i8_to_f16(
    struct csinn_tensor *kernel, struct csinn_conv2d_params *params, __fp16 *kernel_fp16);
void shl_rvv_conv_im2col_gemm_reorder_kernel_pack1ton_int8(struct csinn_tensor *kernel,
                                                           struct csinn_conv2d_params *params);

int shl_rvv_conv_im2col_gemm_pack1ton_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                           struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                           struct csinn_conv2d_params *params);
int shl_rvv_conv_im2col_gemm_pack1ton_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                           struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                           struct csinn_conv2d_params *params);
int shl_rvv_conv_im2col_gemm_pack1ton_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                           struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                           struct csinn_conv2d_params *params);

void shl_rvv_conv_im2col_gemm_reorder_kernel_packnto1_fp32(struct csinn_tensor *kernel,
                                                           struct csinn_conv2d_params *params);
void shl_rvv_conv_im2col_gemm_reorder_kernel_packnto1_fp16(struct csinn_tensor *kernel,
                                                           struct csinn_conv2d_params *params);
void shl_rvv_conv_im2col_gemm_reorder_kernel_packnto1_fp16_w_int8(
    struct csinn_tensor *kernel, struct csinn_conv2d_params *params);
void shl_rvv_conv_im2col_gemm_packnto1_dequantize_per_channel_i8_to_f16(
    struct csinn_tensor *kernel, struct csinn_conv2d_params *params, __fp16 *kernel_fp16);
void shl_rvv_conv_im2col_gemm_reorder_kernel_packnto1_int8(struct csinn_tensor *kernel,
                                                           struct csinn_conv2d_params *params);

int shl_rvv_conv_im2col_gemm_packnto1_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                           struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                           struct csinn_conv2d_params *params);
int shl_rvv_conv_im2col_gemm_packnto1_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                           struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                           struct csinn_conv2d_params *params);
int shl_rvv_conv_im2col_gemm_packnto1_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                           struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                           struct csinn_conv2d_params *params);

/******************************** conv2d1x1s1 + gemm ******************************/
void shl_rvv_conv1x1s1_gemm_reorder_kernel_fp32(struct csinn_tensor *kernel,
                                                struct csinn_conv2d_params *params);
void shl_rvv_conv1x1s1_gemm_reorder_kernel_fp16(struct csinn_tensor *kernel,
                                                struct csinn_conv2d_params *params);
void shl_rvv_conv1x1s1_gemm_reorder_kernel_fp16_w_int8(struct csinn_tensor *kernel,
                                                       struct csinn_conv2d_params *params);
void shl_rvv_conv1x1s1_gemm_reorder_kernel_int8(struct csinn_tensor *kernel,
                                                struct csinn_conv2d_params *params);

int shl_rvv_conv1x1s1_gemm_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                struct csinn_conv2d_params *params);
int shl_rvv_conv1x1s1_gemm_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                struct csinn_conv2d_params *params);
int shl_rvv_conv1x1s1_gemm_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                struct csinn_conv2d_params *params);

void shl_rvv_conv1x1s1_gemm_reorder_kernel_packn_fp32(struct csinn_tensor *kernel,
                                                      struct csinn_conv2d_params *params);
void shl_rvv_conv1x1s1_gemm_reorder_kernel_packn_fp16(struct csinn_tensor *kernel,
                                                      struct csinn_conv2d_params *params);
void shl_rvv_conv1x1s1_gemm_reorder_kernel_packn_fp16_w_int8(struct csinn_tensor *kernel,
                                                             struct csinn_conv2d_params *params);
void shl_rvv_conv1x1s1_gemm_reorder_kernel_packn_int8(struct csinn_tensor *kernel,
                                                      struct csinn_conv2d_params *params);

int shl_rvv_conv1x1s1_gemm_packn_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                      struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                      struct csinn_conv2d_params *params);
int shl_rvv_conv1x1s1_gemm_packn_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                      struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                      struct csinn_conv2d_params *params);
int shl_rvv_conv1x1s1_gemm_packn_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                      struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                      struct csinn_conv2d_params *params);

void shl_rvv_conv1x1s1_gemm_reorder_kernel_pack1ton_fp32(struct csinn_tensor *kernel,
                                                         struct csinn_conv2d_params *params);
void shl_rvv_conv1x1s1_gemm_reorder_kernel_pack1ton_fp16(struct csinn_tensor *kernel,
                                                         struct csinn_conv2d_params *params);
void shl_rvv_conv1x1s1_gemm_reorder_kernel_pack1ton_fp16_w_int8(struct csinn_tensor *kernel,
                                                                struct csinn_conv2d_params *params);
void shl_rvv_conv1x1s1_gemm_reorder_kernel_pack1ton_int8(struct csinn_tensor *kernel,
                                                         struct csinn_conv2d_params *params);

int shl_rvv_conv1x1s1_gemm_pack1ton_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                         struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                         struct csinn_conv2d_params *params);
int shl_rvv_conv1x1s1_gemm_pack1ton_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                         struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                         struct csinn_conv2d_params *params);
int shl_rvv_conv1x1s1_gemm_pack1ton_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                         struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                         struct csinn_conv2d_params *params);

void shl_rvv_conv1x1s1_gemm_reorder_kernel_packnto1_fp32(struct csinn_tensor *kernel,
                                                         struct csinn_conv2d_params *params);
void shl_rvv_conv1x1s1_gemm_reorder_kernel_packnto1_fp16(struct csinn_tensor *kernel,
                                                         struct csinn_conv2d_params *params);
void shl_rvv_conv1x1s1_gemm_reorder_kernel_packnto1_fp16_w_int8(struct csinn_tensor *kernel,
                                                                struct csinn_conv2d_params *params);
void shl_rvv_conv1x1s1_gemm_reorder_kernel_packnto1_int8(struct csinn_tensor *kernel,
                                                         struct csinn_conv2d_params *params);

int shl_rvv_conv1x1s1_gemm_packnto1_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                         struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                         struct csinn_conv2d_params *params);
int shl_rvv_conv1x1s1_gemm_packnto1_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                         struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                         struct csinn_conv2d_params *params);
int shl_rvv_conv1x1s1_gemm_packnto1_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                         struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                         struct csinn_conv2d_params *params);

/************************************* winograd ***********************************/
void shl_rvv_wg_b6f3s1_trans_kernel_packn_fp32(struct csinn_tensor *src_kernel,
                                               struct csinn_tensor *dst_kernel);
void shl_rvv_wg_b6f3s1_trans_kernel_packn_fp16(struct csinn_tensor *src_kernel,
                                               struct csinn_tensor *dst_kernel);

int shl_rvv_wg_b6f3s1_packn_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                 struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                 struct csinn_conv2d_params *params);
int shl_rvv_wg_b6f3s1_packn_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                 struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                 struct csinn_conv2d_params *params);

void shl_rvv_wg_b4f3s1_trans_kernel_packn_fp32(struct csinn_tensor *src_kernel,
                                               struct csinn_tensor *dst_kernel);
void shl_rvv_wg_b4f3s1_trans_kernel_packn_fp16(struct csinn_tensor *src_kernel,
                                               struct csinn_tensor *dst_kernel);
void shl_rvv_wg_b4f3s1_trans_kernel_packn_int8(struct csinn_tensor *src_kernel,
                                               struct csinn_tensor *dst_kernel);

int shl_rvv_wg_b4f3s1_packn_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                 struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                 struct csinn_conv2d_params *params);
int shl_rvv_wg_b4f3s1_packn_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                 struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                 struct csinn_conv2d_params *params);
int shl_rvv_wg_b4f3s1_packn_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                 struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                 struct csinn_conv2d_params *params);

/************************************** direct ************************************/
void shl_rvv_conv3x3s1_direct_reorder_kernel_pack4n_fp16(struct csinn_tensor *kernel,
                                                         struct csinn_conv2d_params *params);
int shl_rvv_conv3x3s1_direct_fp16_nhwc(struct csinn_tensor *input, struct csinn_tensor *output,
                                       struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                       struct csinn_conv2d_params *params);

/******************************* depthwise convolution ****************************/
int shl_rvv_dwconv3x3s1_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_tensor *kernel, struct csinn_tensor *bias,
                             struct csinn_conv2d_params *params);
int shl_rvv_dwconv3x3s2_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_tensor *kernel, struct csinn_tensor *bias,
                             struct csinn_conv2d_params *params);
int shl_rvv_dwconv3x3s1_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_tensor *kernel, struct csinn_tensor *bias,
                             struct csinn_conv2d_params *params);
int shl_rvv_dwconv3x3s2_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_tensor *kernel, struct csinn_tensor *bias,
                             struct csinn_conv2d_params *params);
int shl_rvv_dwconv3x3s1_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_tensor *kernel, struct csinn_tensor *bias,
                             struct csinn_conv2d_params *params);
int shl_rvv_dwconv3x3s2_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_tensor *kernel, struct csinn_tensor *bias,
                             struct csinn_conv2d_params *params);
int shl_rvv_dwconv3x3s1_int4(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_tensor *kernel, struct csinn_tensor *bias,
                             struct csinn_conv2d_params *params);
int shl_rvv_dwconv3x3s2_int4(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_tensor *kernel, struct csinn_tensor *bias,
                             struct csinn_conv2d_params *params);

void shl_rvv_dwconv_reorder_kernel_packn_fp32(struct csinn_tensor *kernel,
                                              struct csinn_conv2d_params *params);
void shl_rvv_dwconv_reorder_kernel_packn_fp16(struct csinn_tensor *kernel,
                                              struct csinn_conv2d_params *params);
void shl_rvv_dwconv_reorder_kernel_packn_fp16_w_int8(struct csinn_tensor *kernel,
                                                     struct csinn_conv2d_params *params);
void shl_rvv_dwconv_reorder_kernel_packn_int8(struct csinn_tensor *kernel,
                                              struct csinn_conv2d_params *params);

int shl_rvv_dwconv3x3s1_packn_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                   struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                   struct csinn_conv2d_params *params);
int shl_rvv_dwconv3x3s2_packn_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                   struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                   struct csinn_conv2d_params *params);
int shl_rvv_dwconv3x3s1_packn_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                   struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                   struct csinn_conv2d_params *params);
int shl_rvv_dwconv3x3s2_packn_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                   struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                   struct csinn_conv2d_params *params);
int shl_rvv_dwconv3x3s1_packn_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                   struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                   struct csinn_conv2d_params *params);
int shl_rvv_dwconv3x3s2_packn_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                   struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                   struct csinn_conv2d_params *params);

int shl_rvv_dwconv_packn_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_tensor *kernel, struct csinn_tensor *bias,
                              struct csinn_conv2d_params *params);
int shl_rvv_dwconv_packn_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_tensor *kernel, struct csinn_tensor *bias,
                              struct csinn_conv2d_params *params);
int shl_rvv_dwconv_packn_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_tensor *kernel, struct csinn_tensor *bias,
                              struct csinn_conv2d_params *params);

int shl_rvv_dwconv_nhwc_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_tensor *kernel, struct csinn_tensor *bias,
                             struct csinn_conv2d_params *params);
int shl_rvv_dwconv_nhwc_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_tensor *kernel, struct csinn_tensor *bias,
                             struct csinn_conv2d_params *params);
int shl_rvv_dwconv_nhwc_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_tensor *kernel, struct csinn_tensor *bias,
                             struct csinn_conv2d_params *params);

int shl_rvv_dwconv3x3s1_nhwc_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                  struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                  struct csinn_conv2d_params *params);
int shl_rvv_dwconv3x3s2_nhwc_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                  struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                  struct csinn_conv2d_params *params);
/************************************ deconvolution *********************************/
/********************************* common gemm + col2im *****************************/
int shl_rvv_common_deconv2d_gemm_col2im_fp32(
    struct csinn_tensor *input, struct csinn_tensor *output, struct csinn_tensor *kernel,
    struct csinn_tensor *bias, struct csinn_conv2d_params *params,
    void (*reorder_input)(float *, float *, int, int, int),
    void (*gemm)(float *, const float *, const float *, float *, int, int, int, int));
int shl_rvv_common_deconv2d_gemm_col2im_fp16(
    struct csinn_tensor *input, struct csinn_tensor *output, struct csinn_tensor *kernel,
    struct csinn_tensor *bias, struct csinn_conv2d_params *params,
    void (*reorder_input)(__fp16 *, __fp16 *, int, int, int),
    void (*gemm)(__fp16 *, const __fp16 *, const __fp16 *, __fp16 *, int, int, int, int));

/************************************ gemm + col2im *********************************/
void shl_rvv_deconv2d_gemm_col2im_reorder_kernel_fp32(struct csinn_tensor *kernel,
                                                      struct csinn_conv2d_params *params);

int shl_rvv_deconv2d_gemm_col2im_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                      struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                      struct csinn_conv2d_params *params);

void shl_rvv_deconv2d_gemm_col2im_reorder_kernel_fp16(struct csinn_tensor *kernel,
                                                      struct csinn_conv2d_params *params);

void shl_rvv_deconv2d_gemm_col2im_reorder_kernel_fp16_w_int8(struct csinn_tensor *kernel,
                                                             struct csinn_conv2d_params *params);

void shl_rvv_deconv2d_gemm_col2im_dequantize_per_channel_i8_to_f16(
    struct csinn_tensor *kernel, struct csinn_conv2d_params *params, __fp16 *kernel_fp16);

int shl_rvv_deconv2d_gemm_col2im_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                      struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                      struct csinn_conv2d_params *params);

/*************************************** gemm *************************************/
void shl_rvv_reorder_kernel_n8_fp32(float *a, float *sa, int m, int k, int ldx);
void shl_rvv_reorder_input_z8_fp32(float *b, float *sb, int k, int n, int ldx);
void shl_rvv_gemm_8x8_fp32(float *dst, const float *sa, const float *sb, float *bias, int m, int k,
                           int n, int ldc);

void shl_rvv_reorder_kernel_n8_fp16(__fp16 *a, __fp16 *sa, int m, int k, int ldx);
void shl_rvv_reorder_input_z16_fp16(__fp16 *b, __fp16 *sb, int k, int n, int ldx);
void shl_rvv_gemm_8x16_fp16(__fp16 *dst, const __fp16 *sa, const __fp16 *sb, __fp16 *bias, int m,
                            int k, int n, int ldc);

void shl_rvv_reorder_kernel_n8_int8_dot(int8_t *a, int8_t *sa, int m, int k, int ldx);
void shl_rvv_reorder_input_z8_int8_dot(int8_t *b, int8_t *sb, int k, int n, int ldx);
void shl_rvv_gemm_8x8_int8_dot(int8_t *dst, const int8_t *sa, const int8_t *sb, int32_t *bias,
                               int m, int k, int n, int ldc, int32_t out_zp, int32_t *mult,
                               int32_t *shift);

void shl_rvv_reorder_kernel_n4_int8_v128(int8_t *a, int8_t *sa, int m, int k, int ldx);
void shl_rvv_reorder_input_z16_int8_v128(int8_t *b, int8_t *sb, int k, int n, int ldx);
void shl_rvv_gemm_4x16_int8_v128(int8_t *dst, const int8_t *sa, const int8_t *sb, int32_t *bias,
                                 int m, int k, int n, int ldc, int32_t out_zp, int32_t *mult,
                                 int32_t *shift);

void shl_rvv_reorder_input_n8_int4_dot(int8_t *a, int8_t *sa, int m, int k, int ldx);
void shl_rvv_reorder_kernel_n8_int4(int8_t *b, int8_t *sb, int n, int k, int ldx);
void shl_rvv_gemm_8x8_int4_dot(int8_t *dst, const int8_t *sa, const int8_t *sb, int m, int k, int n,
                               int ldc, int32_t *bias, int32_t out_zp, int32_t *mult,
                               int32_t *shift);

/************************************ gemm ncxhwx *********************************/
void shl_rvv_reorder_kernel_packn_fp32(float *a, float *sa, int m, int k, int ldx);
void shl_rvv_reorder_input_z8_packn_fp32(float *b, float *sb, int k, int n, int ldx);
void shl_rvv_reorder_input_z12_packn_fp32(float *b, float *sb, int k, int n, int ldx);
void shl_rvv_ncxhwx_gemm_12xpack2n_fp32(float *dst, const float *sa, const float *sb, float *bias,
                                        int m, int k, int n, bool fuse_relu);

void shl_rvv_reorder_kernel_packn_fp16(__fp16 *a, __fp16 *sa, int m, int k, int ldx);
void shl_rvv_reorder_input_z8_packn_fp16(__fp16 *b, __fp16 *sb, int k, int n, int ldx);
void shl_rvv_reorder_input_z12_packn_fp16(__fp16 *b, __fp16 *sb, int k, int n, int ldx);
void shl_rvv_ncxhwx_gemm_12xpack2n_fp16(__fp16 *dst, const __fp16 *sa, const __fp16 *sb,
                                        __fp16 *bias, int m, int k, int n, bool fuse_relu);

void shl_rvv_reorder_input_z8_packn_int8_dot(int8_t *b, int8_t *sb, int k, int n, int ldx);
void shl_rvv_reorder_input_z12_packn_int8_dot(int8_t *b, int8_t *sb, int k, int n, int ldx);
void shl_rvv_ncxhwx_gemm_12xpackn_int8_dot(int8_t *dst, const int8_t *sa, const int8_t *sb,
                                           int32_t *bias, int m, int k, int n, int32_t out_zp,
                                           int32_t *mult, int32_t *shift);

void shl_rvv_reorder_input_z8_packn_int4(int8_t *b, int8_t *sb, int k, int n, int ldx);
void shl_rvv_ncxhwx_gemm_8xpackn_int4(int8_t *dst, const int8_t *sa, const int8_t *sb,
                                      int32_t *bias, int m, int k, int n, int ldc, int32_t out_zp,
                                      int32_t *mult, int32_t *shift);

void shl_rvv_reorder_input_z12_packn_int4(int8_t *b, int8_t *sb, int k, int n, int ldx);
void shl_rvv_ncxhwx_gemm_12xpackn_int4(int8_t *dst, const int8_t *sa, const int8_t *sb,
                                       int32_t *bias, int m, int k, int n, int ldc, int32_t out_zp,
                                       int32_t *mult, int32_t *shift);

void shl_rvv_reorder_input_z12_pack1ton_fp32(float *b, float *sb, int inc, int maxk, int n,
                                             int ldx);
void shl_rvv_reorder_input_z12_pack1ton_fp16(__fp16 *b, __fp16 *sb, int inc, int maxk, int n,
                                             int ldx);
void shl_rvv_reorder_input_z4_pack1ton_int8(int8_t *b, int8_t *sb, int inc, int maxk, int n,
                                            int ldx);
void shl_rvv_reorder_input_z12_pack1ton_int8_dot(int8_t *b, int8_t *sb, int inc, int maxk, int n,
                                                 int ldx);

void shl_rvv_reorder_input_z4_packn_int8(int8_t *b, int8_t *sb, int k, int n, int ldx);
void shl_rvv_ncxhwx_gemm_4xpack2n_int8(int8_t *dst, const int8_t *sa, const int8_t *sb,
                                       int32_t *bias, int m, int k, int n, int32_t out_zp,
                                       int32_t *mult, int32_t *shift);

/************************************ gemm block **********************************/
void shl_rvv_reorder_a_block_12xk_fp32(float *src, float *dst, int m, int k, const int M_BLK,
                                       const int K_BLK);
void shl_rvv_reorder_b_block_pack2nxk_fp32(float *src, float *dst, int k, int n, const int K_BLK,
                                           const int N_BLK);
void shl_rvv_gemm_block_12xpack2n_fp32(float *dst, const float *sa, const float *sb, float *bias,
                                       int m, int k, int n, const int M_BLK, const int K_BLK,
                                       const int N_BLK);

void shl_rvv_reorder_a_block_12xk_fp16(__fp16 *src, __fp16 *dst, int m, int k, const int M_BLK,
                                       const int K_BLK);
void shl_rvv_reorder_b_block_pack2nxk_fp16(__fp16 *src, __fp16 *dst, int k, int n, const int K_BLK,
                                           const int N_BLK);
void shl_rvv_reorder_b_block_pack2nxk_fp16_w_int8(int8_t *src, int8_t *dst, int k, int n,
                                                  const int K_BLK, const int N_BLK);
void shl_rvv_gemm_block_12xpack2n_fp16(__fp16 *dst, const __fp16 *sa, const __fp16 *sb,
                                       __fp16 *bias, int m, int k, int n, const int M_BLK,
                                       const int K_BLK, const int N_BLK);

/************************************ gemm a0b0 **********************************/
void shl_rvv_reorder_a_n12_fp32(float *src, float *dst, int M, int K, int lda);
void shl_rvv_reorder_b_zpack2n_fp32(float *src, float *dst, int K, int N, int ldb);
void shl_rvv_gemm_a0b0_12xpack2n_fp32(float *dst, const float *sa, const float *sb, float *bias,
                                      int M, int K, int N, int ldc);

void shl_rvv_reorder_a_n12_fp16(__fp16 *src, __fp16 *dst, int M, int K, int lda);
void shl_rvv_reorder_a_n12_fp16_w_int8(int8_t *src, int8_t *dst, int M, int K, int lda);
void shl_rvv_reorder_b_zpack2n_fp16(__fp16 *src, __fp16 *dst, int K, int N, int ldb);
void shl_rvv_reorder_b_zpack2n_fp16_w_int8(int8_t *src, int8_t *dst, int K, int N, int ldb);
void shl_rvv_gemm_a0b0_12xpack2n_fp16(__fp16 *dst, const __fp16 *sa, const __fp16 *sb, __fp16 *bias,
                                      int M, int K, int N, int ldc);

/************************************ gemm a0b1 **********************************/
void shl_rvv_reorder_b_npack2n_fp32(float *src, float *dst, int n, int k);
void shl_rvv_reorder_b_npack2n_fp16(__fp16 *src, __fp16 *dst, int n, int k);
void shl_rvv_reorder_b_npack2n_fp16_w_int8(int8_t *src, int8_t *dst, int n, int k);

void shl_rvv_gemm_a0nb1r_12xpack2n_fp32(float *dst, const float *sa, const float *sb, float *bias,
                                        int M, int K, int N);
void shl_rvv_gemm_a0nb1r_12xpack2n_fp16(__fp16 *dst, const __fp16 *sa, const __fp16 *sb,
                                        __fp16 *bias, int M, int K, int N);

void shl_rvv_dequantize_block_q8_to_f32(const int8_t *src, const __fp16 *scale, float *dst,
                                        int n_blk, int k_blk, int ld_src, int ld_dst);
void shl_rvv_dequantize_block_q4_to_f32(const int8_t *src, const __fp16 *scale, float *dst,
                                        int n_blk, int k_blk, int ld_src, int ld_dst);

void shl_rvv_gemm_dot_4x4_fp32(float *dst, const float *sa, const float *sb, float *bias, int M,
                               int K, int N, int lda, int ldb, int ldc, int k_idx);
void shl_rvv_gemm_dot_1x1_fp32_q8(float *dst, const float *sa, const int8_t *sb,
                                  const __fp16 *scale, float *bias, int M, int K, int N, int lda,
                                  int ldb, int ldc, int k_idx);
void shl_rvv_gemm_dot_1x1_fp32_q4(float *dst, const float *sa, const int8_t *sb,
                                  const __fp16 *scale, float *bias, int M, int K, int N, int lda,
                                  int ldb, int ldc, int k_idx);

void shl_rvv_dequantize_block_q8_to_f16(const int8_t *src, const __fp16 *scale, __fp16 *dst,
                                        int n_blk, int k_blk, int ld_src, int ld_dst);
void shl_rvv_dequantize_block_q4_to_f16(const int8_t *src, const __fp16 *scale, __fp16 *dst,
                                        int n_blk, int k_blk, int ld_src, int ld_dst);

void shl_rvv_gemm_dot_4x4_fp16(__fp16 *dst, const __fp16 *sa, const __fp16 *sb, __fp16 *bias, int M,
                               int K, int N, int lda, int ldb, int ldc, int k_idx);
void shl_rvv_gemm_dot_1x1_fp16_q8(__fp16 *dst, const __fp16 *sa, const int8_t *sb,
                                  const __fp16 *scale, __fp16 *bias, int M, int K, int N, int lda,
                                  int ldb, int ldc, int k_idx);
void shl_rvv_gemm_dot_1x1_fp16_q4(__fp16 *dst, const __fp16 *sa, const int8_t *sb,
                                  const __fp16 *scale, __fp16 *bias, int M, int K, int N, int lda,
                                  int ldb, int ldc, int k_idx);

void shl_rvv_gemm_a0nb1_dot_fp16_q8_rearrange(__fp16 *dst, const __fp16 *sa, const int8_t *sb,
                                              __fp16 *bias, int M, int K, int N,
                                              const __fp16 *scale);
void shl_rvv_gemm_a0nb1_dot_fp16_q4_rearrange(__fp16 *dst, const __fp16 *sa, const int8_t *sb,
                                              __fp16 *bias, int M, int K, int N,
                                              const __fp16 *scale);

/************************************ pooling *********************************/
int shl_rvv_avgpool2x2s2_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_pool_params *params);
int shl_rvv_avgpool2x2s2_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_pool_params *params);
int shl_rvv_avgpool2x2s2_p1_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                 struct csinn_pool_params *params);
int shl_rvv_avgpool2x2s2_p1_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                 struct csinn_pool_params *params);
int shl_rvv_avgpool3x3s2_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_pool_params *params);
int shl_rvv_avgpool3x3s2_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_pool_params *params);
int shl_rvv_avgpool3x3s2_p1_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                 struct csinn_pool_params *params);
int shl_rvv_avgpool3x3s2_p1_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                 struct csinn_pool_params *params);
int shl_rvv_avgpool3x3s1_p1_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                 struct csinn_pool_params *params);
int shl_rvv_avgpool3x3s1_p1_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                 struct csinn_pool_params *params);

int shl_rvv_maxpool2x2s2_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_pool_params *params);
int shl_rvv_maxpool2x2s2_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_pool_params *params);
int shl_rvv_maxpool2x2s2_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_pool_params *params);
int shl_rvv_maxpool2x2s2_p1_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                 struct csinn_pool_params *params);
int shl_rvv_maxpool2x2s2_p1_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                 struct csinn_pool_params *params);
int shl_rvv_maxpool2x2s2_p1_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                 struct csinn_pool_params *params);
int shl_rvv_maxpool3x3s2_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_pool_params *params);
int shl_rvv_maxpool3x3s2_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_pool_params *params);
int shl_rvv_maxpool3x3s2_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_pool_params *params);
int shl_rvv_maxpool3x3s2_p1_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                 struct csinn_pool_params *params);
int shl_rvv_maxpool3x3s2_p1_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                 struct csinn_pool_params *params);
int shl_rvv_maxpool3x3s2_p1_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                 struct csinn_pool_params *params);
int shl_rvv_maxpool3x3s1_p1_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                 struct csinn_pool_params *params);
int shl_rvv_maxpool3x3s1_p1_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                 struct csinn_pool_params *params);
int shl_rvv_maxpool3x3s1_p1_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                 struct csinn_pool_params *params);

int shl_rvv_global_avgpool2d_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                  struct csinn_pool_params *params);
int shl_rvv_global_avgpool2d_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                  struct csinn_pool_params *params);

int shl_rvv_global_maxpool2d_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                  struct csinn_pool_params *params);
int shl_rvv_global_maxpool2d_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                  struct csinn_pool_params *params);

int shl_rvv_global_maxpool2d_packn_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                        struct csinn_pool_params *params);
int shl_rvv_global_maxpool2d_packn_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                        struct csinn_pool_params *params);
int shl_rvv_global_maxpool2d_packn_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                        struct csinn_pool_params *params);
int shl_rvv_global_avgpool2d_packn_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                        struct csinn_pool_params *params);
int shl_rvv_global_avgpool2d_packn_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                        struct csinn_pool_params *params);
int shl_rvv_global_avgpool2d_packn_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                        struct csinn_pool_params *params);

int shl_rvv_maxpool_packn_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                               struct csinn_pool_params *params);
int shl_rvv_maxpool_packn_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                               struct csinn_pool_params *params);
int shl_rvv_maxpool_packn_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                               struct csinn_pool_params *params);

int shl_rvv_avgpool_packn_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                               struct csinn_pool_params *params);
int shl_rvv_avgpool_packn_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                               struct csinn_pool_params *params);
int shl_rvv_avgpool_packn_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                               struct csinn_pool_params *params);

int shl_rvv_maxpool_nhwc_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_pool_params *params);
int shl_rvv_maxpool_nhwc_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_pool_params *params);
int shl_rvv_maxpool_nhwc_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_pool_params *params);

int shl_rvv_avgpool_nhwc_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_pool_params *params);
int shl_rvv_avgpool_nhwc_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_pool_params *params);
int shl_rvv_avgpool_nhwc_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_pool_params *params);

int shl_rvv_global_maxpool2d_nhwc_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                       struct csinn_pool_params *params);
int shl_rvv_global_maxpool2d_nhwc_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                       struct csinn_pool_params *params);
int shl_rvv_global_maxpool2d_nhwc_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                       struct csinn_pool_params *params);
int shl_rvv_global_avgpool2d_nhwc_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                       struct csinn_pool_params *params);
int shl_rvv_global_avgpool2d_nhwc_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                       struct csinn_pool_params *params);
int shl_rvv_global_avgpool2d_nhwc_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                       struct csinn_pool_params *params);

/************************************ fullyconnected *********************************/
void shl_rvv_fc_gemm_reorder_weight_fp32(struct csinn_tensor *weights);
void shl_rvv_fc_gemm_reorder_weight_fp16(struct csinn_tensor *weights);
void shl_rvv_fc_gemm_reorder_weight_fp16_w_int8(struct csinn_tensor *weights);
void shl_rvv_fc_gemm_reorder_weight_int8(struct csinn_tensor *weights);

void shl_rvv_fc_npack2n_dequantize_per_channel_i8_to_f16(struct csinn_tensor *weights,
                                                         struct csinn_fc_params *params,
                                                         __fp16 *weights_fp16);

void shl_rvv_gemm_a0b1_12xpack2n_fp32(float *dst, const float *sa, const float *sb, float *bias,
                                      int M, int K, int N);
void shl_rvv_gemm_a0b1_12xpack2n_fp16(__fp16 *dst, const __fp16 *sa, const __fp16 *sb, __fp16 *bias,
                                      int M, int K, int N);
void shl_rvv_gemm_a0b1_4xpackn_int8(int8_t *dst, const int8_t *sa, const int8_t *sb,
                                    const int32_t *bias, int M, int K, int N, int32_t out_zp,
                                    int32_t *mult, int32_t *shift);
void shl_rvv_gemm_a0b1_8xmf2_int8_dot(int8_t *dst, const int8_t *sa, const int8_t *sb,
                                      const int32_t *bias, int M, int K, int N, int32_t out_zp,
                                      int32_t *mult, int32_t *shift);

int shl_rvv_fullyconnected_gemm_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                                     struct csinn_tensor *weights, struct csinn_tensor *bias,
                                     struct csinn_fc_params *params);
int shl_rvv_fullyconnected_gemm_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                     struct csinn_tensor *weights, struct csinn_tensor *bias,
                                     struct csinn_fc_params *params);
int shl_rvv_fullyconnected_gemm_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                     struct csinn_tensor *weights, struct csinn_tensor *bias,
                                     struct csinn_fc_params *params);

/************************************ activation *********************************/
int shl_rvv_relu_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                      struct csinn_relu_params *params);
int shl_rvv_relu_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                      struct csinn_relu_params *params);
int shl_rvv_relu_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                      struct csinn_relu_params *params);

int shl_rvv_relu1_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                       struct csinn_relu_params *params);
int shl_rvv_relu1_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                       struct csinn_relu_params *params);
int shl_rvv_relu1_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                       struct csinn_relu_params *params);

int shl_rvv_relu6_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                       struct csinn_relu_params *params);
int shl_rvv_relu6_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                       struct csinn_relu_params *params);
int shl_rvv_relu6_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                       struct csinn_relu_params *params);

int shl_rvv_leaky_relu_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                            struct csinn_relu_params *params);
int shl_rvv_leaky_relu_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                            struct csinn_relu_params *params);
int shl_rvv_leaky_relu_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                            struct csinn_relu_params *params);

int shl_rvv_sigmoid_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                         struct csinn_sigmoid_params *params);
int shl_rvv_sigmoid_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                         struct csinn_sigmoid_params *params);
int shl_rvv_sigmoid_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                         struct csinn_sigmoid_params *params);

int shl_rvv_softmax_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                         struct csinn_softmax_params *params);
int shl_rvv_softmax_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                         struct csinn_softmax_params *params);
int shl_rvv_softmax_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                         struct csinn_softmax_params *params);

int shl_rvv_prelu_fp32(struct csinn_tensor *input, struct csinn_tensor *alpha,
                       struct csinn_tensor *output, struct csinn_prelu_params *params);
int shl_rvv_prelu_fp16(struct csinn_tensor *input, struct csinn_tensor *alpha,
                       struct csinn_tensor *output, struct csinn_prelu_params *params);
int shl_rvv_prelu_int8(struct csinn_tensor *input, struct csinn_tensor *alpha,
                       struct csinn_tensor *output, struct csinn_prelu_params *params);

int shl_rvv_clip_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                      struct csinn_clip_params *params);
int shl_rvv_clip_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                      struct csinn_clip_params *params);
int shl_rvv_clip_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                      struct csinn_clip_params *params);

int shl_rvv_silu_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                      struct csinn_silu_params *params);
int shl_rvv_silu_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                      struct csinn_silu_params *params);
int shl_rvv_silu_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                      struct csinn_silu_params *params);

int shl_rvv_hard_sigmoid_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_sigmoid_params *params);
int shl_rvv_hard_sigmoid_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_sigmoid_params *params);
int shl_rvv_hard_sigmoid_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                              struct csinn_sigmoid_params *params);

/************************************ layout/memory transform *********************************/
int shl_rvv_concat_fp32(struct csinn_tensor **input, struct csinn_tensor *output,
                        struct csinn_concat_params *params);
int shl_rvv_concat_fp16(struct csinn_tensor **input, struct csinn_tensor *output,
                        struct csinn_concat_params *params);
int shl_rvv_concat_int8(struct csinn_tensor **input, struct csinn_tensor *output,
                        struct csinn_concat_params *params);

int shl_rvv_split_fp32(struct csinn_tensor *input, struct csinn_tensor **output,
                       struct csinn_split_params *params);
int shl_rvv_split_fp16(struct csinn_tensor *input, struct csinn_tensor **output,
                       struct csinn_split_params *params);
int shl_rvv_split_int8(struct csinn_tensor *input, struct csinn_tensor **output,
                       struct csinn_split_params *params);

int shl_rvv_reshape_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                         struct csinn_reshape_params *params);
int shl_rvv_reshape_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                         struct csinn_reshape_params *params);
int shl_rvv_reshape_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                         struct csinn_reshape_params *params);

int shl_rvv_transpose_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                           struct csinn_transpose_params *params);
int shl_rvv_transpose_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                           struct csinn_transpose_params *params);
int shl_rvv_transpose_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                           struct csinn_transpose_params *params);

int shl_rvv_gather_fp32(struct csinn_tensor *input, struct csinn_tensor *indices,
                        struct csinn_tensor *output, struct csinn_gather_params *params);
int shl_rvv_gather_fp16(struct csinn_tensor *input, struct csinn_tensor *indices,
                        struct csinn_tensor *output, struct csinn_gather_params *params);
int shl_rvv_gather_int8(struct csinn_tensor *input, struct csinn_tensor *indices,
                        struct csinn_tensor *output, struct csinn_gather_params *params);

int shl_rvv_strided_slice_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                               struct csinn_strided_slice_params *params);

int shl_rvv_expand_dims_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_expand_dims_params *params);
int shl_rvv_expand_dims_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_expand_dims_params *params);

/************************************ basic math *********************************/
int shl_rvv_add_fp32(struct csinn_tensor *input0, struct csinn_tensor *input1,
                     struct csinn_tensor *output, struct csinn_diso_params *params);
int shl_rvv_add_fp16(struct csinn_tensor *input0, struct csinn_tensor *input1,
                     struct csinn_tensor *output, struct csinn_diso_params *params);
int shl_rvv_add_int8(struct csinn_tensor *input0, struct csinn_tensor *input1,
                     struct csinn_tensor *output, struct csinn_diso_params *params);

int shl_rvv_sub_fp32(struct csinn_tensor *input0, struct csinn_tensor *input1,
                     struct csinn_tensor *output, struct csinn_diso_params *params);
int shl_rvv_sub_fp16(struct csinn_tensor *input0, struct csinn_tensor *input1,
                     struct csinn_tensor *output, struct csinn_diso_params *params);
int shl_rvv_sub_int8(struct csinn_tensor *input0, struct csinn_tensor *input1,
                     struct csinn_tensor *output, struct csinn_diso_params *params);

int shl_rvv_mul_fp32(struct csinn_tensor *input0, struct csinn_tensor *input1,
                     struct csinn_tensor *output, struct csinn_diso_params *params);
int shl_rvv_mul_fp16(struct csinn_tensor *input0, struct csinn_tensor *input1,
                     struct csinn_tensor *output, struct csinn_diso_params *params);
int shl_rvv_mul_int8(struct csinn_tensor *input0, struct csinn_tensor *input1,
                     struct csinn_tensor *output, struct csinn_diso_params *params);

int shl_rvv_div_fp32(struct csinn_tensor *input0, struct csinn_tensor *input1,
                     struct csinn_tensor *output, struct csinn_diso_params *params);
int shl_rvv_div_fp16(struct csinn_tensor *input0, struct csinn_tensor *input1,
                     struct csinn_tensor *output, struct csinn_diso_params *params);
int shl_rvv_div_int8(struct csinn_tensor *input0, struct csinn_tensor *input1,
                     struct csinn_tensor *output, struct csinn_diso_params *params);

int shl_rvv_reduce_sum_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                            struct csinn_reduce_params *params);

int shl_rvv_erf_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                     struct csinn_siso_params *params);
int shl_rvv_erf_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                     struct csinn_siso_params *params);
int shl_rvv_erf_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                     struct csinn_siso_params *params);

/******************************** normalization *****************************/
int shl_rvv_layer_norm_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                            struct csinn_tensor *gamma, struct csinn_tensor *beta,
                            struct csinn_layer_norm_params *params);
int shl_rvv_layer_norm_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                            struct csinn_tensor *gamma, struct csinn_tensor *beta,
                            struct csinn_layer_norm_params *params);
int shl_rvv_layer_norm_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                            struct csinn_tensor *gamma, struct csinn_tensor *beta,
                            struct csinn_layer_norm_params *params);

int shl_rvv_group_norm_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                            struct csinn_tensor *gamma, struct csinn_tensor *beta,
                            struct csinn_group_norm_params *params);
int shl_rvv_group_norm_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                            struct csinn_tensor *gamma, struct csinn_tensor *beta,
                            struct csinn_group_norm_params *params);
int shl_rvv_group_norm_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                            struct csinn_tensor *gamma, struct csinn_tensor *beta,
                            struct csinn_group_norm_params *params);

int shl_rvv_batch_normalization_fp32(struct csinn_tensor *input, struct csinn_tensor *mean,
                                     struct csinn_tensor *variance, struct csinn_tensor *gamma,
                                     struct csinn_tensor *beta, struct csinn_tensor *output,
                                     struct csinn_bn_params *params);
int shl_rvv_batch_normalization_fp16(struct csinn_tensor *input, struct csinn_tensor *mean,
                                     struct csinn_tensor *variance, struct csinn_tensor *gamma,
                                     struct csinn_tensor *beta, struct csinn_tensor *output,
                                     struct csinn_bn_params *params);
int shl_rvv_batch_normalization_int8(struct csinn_tensor *input, struct csinn_tensor *mean,
                                     struct csinn_tensor *variance, struct csinn_tensor *gamma,
                                     struct csinn_tensor *beta, struct csinn_tensor *output,
                                     struct csinn_bn_params *params);

int shl_rvv_instance_norm_fp32(struct csinn_tensor *input, struct csinn_tensor *mean,
                               struct csinn_tensor *variance, struct csinn_tensor *gamma,
                               struct csinn_tensor *beta, struct csinn_tensor *output,
                               struct csinn_instance_norm_params *params);
int shl_rvv_instance_norm_fp16(struct csinn_tensor *input, struct csinn_tensor *mean,
                               struct csinn_tensor *variance, struct csinn_tensor *gamma,
                               struct csinn_tensor *beta, struct csinn_tensor *output,
                               struct csinn_instance_norm_params *params);
int shl_rvv_instance_norm_int8(struct csinn_tensor *input, struct csinn_tensor *mean,
                               struct csinn_tensor *variance, struct csinn_tensor *gamma,
                               struct csinn_tensor *beta, struct csinn_tensor *output,
                               struct csinn_instance_norm_params *params);

int shl_rvv_rms_norm_fp32(struct csinn_tensor *input, struct csinn_tensor *weight,
                          struct csinn_tensor *output, struct csinn_rms_norm_params *params);
int shl_rvv_rms_norm_fp16(struct csinn_tensor *input, struct csinn_tensor *weight,
                          struct csinn_tensor *output, struct csinn_rms_norm_params *params);
int shl_rvv_rms_norm_int8(struct csinn_tensor *input, struct csinn_tensor *weight,
                          struct csinn_tensor *output, struct csinn_rms_norm_params *params);

/*********************************** matmul *********************************/
int shl_rvv_common_matmul_a0b0_block_fp32(
    struct csinn_tensor *mat0, struct csinn_tensor *mat1, struct csinn_tensor *output,
    struct csinn_matmul_params *params, const int M_BLK, const int K_BLK, const int N_BLK,
    void (*reorder_a)(float *, float *, int, int, int, int),
    void (*reorder_b)(float *, float *, int, int, int, int),
    void (*gemm)(float *, const float *, const float *, float *, int, int, int, int, int, int));
int shl_rvv_common_matmul_a0b0_block_fp16(
    struct csinn_tensor *mat0, struct csinn_tensor *mat1, struct csinn_tensor *output,
    struct csinn_matmul_params *params, const int M_BLK, const int K_BLK, const int N_BLK,
    void (*reorder_a)(__fp16 *, __fp16 *, int, int, int, int),
    void (*reorder_b)(__fp16 *, __fp16 *, int, int, int, int),
    void (*gemm)(__fp16 *, const __fp16 *, const __fp16 *, __fp16 *, int, int, int, int, int, int));
int shl_rvv_common_matmul_a0b0_block_fp16_w_int8(
    struct csinn_tensor *mat0, struct csinn_tensor *mat1, struct csinn_tensor *output,
    struct csinn_matmul_params *params, const int M_BLK, const int K_BLK, const int N_BLK,
    void (*reorder_a)(__fp16 *, __fp16 *, int, int, int, int),
    void (*gemm)(__fp16 *, const __fp16 *, const __fp16 *, __fp16 *, int, int, int, int, int, int));

int shl_rvv_common_matmul_a0b0_fp32(struct csinn_tensor *mat0, struct csinn_tensor *mat1,
                                    struct csinn_tensor *output, struct csinn_matmul_params *params,
                                    void (*reorder_a)(float *, float *, int, int, int),
                                    void (*reorder_b)(float *, float *, int, int, int),
                                    void (*gemm)(float *, const float *, const float *, float *,
                                                 int, int, int, int));
int shl_rvv_common_matmul_a0b0_fp16(struct csinn_tensor *mat0, struct csinn_tensor *mat1,
                                    struct csinn_tensor *output, struct csinn_matmul_params *params,
                                    void (*reorder_a)(__fp16 *, __fp16 *, int, int, int),
                                    void (*reorder_b)(__fp16 *, __fp16 *, int, int, int),
                                    void (*gemm)(__fp16 *, const __fp16 *, const __fp16 *, __fp16 *,
                                                 int, int, int, int));
int shl_rvv_common_matmul_a0b0_fp16_w_int8(
    struct csinn_tensor *mat0, struct csinn_tensor *mat1, struct csinn_tensor *output,
    struct csinn_matmul_params *params, void (*reorder_a)(__fp16 *, __fp16 *, int, int, int),
    void (*gemm)(__fp16 *, const __fp16 *, const __fp16 *, __fp16 *, int, int, int, int));
int shl_rvv_common_matmul_a0b0_int8(struct csinn_tensor *mat0, struct csinn_tensor *mat1,
                                    struct csinn_tensor *output, struct csinn_matmul_params *params,
                                    void (*reorder_mat0)(int8_t *, int8_t *, int, int, int),
                                    void (*reorder_mat1)(int8_t *, int8_t *, int, int, int),
                                    void (*matmul)(int8_t *, const int8_t *, const int8_t *, int,
                                                   int, int, int, int32_t, int32_t, int32_t,
                                                   int32_t, int32_t));

int shl_rvv_common_matmul_a0b1_fp32(struct csinn_tensor *mat0, struct csinn_tensor *mat1,
                                    struct csinn_tensor *output, struct csinn_matmul_params *params,
                                    void (*reorder_b)(float *, float *, int, int),
                                    void (*gemm)(float *, const float *, const float *, float *,
                                                 int, int, int));
int shl_rvv_common_matmul_a0b1_fp16(struct csinn_tensor *mat0, struct csinn_tensor *mat1,
                                    struct csinn_tensor *output, struct csinn_matmul_params *params,
                                    void (*reorder_b)(__fp16 *, __fp16 *, int, int),
                                    void (*gemm)(__fp16 *, const __fp16 *, const __fp16 *, __fp16 *,
                                                 int, int, int));

int shl_rvv_common_matmul_a0b1_fp32_block_quant(
    struct csinn_tensor *mat0, struct csinn_tensor *mat1, struct csinn_tensor *output,
    struct csinn_matmul_params *params,
    void (*gemm_fp32_q8)(float *, const float *, const int8_t *, float *, int, int, int,
                         const __fp16 *),
    void (*gemm_fp32_q4)(float *, const float *, const int8_t *, float *, int, int, int,
                         const __fp16 *));
int shl_rvv_common_matmul_a0b1_fp16_block_quant(
    struct csinn_tensor *mat0, struct csinn_tensor *mat1, struct csinn_tensor *output,
    struct csinn_matmul_params *params,
    void (*gemm_fp16_q8)(__fp16 *, const __fp16 *, const int8_t *, __fp16 *, int, int, int,
                         const __fp16 *),
    void (*gemm_fp16_q4)(__fp16 *, const __fp16 *, const int8_t *, __fp16 *, int, int, int,
                         const __fp16 *));

void shl_rvv_matmul_reorder_mat0_n4_int8(int8_t *src, int8_t *dst, int m, int k, int lda);
void shl_rvv_matmul_reorder_mat1_zpackn_int8(int8_t *src, int8_t *dst, int k, int n, int ldb);
void shl_rvv_matmul_4xpackn_int8(int8_t *dst, const int8_t *sa, const int8_t *sb, int m, int k,
                                 int n, int ldc, int32_t z1, int32_t z2, int32_t z3, int32_t mult,
                                 int32_t shift);

void shl_rvv_matmul_reorder_mat0_n8z4_int8_dot(int8_t *src, int8_t *dst, int m, int k, int lda);
void shl_rvv_matmul_reorder_mat1_zmf2n4_int8_dot(int8_t *src, int8_t *dst, int k, int n, int ldb);
void shl_rvv_matmul_8xmf2_int8_dot(int8_t *dst, const int8_t *sa, const int8_t *sb, int m, int k,
                                   int n, int ldc, int32_t z1, int32_t z2, int32_t z3, int32_t mult,
                                   int32_t shift);

void shl_rvv_matmul_block_reorder_weight_fp32(struct csinn_tensor *mat1, const int K_BLK,
                                              const int N_BLK);
void shl_rvv_matmul_block_reorder_weight_fp16(struct csinn_tensor *mat1, const int K_BLK,
                                              const int N_BLK);
void shl_rvv_matmul_block_reorder_weight_fp16_w_int8(struct csinn_tensor *mat1, const int K_BLK,
                                                     const int N_BLK);

int shl_rvv_matmul_a0b0_block_fp32(struct csinn_tensor *mat0, struct csinn_tensor *mat1,
                                   struct csinn_tensor *output, struct csinn_matmul_params *params);
int shl_rvv_matmul_a0b0_block_fp16(struct csinn_tensor *mat0, struct csinn_tensor *mat1,
                                   struct csinn_tensor *output, struct csinn_matmul_params *params);
int shl_rvv_matmul_a0b0_block_fp16_w_int8(struct csinn_tensor *mat0, struct csinn_tensor *mat1,
                                          struct csinn_tensor *output,
                                          struct csinn_matmul_params *params);

void shl_rvv_matmul_reorder_weight_fp32(struct csinn_tensor *mat1);
void shl_rvv_matmul_reorder_weight_fp16(struct csinn_tensor *mat1);
void shl_rvv_matmul_reorder_weight_fp16_w_int8(struct csinn_tensor *mat1);
void shl_rvv_matmul_reorder_weight_int8(struct csinn_tensor *mat0, struct csinn_tensor *mat1);

int shl_rvv_matmul_a0b0_fp32(struct csinn_tensor *mat0, struct csinn_tensor *mat1,
                             struct csinn_tensor *output, struct csinn_matmul_params *params);
int shl_rvv_matmul_a0b0_fp16(struct csinn_tensor *mat0, struct csinn_tensor *mat1,
                             struct csinn_tensor *output, struct csinn_matmul_params *params);
int shl_rvv_matmul_a0b0_fp16_w_int8(struct csinn_tensor *mat0, struct csinn_tensor *mat1,
                                    struct csinn_tensor *output,
                                    struct csinn_matmul_params *params);
int shl_rvv_matmul_a0b0_int8(struct csinn_tensor *mat0, struct csinn_tensor *mat1,
                             struct csinn_tensor *output, struct csinn_matmul_params *params);

int shl_rvv_matmul_a0b1_fp32(struct csinn_tensor *mat0, struct csinn_tensor *mat1,
                             struct csinn_tensor *output, struct csinn_matmul_params *params);
int shl_rvv_matmul_a0b1_fp16(struct csinn_tensor *mat0, struct csinn_tensor *mat1,
                             struct csinn_tensor *output, struct csinn_matmul_params *params);

int shl_rvv_matmul_a0b1_fp16_block_quant_rearrange(struct csinn_tensor *mat0,
                                                   struct csinn_tensor *mat1,
                                                   struct csinn_tensor *output,
                                                   struct csinn_matmul_params *params);

/******************************** llm *****************************/
int shl_rvv_embedding_int32(struct csinn_tensor *input, struct csinn_tensor *weight,
                            struct csinn_tensor *output, struct csinn_diso_params *params);

int shl_rvv_rope_fp32(struct csinn_tensor *input, struct csinn_tensor *output,
                      struct csinn_rope_params *params);
int shl_rvv_rope_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                      struct csinn_rope_params *params);

int shl_rvv_llm_pos_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                         struct csinn_llm_pos_params *params);

int shl_rvv_scaled_dot_product_attention_fp32(struct csinn_tensor *query, struct csinn_tensor *key,
                                              struct csinn_tensor *value,
                                              struct csinn_tensor *output_tensor,
                                              struct csinn_scale_dot_attention_params *params);
int shl_rvv_scaled_dot_product_attention_fp16(struct csinn_tensor *query, struct csinn_tensor *key,
                                              struct csinn_tensor *value,
                                              struct csinn_tensor *output_tensor,
                                              struct csinn_scale_dot_attention_params *params);

/************************************ utils *********************************/
void shl_rvv_pad_input_fp32(const float *input, float *input_padded, int inc, int inh, int inw,
                            int padded_h, int padded_w, int pad_top, int pad_left);
void shl_rvv_pad_input_fp16(const __fp16 *input, __fp16 *input_padded, int inc, int inh, int inw,
                            int padded_h, int padded_w, int pad_top, int pad_left);
void shl_rvv_pad_input_int8(const int8_t *input, int8_t *input_padded, int inc, int inh, int inw,
                            int padded_h, int padded_w, int pad_top, int pad_left,
                            int8_t pad_value);

void shl_rvv_pad_input_packn_fp32(const float *input, float *input_padded, int inc, int inh,
                                  int inw, int padded_h, int padded_w, int pad_top, int pad_left);
void shl_rvv_pad_input_packn_fp16(const __fp16 *input, __fp16 *input_padded, int inc, int inh,
                                  int inw, int padded_h, int padded_w, int pad_top, int pad_left);
void shl_rvv_pad_input_packn_int8(const int8_t *input, int8_t *input_padded, int inc, int inh,
                                  int inw, int padded_h, int padded_w, int pad_top, int pad_left,
                                  int8_t pad_value);

void shl_rvv_pad_input_pack1ton_fp32(const float *input, float *input_padded, int inc, int inh,
                                     int inw, int padded_h, int padded_w, int pad_top,
                                     int pad_left);
void shl_rvv_pad_input_pack1ton_fp16(const __fp16 *input, __fp16 *input_padded, int inc, int inh,
                                     int inw, int padded_h, int padded_w, int pad_top,
                                     int pad_left);
void shl_rvv_pad_input_pack1ton_int8(const int8_t *input, int8_t *input_padded, int inc, int inh,
                                     int inw, int padded_h, int padded_w, int pad_top, int pad_left,
                                     int8_t pad_value);

void shl_rvv_pad_input_nhwc_fp32(const float *input, float *input_padded, int inh, int inw, int inc,
                                 int padded_h, int padded_w, int pad_top, int pad_left);
void shl_rvv_pad_input_nhwc_fp16(const __fp16 *input, __fp16 *input_padded, int inh, int inw,
                                 int inc, int padded_h, int padded_w, int pad_top, int pad_left);
void shl_rvv_pad_input_nhwc_int8(const int8_t *input, int8_t *input_padded, int inh, int inw,
                                 int inc, int padded_h, int padded_w, int pad_top, int pad_left,
                                 int8_t pad_value);

void shl_rvv_reorder_input_pack1ton_fp32(const float *src, float *dst, int inc, int inh, int inw);
void shl_rvv_reorder_input_pack1ton_fp16(const __fp16 *src, __fp16 *dst, int inc, int inh, int inw);
void shl_rvv_reorder_input_pack1ton_int8(const int8_t *src, int8_t *dst, int inc, int inh, int inw);
void shl_rvv_reorder_input_packnto1_fp32(const float *src, float *dst, int inc, int inh, int inw);
void shl_rvv_reorder_input_packnto1_fp16(const __fp16 *src, __fp16 *dst, int inc, int inh, int inw);
void shl_rvv_reorder_input_packnto1_int8(const int8_t *src, int8_t *dst, int inc, int inh, int inw);

void shl_rvv_saturated_int8(int32_t *src, int8_t *dst, int32_t out_zp, int size);

void shl_rvv_requantize_fp16(__fp16 *src, __fp16 scale, int size);
void shl_rvv_sidcso_op_requantize_fp16(struct csinn_tensor *input, struct csinn_tensor *output,
                                       struct csinn_tensor *kernel);
void shl_rvv_siso_op_requantize_fp16(struct csinn_tensor *input, struct csinn_tensor *output);
void shl_rvv_diso_op_requantize_fp16(struct csinn_tensor *input0, struct csinn_tensor *input1,
                                     struct csinn_tensor *output);

void shl_rvv_requantize(int32_t *src, int32_t multiplier, int32_t shift, int channel_size);

void shl_rvv_dequantize_i8_to_f16(int8_t *src, __fp16 *dst, int size, int32_t zp, float scale);
static inline vfloat16m2_t shl_rvv_vdeq_vv_f16m2(vint8m1_t _i8, vint8m1_t _z, vfloat16m2_t _s,
                                                 size_t vl)
{
    vint16m2_t _i16 = vwsub_vv_i16m2(_i8, _z, vl);
    vfloat16m2_t _f16 = vfcvt_f_x_v_f16m2(_i16, vl);
    _f16 = vfmul_vv_f16m2(_f16, _s, vl);
    return _f16;
}

void shl_rvv_reorder_kernel_n8_fp16_w_int8(int8_t *a, int8_t *sa, int m, int k, int ldx);

void shl_rvv_pad_input_int4_trans_int8(const int8_t *input, int8_t *input_padded, int inc, int inh,
                                       int inw, int padded_h, int padded_w, int pad_top,
                                       int pad_left, int8_t pad_value);
void shl_rvv_int4_to_int8(int8_t *src, int8_t *dst, int size);
void shl_rvv_int8_to_int4(int8_t *src, int8_t *dst, int size);
void shl_rvv_int4_trans_int8(int8_t *src, int8_t *dst, int size);
void shl_rvv_saturated_int4(int32_t *src, int8_t *dst, int32_t out_zp, int size);

int shl_rvv_tensor_data_convert(struct csinn_tensor *src, struct csinn_tensor *dst);
void shl_rvv_u8_to_i16(const uint8_t *input, int16_t *output, int32_t z1, float *s1, int32_t z2,
                       float *s2, uint32_t length);
void shl_rvv_i16_to_u8(const int16_t *input, uint8_t *output, int32_t z1, float *s1, int32_t z2,
                       float *s2, uint32_t length);
void shl_rvv_u8_to_f32(const uint8_t *input, float *output, int32_t offset, float *scale,
                       uint32_t length);
void shl_rvv_f32_to_u8(const float *input, uint8_t *output, int32_t offset, float *scale,
                       uint32_t length);
void shl_rvv_i8_to_f32(const int8_t *input, float *output, int32_t offset, float *scale,
                       uint32_t length);
void shl_rvv_f32_to_i8(const float *input, int8_t *output, int32_t offset, float *scale,
                       uint32_t length);
void shl_rvv_i16_to_f32(const int16_t *input, float *output, int32_t offset, float *scale,
                        uint32_t length);
void shl_rvv_f32_to_i16(const float *input, int16_t *output, int32_t offset, float *scale,
                        uint32_t length);
void shl_rvv_i32_to_f32(const int32_t *input, float *output, int32_t offset, float *scale,
                        uint32_t length);
void shl_rvv_f32_to_i32(const float *input, int32_t *output, int32_t offset, float *scale,
                        uint32_t length);
void shl_rvv_i64_to_f32(const int64_t *input, float *output, uint32_t length);
void shl_rvv_f32_to_i64(const float *input, int64_t *output, uint32_t length);
void shl_rvv_f16_to_f32(const __fp16 *input, float *output, float *scale, uint32_t length);
void shl_rvv_f32_to_f16(const float *input, __fp16 *output, float *scale, uint32_t length);

struct csinn_tensor *shl_rvv_tensor_transform_f32(struct csinn_tensor *input);
struct csinn_tensor *shl_rvv_tensor_transform_dtype_f32(struct csinn_tensor *input);
int shl_rvv_siso_callback_base(struct csinn_tensor *input, struct csinn_tensor *output,
                               void *params, void *cb);
int shl_rvv_siso_callback_dtype_only(struct csinn_tensor *input, struct csinn_tensor *output,
                                     void *params, void *cb);

int shl_rvv_data_convert_int8_to_int4(struct csinn_tensor *input, struct csinn_tensor *output,
                                      struct csinn_siso_params *params);
int shl_rvv_data_convert_int4_to_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                                      struct csinn_siso_params *params);

void shl_rvv_tensor_ndarray_to_nc1xc0_replace_fp32(struct csinn_tensor *t);
void shl_rvv_tensor_ndarray_to_nc1xc0_replace_fp16(struct csinn_tensor *t);
void shl_rvv_tensor_ndarray_to_nc1xc0_replace_int8(struct csinn_tensor *t);
void shl_rvv_tensor_nc1xc0_to_ndarray_replace_fp32(struct csinn_tensor *t);
void shl_rvv_tensor_nc1xc0_to_ndarray_replace_fp16(struct csinn_tensor *t);
void shl_rvv_tensor_nc1xc0_to_ndarray_replace_int8(struct csinn_tensor *t);

void shl_rvv_tensor_ndarray_to_nc1xc0_inplace_fp32(struct csinn_tensor *t);
void shl_rvv_tensor_ndarray_to_nc1xc0_inplace_fp16(struct csinn_tensor *t);
void shl_rvv_tensor_ndarray_to_nc1xc0_inplace_int8(struct csinn_tensor *t);
void shl_rvv_tensor_nc1xc0_to_ndarray_inplace_fp32(struct csinn_tensor *t);
void shl_rvv_tensor_nc1xc0_to_ndarray_inplace_fp16(struct csinn_tensor *t);
void shl_rvv_tensor_nc1xc0_to_ndarray_inplace_int8(struct csinn_tensor *t);

void shl_rvv_nc1xc0_fp16_to_nchw_fp32(struct csinn_tensor *dest, struct csinn_tensor *src);

struct csinn_callback *shl_cb_map_rvv(int op, int dtype);
void shl_rvv_reg_op(enum csinn_dtype_enum dtype, enum csinn_op_enum op_name, void *init, void *exec,
                    void *est, void *cap, void *perf);

int csrr_vl();
int csrr_vlenb();

enum avgpool_loc_enum {
    AVGPOOL_LEFT_TOP = 0,
    AVGPOOL_RIGHT_TOP,
    AVGPOOL_LEFT_BOTTOM,
    AVGPOOL_RIGHT_BOTTOM,
    AVGPOOL_LEFT,
    AVGPOOL_RIGHT,
    AVGPOOL_TOP,
    AVGPOOL_BOTTOM,
    AVGPOOL_CENTER,
};

int shl_rvv_avgpool_get_window_size(struct csinn_pool_params *params, int idx_h_start,
                                    int idx_h_end, int idx_w_start, int idx_w_end,
                                    enum avgpool_loc_enum loc);

void shl_rvv_conv1d_gemm_reorder_kernel_int8(struct csinn_tensor *kernel,
                                             struct csinn_conv1d_params *params);
int shl_rvv_conv1d_gemm_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_tensor *kernel, struct csinn_tensor *bias,
                             struct csinn_conv1d_params *params);

int shl_rvv_dwconv1d_int8(struct csinn_tensor *input, struct csinn_tensor *output,
                          struct csinn_tensor *kernel, struct csinn_tensor *bias,
                          struct csinn_conv1d_params *params);

int shl_rvv_transpose_get_tail(int32_t *permute, int32_t permute_num);
int shl_rvv_transpose_get_in_index(int32_t *dim, int32_t *idx, int32_t dim_count);
int shl_rvv_transpose_get_out_index(int32_t *dim, int32_t *idx, int32_t *permute,
                                    int32_t dim_count);

int shl_rvv_binary_op_broadcast_fp32(struct csinn_tensor *input0, struct csinn_tensor *input1,
                                     struct csinn_tensor *output, void *binary_op_callback[]);
int shl_rvv_binary_op_broadcast_fp16(struct csinn_tensor *input0, struct csinn_tensor *input1,
                                     struct csinn_tensor *output, void *binary_op_callback[]);
int shl_rvv_binary_op_broadcast_int8(struct csinn_tensor *input0, struct csinn_tensor *input1,
                                     struct csinn_tensor *output, void *binary_op_callback[]);

#ifdef SHL_USE_DOT_INT4
int shl_rvv_conv2d_init_int4(struct csinn_tensor *input, struct csinn_tensor *output,
                             struct csinn_tensor *kernel, struct csinn_tensor *bias,
                             struct csinn_conv2d_params *params);
void shl_rvv_conv_im2col_gemm_reorder_kernel_int4(struct csinn_tensor *kernel,
                                                  struct csinn_conv2d_params *params);
int shl_rvv_conv_im2col_gemm_int4(struct csinn_tensor *input, struct csinn_tensor *output,
                                  struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                  struct csinn_conv2d_params *params);
void shl_rvv_conv_im2col_gemm_reorder_kernel_packn_int4(struct csinn_tensor *kernel,
                                                        struct csinn_conv2d_params *params);
int shl_rvv_conv_im2col_gemm_packn_int4(struct csinn_tensor *input, struct csinn_tensor *output,
                                        struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                        struct csinn_conv2d_params *params);
void shl_rvv_conv1x1s1_gemm_reorder_kernel_int4(struct csinn_tensor *kernel,
                                                struct csinn_conv2d_params *params);
int shl_rvv_conv1x1s1_gemm_int4(struct csinn_tensor *input, struct csinn_tensor *output,
                                struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                struct csinn_conv2d_params *params);
void shl_rvv_conv1x1s1_gemm_reorder_kernel_packn_int4(struct csinn_tensor *kernel,
                                                      struct csinn_conv2d_params *params);
int shl_rvv_conv1x1s1_gemm_packn_int4(struct csinn_tensor *input, struct csinn_tensor *output,
                                      struct csinn_tensor *kernel, struct csinn_tensor *bias,
                                      struct csinn_conv2d_params *params);
void shl_rvv_fc_gemv_transform_weight_int4_dot(struct csinn_tensor *weights);
int shl_rvv_fullyconnected_packn_int4_dot(struct csinn_tensor *input, struct csinn_tensor *output,
                                          struct csinn_tensor *weights, struct csinn_tensor *bias,
                                          struct csinn_fc_params *params);
#endif

struct shl_rvv_option {
    bool use_packn_layout;
    bool binary_model_op_init;
};

struct shl_rvv_option *shl_rvv_get_graph_option(struct csinn_session *sess);
bool shl_rvv_get_binary_model_op_init(struct csinn_session *sess);

#ifdef __cplusplus
}
#endif

#endif  // INCLUDE_SHL_RVV_H_

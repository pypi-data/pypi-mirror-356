/*
 * Copyright (C) 2017-2024 Alibaba Group Holding Limited
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/// @file

#ifndef INCLUDE_XNNL_REF_H_
#define INCLUDE_XNNL_REF_H_

#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @defgroup REF Reference
 * @{
 */

/**
 * @defgroup REF_ACTIVATION Activation Functions
 * @{
 */

/*********************************** activation *********************************/

/**
 * @brief       Softmax function
 *
 * @param[in]   input           Pointer to the input data
 * @param[out]  output          Pointer to the output data
 * @param[in]   shape           Shape of the input and output
 * @param[in]   dim             Number of dimensions of input and output
 * @param[in]   axis            Used to specify which dimension the operation is performed along
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_softmax_fp32(float *input, float *output, int32_t *shape, int32_t dim, int32_t axis);

/**
 * @brief       Softmax function
 *
 * @param[in]   input           Pointer to the input data
 * @param[out]  output          Pointer to the output data
 * @param[in]   shape           Shape of the input and output
 * @param[in]   dim             Number of dimensions of input and output
 * @param[in]   axis            Used to specify which dimension the operation is performed along
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_softmax_fp16(__fp16 *input, __fp16 *output, int32_t *shape, int32_t dim, int32_t axis);

/**
 * @brief       Silu function
 *
 * @param[in]   input   Pointer to the input data
 * @param[out]  output  Pointer to the output data
 * @param[in]   size    Size of input and output
 * @return      Returns 0 on success; returns 1 or greater on error.
 */
int xnnl_ref_silu_fp32(float *input, float *output, int32_t size);

/**
 * @brief       Silu function
 *
 * @param[in]   input   Pointer to the input data
 * @param[out]  output  Pointer to the output data
 * @param[in]   size    Size of input and output
 * @return      Returns 0 on success; returns 1 or greater on error.
 */
int xnnl_ref_silu_fp16(__fp16 *input, __fp16 *output, int32_t size);
/**
 * @}
 */

/**
 * @defgroup REF_BINARY Binary Functions
 * @{
 */

/*********************************** binary *********************************/

/**
 * @brief       Add function
 *
 * @param[in]   input0      Pointer to the input0 data
 * @param[in]   input1      Pointer to the input1 data
 * @param[out]  output      Pointer to the output data
 * @param[in]   shape_in0   Shape of the input0
 * @param[in]   dim_in0     Number of dimensions of input0
 * @param[in]   shape_in1   Shape of the input1
 * @param[in]   dim_in1     Number of dimensions of input1
 * @param[in]   shape_out   Shape of the output
 * @param[in]   dim_out     Number of dimensions of output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_add_fp32(float *input0, float *input1, float *output, int32_t *shape_in0,
                      int32_t dim_in0, int32_t *shape_in1, int32_t dim_in1, int32_t *shape_out,
                      int32_t dim_out);

/**
 * @brief       Add function
 *
 * @param[in]   input0      Pointer to the input0 data
 * @param[in]   input1      Pointer to the input1 data
 * @param[out]  output      Pointer to the output data
 * @param[in]   shape_in0   Shape of the input0
 * @param[in]   dim_in0     Number of dimensions of input0
 * @param[in]   shape_in1   Shape of the input1
 * @param[in]   dim_in1     Number of dimensions of input1
 * @param[in]   shape_out   Shape of the output
 * @param[in]   dim_out     Number of dimensions of output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_add_fp16(__fp16 *input0, __fp16 *input1, __fp16 *output, int32_t *shape_in0,
                      int32_t dim_in0, int32_t *shape_in1, int32_t dim_in1, int32_t *shape_out,
                      int32_t dim_out);

/**
 * @brief       Sub function
 *
 * @param[in]   input0      Pointer to the input0 data
 * @param[in]   input1      Pointer to the input1 data
 * @param[out]  output      Pointer to the output data
 * @param[in]   shape_in0   Shape of the input0
 * @param[in]   dim_in0     Number of dimensions of input0
 * @param[in]   shape_in1   Shape of the input1
 * @param[in]   dim_in1     Number of dimensions of input1
 * @param[in]   shape_out   Shape of the output
 * @param[in]   dim_out     Number of dimensions of output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_sub_fp32(float *input0, float *input1, float *output, int32_t *shape_in0,
                      int32_t dim_in0, int32_t *shape_in1, int32_t dim_in1, int32_t *shape_out,
                      int32_t dim_out);

/**
 * @brief       Sub function
 *
 * @param[in]   input0      Pointer to the input0 data
 * @param[in]   input1      Pointer to the input1 data
 * @param[out]  output      Pointer to the output data
 * @param[in]   shape_in0   Shape of the input0
 * @param[in]   dim_in0     Number of dimensions of input0
 * @param[in]   shape_in1   Shape of the input1
 * @param[in]   dim_in1     Number of dimensions of input1
 * @param[in]   shape_out   Shape of the output
 * @param[in]   dim_out     Number of dimensions of output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_sub_fp16(__fp16 *input0, __fp16 *input1, __fp16 *output, int32_t *shape_in0,
                      int32_t dim_in0, int32_t *shape_in1, int32_t dim_in1, int32_t *shape_out,
                      int32_t dim_out);

/**
 * @brief       Mul function
 *
 * @param[in]   input0      Pointer to the input0 data
 * @param[in]   input1      Pointer to the input1 data
 * @param[out]  output      Pointer to the output data
 * @param[in]   shape_in0   Shape of the input0
 * @param[in]   dim_in0     Number of dimensions of input0
 * @param[in]   shape_in1   Shape of the input1
 * @param[in]   dim_in1     Number of dimensions of input1
 * @param[in]   shape_out   Shape of the output
 * @param[in]   dim_out     Number of dimensions of output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_mul_fp32(float *input0, float *input1, float *output, int32_t *shape_in0,
                      int32_t dim_in0, int32_t *shape_in1, int32_t dim_in1, int32_t *shape_out,
                      int32_t dim_out);

/**
 * @brief       Mul function
 *
 * @param[in]   input0      Pointer to the input0 data
 * @param[in]   input1      Pointer to the input1 data
 * @param[out]  output      Pointer to the output data
 * @param[in]   shape_in0   Shape of the input0
 * @param[in]   dim_in0     Number of dimensions of input0
 * @param[in]   shape_in1   Shape of the input1
 * @param[in]   dim_in1     Number of dimensions of input1
 * @param[in]   shape_out   Shape of the output
 * @param[in]   dim_out     Number of dimensions of output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_mul_fp16(__fp16 *input0, __fp16 *input1, __fp16 *output, int32_t *shape_in0,
                      int32_t dim_in0, int32_t *shape_in1, int32_t dim_in1, int32_t *shape_out,
                      int32_t dim_out);

/**
 * @brief       Div function
 *
 * @param[in]   input0      Pointer to the input0 data
 * @param[in]   input1      Pointer to the input1 data
 * @param[out]  output      Pointer to the output data
 * @param[in]   shape_in0   Shape of the input0
 * @param[in]   dim_in0     Number of dimensions of input0
 * @param[in]   shape_in1   Shape of the input1
 * @param[in]   dim_in1     Number of dimensions of input1
 * @param[in]   shape_out   Shape of the output
 * @param[in]   dim_out     Number of dimensions of output
 * @return      Returns 0 on success; returns 1 or greater on error.
 */
int xnnl_ref_div_fp32(float *input0, float *input1, float *output, int32_t *shape_in0,
                      int32_t dim_in0, int32_t *shape_in1, int32_t dim_in1, int32_t *shape_out,
                      int32_t dim_out);

/**
 * @brief       Div function
 *
 * @param[in]   input0      Pointer to the input0 data
 * @param[in]   input1      Pointer to the input1 data
 * @param[out]  output      Pointer to the output data
 * @param[in]   shape_in0   Shape of the input0
 * @param[in]   dim_in0     Number of dimensions of input0
 * @param[in]   shape_in1   Shape of the input1
 * @param[in]   dim_in1     Number of dimensions of input1
 * @param[in]   shape_out   Shape of the output
 * @param[in]   dim_out     Number of dimensions of output
 * @return      Returns 0 on success; returns 1 or greater on error.
 */
int xnnl_ref_div_fp16(__fp16 *input0, __fp16 *input1, __fp16 *output, int32_t *shape_in0,
                      int32_t dim_in0, int32_t *shape_in1, int32_t dim_in1, int32_t *shape_out,
                      int32_t dim_out);
/**
 * @}
 */

/**
 * @defgroup OTHERS Others Functions
 * @{
 */

/*********************************** others *********************************/

/**
 * @brief       Cast function
 *
 * @param[in]   input    Pointer to the input data
 * @param[out]  output   Pointer to the output data
 * @param[in]   size     Size of input and output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_cast_int_to_float_fp32(int32_t *input, float *output, int32_t size);

/**
 * @brief       Cast function
 *
 * @param[in]   input    Pointer to the input data
 * @param[out]  output   Pointer to the output data
 * @param[in]   size     Size of input and output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_cast_uint_to_float_fp32(uint32_t *input, float *output, int32_t size);

/**
 * @brief compare function
 *
 * @param[in]   input0      Pointer to the input0 data
 * @param[in]   input1      Pointer to the input1 data
 * @param[out]  output      Pointer to the output data
 * @param[in]   shape_in0   Shape of the input0
 * @param[in]   dim_in0     Number of dimensions of input0
 * @param[in]   shape_in1   Shape of the input1
 * @param[in]   dim_in1     Number of dimensions of input1
 * @param[in]   shape_out   Shape of the output
 * @param[in]   dim_out     Number of dimensions of output
 * @param[in]   type        The type of compare, equal--0, not equal--1, less than--2, less than or
 * equal--3, greater than--4, greater than or equal--5
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_compare_fp32(float *input0, float *input1, float *output, int32_t *shape_in0,
                          int32_t dim_in0, int32_t *shape_in1, int32_t dim_in1, int32_t *shape_out,
                          int32_t dim_out, int32_t type);

/**
 * @brief compare function
 *
 * @param[in]   input0      Pointer to the input0 data
 * @param[in]   input1      Pointer to the input1 data
 * @param[out]  output      Pointer to the output data
 * @param[in]   shape_in0   Shape of the input0
 * @param[in]   dim_in0     Number of dimensions of input0
 * @param[in]   shape_in1   Shape of the input1
 * @param[in]   dim_in1     Number of dimensions of input1
 * @param[in]   shape_out   Shape of the output
 * @param[in]   dim_out     Number of dimensions of output
 * @param[in]   type        The type of compare, equal--0, not equal--1, less than--2, less than or
 * equal--3, greater than--4, greater than or equal--5
 *
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_compare_fp16(__fp16 *input0, __fp16 *input1, __fp16 *output, int32_t *shape_in0,
                          int32_t dim_in0, int32_t *shape_in1, int32_t dim_in1, int32_t *shape_out,
                          int32_t dim_out, int32_t type);
/**
 * @}
 */

/**
 * @defgroup REF_INDEXING Indexing Functions
 * @{
 */

/*********************************** indexing *********************************/

/**
 * @brief       Transpose function
 *
 * @param[in]   input       Pointer to the input data
 * @param[out]  output      Pointer to the output data
 * @param[in]   shape_i     Shape of the input
 * @param[in]   shape_o     Shape of the output
 * @param[in]   dim         Number of dimensions of input and output
 * @param[in]   permute     Describe how to transpose
 * @return      Returns 0 on success; returns 1 or greater on error.
 */
int xnnl_ref_transpose_fp32(float *input, float *output, int32_t *shape_i, int32_t *shape_o,
                            int32_t dim, int32_t *permute);

/**
 * @brief       Transpose function
 *
 * @param[in]   input       Pointer to the input data
 * @param[out]  output      Pointer to the output data
 * @param[in]   shape_i     Shape of the input
 * @param[in]   shape_o     Shape of the output
 * @param[in]   dim         Number of dimensions of input and output
 * @param[in]   permute     Describe how to transpose
 * @return      Returns 0 on success; returns 1 or greater on error.
 */
int xnnl_ref_transpose_fp16(__fp16 *input, __fp16 *output, int32_t *shape_i, int32_t *shape_o,
                            int32_t dim, int32_t *permute);

/**
 * @brief       Split function
 *
 * @param[in]   input       Pointer to the input data
 * @param[out]  output      Output Pointer to an array of output data pointers
 * @param[in]   shape       Shape of the input and output
 * @param[in]   dim         Number of dimensions of input and output
 * @param[in]   split_index Pointer to the split data
 * @param[in]   split_num   Number of split
 * @param[in]   axis        Used to specify which dimension the operation is performed along
 * @return      Returns 0 on success; returns 1 or greater on error.
 */
int xnnl_ref_split_fp32(float *input, float **output, int32_t *shape, int32_t dim,
                        int32_t *split_index, int32_t split_num, int32_t axis);

/**
 * @brief       Split function
 *
 * @param[in]   input       Pointer to the input data
 * @param[out]  output      Output Pointer to an array of output data pointers
 * @param[in]   shape       Shape of the input and output
 * @param[in]   dim         Number of dimensions of input and output
 * @param[in]   split_index Pointer to the split data
 * @param[in]   split_num   Number of split
 * @param[in]   axis        Used to specify which dimension the operation is performed along
 * @return      Returns 0 on success; returns 1 or greater on error.
 */
int xnnl_ref_split_fp16(__fp16 *input, __fp16 **output, int32_t *shape, int32_t dim,
                        int32_t *split_index, int32_t split_num, int32_t axis);

/**
 * @brief       Where function
 *
 * @param[in]   condition    Pointer to the condition data
 * @param[in]   x            Pointer to the x data
 * @param[in]   y            Pointer to the y data
 * @param[out]  output       Pointer to the output data
 * @param[in]   shape_c      Shape of the condition
 * @param[in]   dim_c        Number of dimensions of condition
 * @param[in]   shape_x      Shape of the x
 * @param[in]   dim_x        Number of dimensions of x
 * @param[in]   shape_y      Shape of the y
 * @param[in]   dim_y        Number of dimensions of y
 * @param[in]   shape_o      Shape of the output
 * @param[in]   dim_o        Number of dimensions of output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_where_fp32(float *condition, float *x, float *y, float *output, int32_t *shape_c,
                        int32_t dim_c, int32_t *shape_x, int32_t dim_x, int32_t *shape_y,
                        int32_t dim_y, int32_t *shape_o, int32_t dim_o);

/**
 * @brief       Where function
 *
 * @param[in]   condition    Pointer to the condition data
 * @param[in]   x            Pointer to the x data
 * @param[in]   y            Pointer to the y data
 * @param[out]  output       Pointer to the output data
 * @param[in]   shape_c      Shape of the condition
 * @param[in]   dim_c        Number of dimensions of condition
 * @param[in]   shape_x      Shape of the x
 * @param[in]   dim_x        Number of dimensions of x
 * @param[in]   shape_y      Shape of the y
 * @param[in]   dim_y        Number of dimensions of y
 * @param[in]   shape_o      Shape of the output
 * @param[in]   dim_o        Number of dimensions of output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_where_fp16(__fp16 *condition, __fp16 *x, __fp16 *y, __fp16 *output, int32_t *shape_c,
                        int32_t dim_c, int32_t *shape_x, int32_t dim_x, int32_t *shape_y,
                        int32_t dim_y, int32_t *shape_o, int32_t dim_o);

/**
 * @brief       Gather function
 *
 * @param[in]   input           Pointer to the input data
 * @param[out]  output          Pointer to the output data
 * @param[in]   index           Pointer to the index data
 * @param[in]   shape           Shape of the input
 * @param[in]   dim             Number of dimensions of input and index
 * @param[in]   shape_idx       Shape of the index
 * @param[in]   axis            Used to specify which dimension the operation is performed along
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_gather_fp32(float *input, float *output, int32_t *index, int32_t *shape_in,
                         int32_t dim_in, int32_t *shape_idx, int32_t dim_idx, int32_t axis);

/**
 * @brief       Gather function
 *
 * @param[in]   input           Pointer to the input data
 * @param[out]  output          Pointer to the output data
 * @param[in]   index           Pointer to the index data
 * @param[in]   shape           Shape of the input
 * @param[in]   dim             Number of dimensions of input and index
 * @param[in]   shape_idx       Shape of the index
 * @param[in]   axis            Used to specify which dimension the operation is performed along
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_gather_fp16(__fp16 *input, __fp16 *output, int32_t *index, int32_t *shape_in,
                         int32_t dim_in, int32_t *shape_idx, int32_t dim_idx, int32_t axis);

/**
 * @brief       Slice function
 *
 * @param[in]   input           Pointer to the input data
 * @param[out]  output          Pointer to the output data
 * @param[in]   shape_i         Shape of the input
 * @param[in]   shape_o         Shape of the output,you can pass a buffer of size dim_i *
 * sizeof(int32_t).
 * @param[in]   dim_i           Number of dimensions of input and output
 * @param[in]   starts          Pointer to the start data
 * @param[in]   ends            Pointer to the end data
 * @param[in]   steps           Pointer to the step data
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_slice_fp32(float *input, float *output, int32_t *shape_i, int32_t *shape_o,
                        int32_t dim_i, int32_t *starts, int32_t *ends, int32_t *steps);

/**
 * @brief       Slice function
 *
 * @param[in]   input           Pointer to the input data
 * @param[out]  output          Pointer to the output data
 * @param[in]   shape_i         Shape of the input
 * @param[in]   shape_o         Shape of the output,you can pass a buffer of size dim_i *
 * sizeof(int32_t).
 * @param[in]   dim_i           Number of dimensions of input and output
 * @param[in]   starts          Pointer to the start data
 * @param[in]   ends            Pointer to the end data
 * @param[in]   steps           Pointer to the step data
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_slice_fp16(__fp16 *input, __fp16 *output, int32_t *shape_i, int32_t *shape_o,
                        int32_t dim_i, int32_t *starts, int32_t *ends, int32_t *steps);

/**
 * @}
 */

/**
 * @defgroup REF_MATMUL Matmul Functions
 * @{
 */

/*********************************** matmul *********************************/

/**
 * @brief       Matmul function
 *
 * @param[in]   A           Pointer to the matrix-A
 * @param[in]   B           Pointer to the matrix-B
 * @param[out]  C           Pointer to the matrix-C
 * @param[in]   shape_a     Shape of the matrix-A
 * @param[in]   dim_a       Number of dimensions of matrix-A
 * @param[in]   shape_b     Shape of the matrix-B
 * @param[in]   dim_b       Number of dimensions of matrix-B
 * @param[in]   shape_c     Shape of the matrix-C
 * @param[in]   dim_c       Number of dimensions of matrix-C
 * @param[in]   trans_a     Whether the matrix-A is transposed
 * @param[in]   trans_b     Whether the matrix-B is transposed
 * @param[in]   rB_buffer   The buffer size is K * N, used for reordering B
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_matmul_fp32(float *A, float *B, float *C, int32_t *shape_a, int32_t dim_a,
                         int32_t *shape_b, int32_t dim_b, int32_t *shape_c, int32_t dim_c,
                         bool trans_a, bool trans_b, void *rB_buffer);

/**
 * @brief       Matmul function
 *
 * @param[in]   A           Pointer to the matrix-A
 * @param[in]   B           Pointer to the matrix-B
 * @param[out]  C           Pointer to the matrix-C
 * @param[in]   shape_a     Shape of the matrix-A
 * @param[in]   dim_a       Number of dimensions of matrix-A
 * @param[in]   shape_b     Shape of the matrix-B
 * @param[in]   dim_b       Number of dimensions of matrix-B
 * @param[in]   shape_c     Shape of the matrix-C
 * @param[in]   dim_c       Number of dimensions of matrix-C
 * @param[in]   trans_a     Whether the matrix-A is transposed
 * @param[in]   trans_b     Whether the matrix-B is transposed
 * @param[in]   rB_buffer      The buffer size is K * N, used for reordering B
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_matmul_fp16(__fp16 *A, __fp16 *B, __fp16 *C, int32_t *shape_a, int32_t dim_a,
                         int32_t *shape_b, int32_t dim_b, int32_t *shape_c, int32_t dim_c,
                         bool trans_a, bool trans_b, void *rB_buffer);

/**
 * @brief       Gemm function
 *
 * @param[in]   A           Pointer to the matrix-A
 * @param[in]   B           Pointer to the matrix-B
 * @param[out]  C           Pointer to the matrix-C
 * @param[in]   M           The dimension M in gemm
 * @param[in]   K           The dimension K in gemm
 * @param[in]   N           The dimension N in gemm
 * @param[in]   trans_a     Whether the matrix-A is transposed
 * @param[in]   trans_b     Whether the matrix-B is transposed
 * @param[in]   rA_buffer   The buffer size is M * K, used for reordering A
 * @param[in]   rB_buffer   The buffer size is K * N, used for reordering B
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_gemm_fp32(float *A, float *B, float *C, int32_t M, int32_t K, int32_t N, bool trans_a,
                       bool trans_b, void *rB_buffer);

/**
 * @brief       Gemm function
 *
 * @param[in]   A           Pointer to the matrix-A
 * @param[in]   B           Pointer to the matrix-B
 * @param[out]  C           Pointer to the matrix-C
 * @param[in]   M           The dimension M in gemm
 * @param[in]   K           The dimension K in gemm
 * @param[in]   N           The dimension N in gemm
 * @param[in]   trans_a     Whether the matrix-A is transposed
 * @param[in]   trans_b     Whether the matrix-B is transposed
 * @param[in]   rB_buffer   The buffer size is K * N, used for reordering B
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_gemm_fp16(__fp16 *A, __fp16 *B, __fp16 *C, int32_t M, int32_t K, int32_t N,
                       bool trans_a, bool trans_b, void *rB_buffer);

/**
 * @}
 */

/**
 * @defgroup REF_MATH Math Functions
 * @{
 */

/*************************************** math *************************************/

/**
 * @brief       Exp function
 *
 * @param[in]   input    Pointer to the input data
 * @param[out]  output   Pointer to the output data
 * @param[in]   size     Size of input and output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_exp_fp32(float *input, float *output, int32_t size);

/**
 * @brief       Exp function
 *
 * @param[in]   input    Pointer to the input data
 * @param[out]  output   Pointer to the output data
 * @param[in]   size     Size of input and output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_exp_fp16(__fp16 *input, __fp16 *output, int32_t size);

/**
 * @brief       Square function
 *
 * @param[in]   input    Pointer to the input data
 * @param[out]  output   Pointer to the output data
 * @param[in]   size     Size of input and output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_square_fp32(float *input, float *output, int32_t size);

/**
 * @brief       Square function
 *
 * @param[in]   input    Pointer to the input data
 * @param[out]  output   Pointer to the output data
 * @param[in]   size     Size of input and output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_square_fp16(__fp16 *input, __fp16 *output, int32_t size);

/**
 * @brief       Sqrt function
 *
 * @param[in]   input    Pointer to the input data
 * @param[out]  output   Pointer to the output data
 * @param[in]   size     Size of input and output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_sqrt_fp32(float *input, float *output, int32_t size);

/**
 * @brief       Sqrt function
 *
 * @param[in]   input    Pointer to the input data
 * @param[out]  output   Pointer to the output data
 * @param[in]   size     Size of input and output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_sqrt_fp16(__fp16 *input, __fp16 *output, int32_t size);

/**
 * @brief       Rsqrt function
 *
 * @param[in]   input    Pointer to the input data
 * @param[out]  output   Pointer to the output data
 * @param[in]   size     Size of input and output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_rsqrt_fp32(float *input, float *output, int32_t size);

/**
 * @brief       Rsqrt function
 *
 * @param[in]   input    Pointer to the input data
 * @param[out]  output   Pointer to the output data
 * @param[in]   size     Size of input and output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_rsqrt_fp16(__fp16 *input, __fp16 *output, int32_t size);

/**
 * @brief       Sin function
 *
 * @param[in]   input    Pointer to the input data
 * @param[out]  output   Pointer to the output data
 * @param[in]   size     Size of input and output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_sin_fp32(float *input, float *output, int32_t size);

/**
 * @brief       Sin function
 *
 * @param[in]   input    Pointer to the input data
 * @param[out]  output   Pointer to the output data
 * @param[in]   size     Size of input and output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_sin_fp16(__fp16 *input, __fp16 *output, int32_t size);

/**
 * @brief       Cos function
 *
 * @param[in]   input    Pointer to the input data
 * @param[out]  output   Pointer to the output data
 * @param[in]   size     Size of input and output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_cos_fp32(float *input, float *output, int32_t size);

/**
 * @brief       Cos function
 *
 * @param[in]   input    Pointer to the input data
 * @param[out]  output   Pointer to the output data
 * @param[in]   size     Size of input and output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_cos_fp16(__fp16 *input, __fp16 *output, int32_t size);

/**
 * @brief       Neg function
 *
 * @param[in]   input    Pointer to the input data
 * @param[out]  output   Pointer to the output data
 * @param[in]   size     Size of input and output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_neg_fp32(float *input, float *output, int32_t size);

/**
 * @brief       Neg function
 *
 * @param[in]   input    Pointer to the input data
 * @param[out]  output   Pointer to the output data
 * @param[in]   size     Size of input and output
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_neg_fp16(__fp16 *input, __fp16 *output, int32_t size);
/**
 * @}
 */

/**
 * @defgroup REF_NORM Normalization Functions
 * @{
 */

/*********************************** normalization *********************************/

/**
 * @brief       Layer Norm function
 *
 * @param[in]   input           Pointer to the input data
 * @param[out]  output          Pointer to the output data
 * @param[in]   shape           Shape of the input and output
 * @param[in]   dim             Number of dimensions of input and output
 * @param[in]   gamma           Pointer to the gamma data, if gamma == NULL, default to 1.0
 * @param[in]   beta            Pointer to the beta data, if beta == NULL, default to 0.0
 * @param[in]   axis            Used to specify which dimension the operation is performed along
 * @param[in]   epsilon         Pointer to the epsilon, if epsilon == NULL, default to 1e-5
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than
 * or equal to 0.
 */
int xnnl_ref_layer_norm_fp32(float *input, float *output, int32_t *shape, int32_t dim, float *gamma,
                             float *beta, int32_t axis, float *epsilon);

/**
 * @brief       Layer Norm function
 *
 * @param[in]   input           Pointer to the input data
 * @param[out]  output          Pointer to the output data
 * @param[in]   shape           Shape of the input and output
 * @param[in]   dim             Number of dimensions of input and output
 * @param[in]   gamma           Pointer to the gamma data, if gamma == NULL, default to 1.0
 * @param[in]   beta            Pointer to the beta data, if beta == NULL, default to 0.0
 * @param[in]   axis            Used to specify which dimension the operation is performed along
 * @param[in]   epsilon         Pointer to the epsilon, if epsilon == NULL, default to 1e-5
 * @return      On success, the return value is 1.
 *              If an error occurred while executing the function, the return value is less than or
 *              equal to 0.
 */
int xnnl_ref_layer_norm_fp16(__fp16 *input, __fp16 *output, int32_t *shape, int32_t dim,
                             __fp16 *gamma, __fp16 *beta, int32_t axis, float *epsilon);

/**
 * @brief       Group Norm function
 *
 * @param[in]   input           Pointer to the input data
 * @param[out]  output          Pointer to the output data
 * @param[in]   shape           Shape of the input and output
 * @param[in]   dim             Number of dimensions of input and output
 * @param[in]   gamma           Pointer to the gamma data, if gamma == NULL, default to 1.0
 * @param[in]   beta            Pointer to the beta data, if beta == NULL, default to 0.0
 * @param[in]   num_groups      Number of groups to separate the channels into
 * @param[in]   epsilon         Pointer to the epsilon, if epsilon == NULL, default to 1e-5
 * @return      Returns 0 on success; returns 1 or greater on error.
 */
int xnnl_ref_group_norm_fp32(float *input, float *output, int32_t *shape, int32_t dim, float *gamma,
                             float *beta, int32_t num_groups, float *epsilon);

/**
 * @brief       Group Norm function
 *
 * @param[in]   input           Pointer to the input data
 * @param[out]  output          Pointer to the output data
 * @param[in]   shape           Shape of the input and output
 * @param[in]   dim             Number of dimensions of input and output
 * @param[in]   gamma           Pointer to the gamma data, if gamma == NULL, default to 1.0
 * @param[in]   beta            Pointer to the beta data, if beta == NULL, default to 0.0
 * @param[in]   num_groups      Number of groups to separate the channels into
 * @param[in]   epsilon         Pointer to the epsilon, if epsilon == NULL, default to 1e-5
 * @return      Returns 0 on success; returns 1 or greater on error.
 */
int xnnl_ref_group_norm_fp16(__fp16 *input, __fp16 *output, int32_t *shape, int32_t dim,
                             __fp16 *gamma, __fp16 *beta, int32_t num_groups, float *epsilon);

/**
 * @brief       Batch Norm function
 *
 * @param[in]   input          Pointer to the input data
 * @param[out]  output         Pointer to the output data
 * @param[in]   shape          Shape of the input and output
 * @param[in]   dim            Number of dimensions of input and output
 * @param[in]   mean           Pointer to the mean data
 * @param[in]   variance       Pointer to the variance data
 * @param[in]   gamma          Pointer to the gamma data, if gamma == NULL, default to 1.0
 * @param[in]   beta           Pointer to the beta data, if beta == NULL, default to 0.0
 * @param[in]   epsilon        Pointer to the epsilon, if epsilon == NULL, default to 1e-5
 * @return      Returns 0 on success; returns 1 or greater on error.
 */
int xnnl_ref_batch_norm_fp32(float *input, float *output, int32_t *shape, int32_t dim, float *mean,
                             float *variance, float *gamma, float *beta, float *epsilon);

/**
 * @brief       Batch Norm function
 *
 * @param[in]   input          Pointer to the input data
 * @param[out]  output         Pointer to the output data
 * @param[in]   shape          Shape of the input and output
 * @param[in]   dim            Number of dimensions of input and output
 * @param[in]   mean           Pointer to the mean data
 * @param[in]   variance       Pointer to the variance data
 * @param[in]   gamma          Pointer to the gamma data, if gamma == NULL, default to 1.0
 * @param[in]   beta           Pointer to the beta data, if beta == NULL, default to 0.0
 * @param[in]   epsilon        Pointer to the epsilon, if epsilon == NULL, default to 1e-5
 * @return      Returns 0 on success; returns 1 or greater on error.
 */
int xnnl_ref_batch_norm_fp16(__fp16 *input, __fp16 *output, int32_t *shape, int32_t dim,
                             __fp16 *mean, __fp16 *variance, __fp16 *gamma, __fp16 *beta,
                             float *epsilon);
/**
 * @}
 */

/**
 * @defgroup REF_REDUCTION Reduction Functions
 * @{
 */

/*************************************** reduction *************************************/

/**
 * @brief       Mean function
 *
 * @param[in]   input           Pointer to the input data
 * @param[out]  output          Pointer to the output data
 * @param[in]   shape           Shape of the input and output
 * @param[in]   dim             Number of dimensions of input and output
 * @param[in]   axes            Shape of the axes
 * @param[in]   dim_a           Number of dimensions of axes
 * @return      Returns 0 on success; returns 1 or greater on error.
 */
int xnnl_ref_mean_fp32(float *input, float *output, int32_t *shape, int32_t dim, int32_t *axes,
                       int32_t dim_a);

/**
 * @brief       Mean function
 *
 * @param[in]   input           Pointer to the input data
 * @param[out]  output          Pointer to the output data
 * @param[in]   shape           Shape of the input and output
 * @param[in]   dim             Number of dimensions of input and output
 * @param[in]   axes            Shape of the axes
 * @param[in]   dim_a           Number of dimensions of axes
 * @return      Returns 0 on success; returns 1 or greater on error.
 */
int xnnl_ref_mean_fp16(__fp16 *input, __fp16 *output, int32_t *shape, int32_t dim, int32_t *axes,
                       int32_t dim_a);

/**
 * @brief       Sum function
 *
 * @param[in]   input           Pointer to the input data
 * @param[out]  output          Pointer to the output data
 * @param[in]   shape           Shape of the input and output
 * @param[in]   dim             Number of dimensions of input and output
 * @param[in]   axes            Shape of the axes
 * @param[in]   dim_a           Number of dimensions of axes
 * @return      Returns 0 on success; returns 1 or greater on error.
 */
int xnnl_ref_sum_fp32(float *input, float *output, int32_t *shape, int32_t dim, int32_t *axes,
                      int32_t dim_a);

/**
 * @brief       Sum function
 *
 * @param[in]   input           Pointer to the input data
 * @param[out]  output          Pointer to the output data
 * @param[in]   shape           Shape of the input and output
 * @param[in]   dim             Number of dimensions of input and output
 * @param[in]   axes            Shape of the axes
 * @param[in]   dim_a           Number of dimensions of axes
 * @return      Returns 0 on success; returns 1 or greater on error.
 */
int xnnl_ref_sum_fp16(__fp16 *input, __fp16 *output, int32_t *shape, int32_t dim, int32_t *axes,
                      int32_t dim_a);

/**
 * @}
 */

/**
 * @}
 */

#ifdef __cplusplus
}
#endif

#endif  // INCLUDE_XNNL_REF_H_

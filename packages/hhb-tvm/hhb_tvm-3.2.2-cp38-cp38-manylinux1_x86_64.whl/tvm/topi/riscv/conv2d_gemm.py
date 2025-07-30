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
# pylint: disable=invalid-name, unused-variable, too-many-locals
# pylint: disable=unused-argument, redefined-builtin
"""GEMM Convolution schedule on Riscv"""
import tvm
from tvm.target import Target
from tvm import te
from tvm.topi import nn
import tvm.topi
from ..utils import get_const_tuple
from ..nn.utils import get_pad_tuple
from typing import Union, Sequence


def im2col(data, R, S, pad_h, pad_w, stride_h, stride_w):
    N, C, H, W = data.shape
    pad_top, pad_bottom = pad_h
    pad_left, pad_right = pad_w
    out_height = (H + pad_top + pad_bottom - R) // stride_h + 1
    out_width = (W + pad_left + pad_right - S) // stride_w + 1

    if {pad_h} != {0} or {pad_w} != {0}:
        data_padded = te.compute(
            (N, C, H + pad_top + pad_bottom, W + pad_left + pad_right),
            lambda n, c, h, w: te.if_then_else(
                tvm.tir.all(h >= pad_top, h < H + pad_top, w >= pad_left, w < W + pad_left),
                data[n, c, h - pad_top, w - pad_left],
                tvm.tir.const(0, data.dtype),
            ),
            name="data_padded",
        )
    else:
        data_padded = data

    data_col_2d = te.compute(
        (N * out_height * out_width, C * R * S),
        lambda idx, k: data_padded[
            idx // (out_height * out_width),  # n
            k // (R * S),  # c
            (idx % (out_height * out_width)) // out_width * stride_h
            + (k // S) % R,  # i * stride_h + r
            (idx % (out_height * out_width)) % out_width * stride_w + k % S,  # j * stride_w + s
        ],
        name="data_col",
    )

    return data_col_2d, out_height, out_width


def normalize_params(params, is_strided: bool = False):
    if is_strided:
        if isinstance(params, int):
            return params, params

        if isinstance(params, Sequence):
            if len(params) == 2:
                return params[0], params[1]
            else:
                raise ValueError("Invalid number of stride parameters")

    if isinstance(params, int):
        return params, params, params, params

    if isinstance(params, Sequence):
        if len(params) == 2:
            return params[0], params[1], params[0], params[1]
        if len(params) == 4:
            return params[0], params[1], params[2], params[3]
        else:
            raise ValueError("Invalid number of pad parameters")


def conv2d_im2col(
    data: te.Tensor,
    kernel: te.Tensor,
    stride: Union[int, Sequence[int]] = [1, 1],
    padding: Union[int, Sequence[int]] = [0, 0],
    dilation: Union[int, Sequence[int]] = [1, 1],
):
    # check dilation=1
    if (isinstance(dilation, int) and dilation != 1) or (
        isinstance(dilation, Sequence) and {_ for _ in dilation} != {1}
    ):
        raise ValueError("1x1 conv2d only support dilation=1")
    N, C, H, W = data.shape
    K, _, R, S = kernel.shape
    pad_top, pad_left, pad_bottom, pad_right = normalize_params(padding)
    stride_h, stride_w = normalize_params(stride, True)

    data_col_2d, out_height, out_width = im2col(
        data, R, S, (pad_top, pad_bottom), (pad_left, pad_right), stride_h, stride_w
    )

    # Reshape kernel to (K, C * R * S)
    kernel_flat = te.compute(
        (K, C * R * S),
        lambda k, c: kernel[k, c // (R * S), (c // S) % R, c % S],
        name="kernel_flat",
    )

    # Define batch axis for matrix multiplication
    k_axis = te.reduce_axis((0, C * R * S), name="k")

    # Matrix multiplication (N * out_height * out_width, K)
    conv_out_2d = te.compute(
        (N * out_height * out_width, K),
        lambda i, j: te.sum(data_col_2d[i, k_axis] * kernel_flat[j, k_axis], axis=k_axis),
        name="conv2d_compute",
    )

    # Reshape output to (N, K, out_height, out_width)
    conv = te.compute(
        (N, K, out_height, out_width),
        lambda n, k, h, w: conv_out_2d[n * out_height * out_width + h * out_width + w, k],
        name="conv",
    )

    return conv


def conv2d_1x1_im2col(
    data: te.Tensor,
    kernel: te.Tensor,
    stride: Union[int, Sequence[int]] = [1, 1],
    padding: Union[int, Sequence[int]] = [0, 0],
):
    N, C, H, W = data.shape
    K, _, R, S = kernel.shape  # In 1x1 conv, R, S == 1
    pad_top, pad_left, pad_bottom, pad_right = normalize_params(padding)
    stride_h, stride_w = normalize_params(stride, True)

    assert R == 1 and S == 1

    # Output dimensions
    out_height = (H + pad_top + pad_bottom - R) // stride_h + 1
    out_width = (W + pad_left + pad_right - S) // stride_w + 1

    # Pad the input
    if {pad_top, pad_left, pad_bottom, pad_right} != {0}:
        data_padded = te.compute(
            (N, C, H + pad_top + pad_bottom, W + pad_left + pad_right),
            lambda n, c, h, w: te.if_then_else(
                tvm.tir.all(h >= pad_top, h < H + pad_top, w >= pad_left, w < W + pad_left),
                data[n, c, h - pad_top, w - pad_left],
                tvm.tir.const(0.0, data.dtype),
            ),
            name="data_padded",
        )
    else:
        data_padded = data

    data_col_reshaped = te.compute(
        (N * out_height * out_width, C),
        lambda idx, c: data_padded[
            idx // (out_height * out_width),  # n
            c,  # c
            ((idx % (out_height * out_width)) // out_width) * stride_h,  # h
            ((idx % (out_height * out_width)) % out_width) * stride_w,  # w
        ],
        name="data_col",
    )

    # Flatten the kernel for matrix multiplication
    kernel_flat = te.compute((K, C), lambda k, c: kernel[k, c, 0, 0], name="kernel_flat")

    # Matrix multiplication
    rc = te.reduce_axis((0, C), name="rc")
    conv_out = te.compute(
        (N * out_height * out_width, K),
        lambda i, k: te.sum(data_col_reshaped[i, rc] * kernel_flat[k, rc], axis=rc),
        name="conv2d_compute",
    )

    # Reshape the output to the 4D tensor
    conv = te.compute(
        (N, K, out_height, out_width),
        lambda n, k, h, w: conv_out[n * out_height * out_width + h * out_width + w, k],
        name="conv",
    )

    return conv


def group_conv2d_im2col(
    data: te.Tensor,
    kernel: te.Tensor,
    stride: Union[int, Sequence[int]] = [1, 1],
    padding: Union[int, Sequence[int]] = [0, 0],
    groups: int = 1,
):
    N, C, H, W = data.shape
    K, _, R, S = kernel.shape  # In 1x1 conv, R, S == 1
    G = groups  # Number of groups
    assert C % G == 0, "Input channels must be divisible by the number of groups"
    assert K % G == 0, "Output channels must be divisible by the number of groups"

    group_channels_in = C // G
    group_channels_out = K // G

    conv_group = []
    for g in range(G):
        data_slice = te.compute(
            (N, group_channels_in, H, W),
            lambda n, c, h, w: data[n, g * group_channels_in + c, h, w],
            name=f"data_slice_{g}",
        )

        kernel_slice = te.compute(
            (group_channels_out, group_channels_in, R, S),
            lambda k, c, r, s: kernel[g * group_channels_out + k, c, r, s],
            name=f"kernel_slice_{g}",
        )

        # Apply the im2col transformation
        conv_out_flat = conv2d_im2col(data_slice, kernel_slice, stride, padding)
        conv_group.append(conv_out_flat)

    # Concatenate the results from each group
    concatenated = tvm.topi.concatenate(conv_group, axis=1)
    return concatenated


# Compute function
def conv2d_gemm(
    data: te.Tensor,
    kernel: te.Tensor,
    stride: Union[int, Sequence[int]] = [1, 1],
    padding: Union[int, Sequence[int]] = [0, 0],
    dilation: Union[int, Sequence[int]] = [1, 1],
    groups: int = 1,
    data_layout: str = "NCHW",
    out_dtype: Union[str, None] = "float32",
    use_im2col: bool = False,
):
    """Compute conv2d by transforming the input,
    executing GEMM and transforming the output back"""
    _, IC, _, _ = get_const_tuple(data.shape)
    OC, KIC, KH, KW = get_const_tuple(kernel.shape)
    # check dilation=1
    if (isinstance(dilation, int) and dilation != 1) or (
        isinstance(dilation, Sequence) and {_ for _ in dilation} != {1}
    ):
        raise ValueError("1x1 conv2d only support dilation=1")

    if data_layout != "NCHW":
        raise ValueError("Only support NCHW data layout")

    if use_im2col:
        if groups == 1:
            if KW == 1 and KH == 1:
                return conv2d_1x1_im2col(data, kernel, stride, padding)
            else:
                return conv2d_im2col(data, kernel, stride, padding)
        else:
            if groups == IC == OC and KIC == 1:
                # is depthwise conv
                return nn.depthwise_conv2d_nchw(data, kernel, stride, padding, dilation)
            return group_conv2d_im2col(data, kernel, stride, padding, groups)

    else:
        if groups == 1:
            if KW == 1 and KH == 1:
                return conv2d_gemm_1x1(data, kernel, stride, padding)
            return nn.conv2d(data, kernel, stride, padding)
        else:
            if groups == IC == OC and KIC == 1:
                # is depthwise conv
                return nn.depthwise_conv2d_nchw(data, kernel, stride, padding, dilation)
            return nn.group_conv2d_nchw(data, kernel, stride, padding, dilation, groups)


def conv2d_gemm_1x1(
    data: te.Tensor,
    kernel: te.Tensor,
    stride: Union[int, Sequence[int]] = 1,
    padding: Union[int, Sequence[int]] = 0,
    dilation: Union[int, Sequence[int]] = 1,
    groups: int = 1,
    data_layout: str = "NCHW",
    kernel_layout: str = "",
    out_dtype: Union[str, None] = None,
):
    """Compute conv2d when kernel 1x1"""
    if (isinstance(padding, int) and padding != 0) or (
        isinstance(padding, Sequence) and {_ for _ in padding} != {0}
    ):
        raise ValueError("1x1 conv2d only support no padding")

    if (isinstance(stride, int) and stride != 1) or (
        isinstance(stride, Sequence) and {_ for _ in stride} != {1}
    ):
        raise ValueError("1x1 conv2d only support strde=1")

    # check dilation=1
    if (isinstance(dilation, int) and dilation != 1) or (
        isinstance(dilation, Sequence) and {_ for _ in dilation} != {1}
    ):
        raise ValueError("1x1 conv2d only support dilation=1")

    # check groups=1
    if groups != 1:
        raise ValueError("1x1 conv2d only support groups=1")

    batches, IC, IH, IW = get_const_tuple(data.shape)
    OC = get_const_tuple(kernel.shape)[0]

    OH = IH
    OW = IW

    k = te.reduce_axis((0, IC), "k")

    # conv2d_1x1
    C = te.compute(
        (batches, OC, OH, OW),
        lambda b, oc, oh, ow: te.sum(data[b, k, oh, ow] * kernel[oc, k, 0, 0], axis=k),
        name="conv2d_1x1",
    )
    return C

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
from tvm import te
from tvm.topi import nn
import tvm.topi
from ..utils import get_const_tuple
from ..nn.utils import get_pad_tuple
from tvm.topi.nn.pad import pad
from tvm.topi.nn.winograd_util import winograd_transform_matrices
from typing import Sequence, Union
from tvm.target import Target


# Compute function
def conv2d_gemm_vector(
    data: te.Tensor,
    kernel: te.Tensor,
    stride: Union[int, Sequence[int]] = [1, 1],
    padding: Union[int, Sequence[int]] = [0, 0],
    dilation: Union[int, Sequence[int]] = [1, 1],
    groups: int = 1,
    data_layout: str = "NCHW",
    out_dtype: Union[str, None] = "float32",
):
    """Compute conv2d"""
    _, IC, IH, IW = get_const_tuple(data.shape)
    OC, KIC, KH, KW = get_const_tuple(kernel.shape)

    if groups == 1:
        if KW == 1 and KH == 1:
            return conv2d_gemm_1x1(data, kernel, stride, padding)
        else:
            return nn.conv2d(data, kernel, stride, padding, dilation)
    else:
        if groups == IC == OC and KIC == 1:
            # is depthwise conv
            return nn.depthwise_conv2d_nchw(data, kernel, stride, padding, dilation)
        return nn.group_conv2d_nchw(data, kernel, stride, padding, dilation, groups)


def conv2d_winograd_vector(
    data, weight, strides, padding, dilation, out_dtype="float32", tile_size=4, pre_computed=False
):
    """Compute winograd conv2d"""
    if not out_dtype:
        out_dtype = "float32"
    return conv2d_winograd_nchw(
        data, weight, strides, padding, dilation, out_dtype, tile_size, pre_computed
    )


def conv2d_gemm_1x1(
    data: te.Tensor,
    kernel: te.Tensor,
    stride: Union[int, Sequence[int]] = 1,
    padding: Union[int, Sequence[int]] = 0,
    dilation: Union[int, Sequence[int]] = 1,
    groups: int = 1,
    data_layout: str = "NCHW",
    kernel_layout: str = "",
    out_dtype: Union[str, None] = "float32",
    pre_compute=False,
    out_channel: int = 0,
):
    """Compute conv2d when kernel 1x1"""
    if (isinstance(padding, int) and padding != 0) or (
        isinstance(padding, Sequence) and {_ for _ in padding} != {0}
    ):
        raise ValueError("1x1 conv2d only support no padding")

    # check dilation=1
    if (isinstance(dilation, int) and dilation != 1) or (
        isinstance(dilation, Sequence) and {_ for _ in dilation} != {1}
    ):
        raise ValueError("1x1 conv2d only support dilation=1")

    # check groups=1
    if groups != 1:
        raise ValueError("1x1 conv2d only support groups=1")

    if isinstance(stride, int):
        strides = [stride, stride]
    else:
        strides = stride

    batches, IC, IH, IW = get_const_tuple(data.shape)
    target = Target.current(False)
    vlen = target.vlen
    packn = int(vlen / 32)
    if pre_compute:
        OC = out_channel
        tilem = get_const_tuple(kernel.shape)[-1]
    else:
        OC = get_const_tuple(kernel.shape)[0]

    OH = (IH - 1) // strides[0] + 1
    OW = (IW - 1) // strides[1] + 1

    k = te.reduce_axis((0, IC), "k")

    if IH * IW % packn != 0 or OH * OW % packn != 0:
        IW_pack = packn * strides[1]
        IW_Pad = (IW + IW_pack - 1) // IW_pack * IW_pack
        OW_Pad = (IW_Pad - 1) // strides[1] + 1

        # Pad the input
        data_padded = te.compute(
            (batches, IC, IH, IW_Pad),
            lambda b, ic, ih, iw: te.if_then_else(
                iw < IW,
                data[b, ic, ih, iw],
                tvm.tir.const(0.0, data.dtype),
            ),
            name="padded_A",
        )

        # Matrix multiplication
        if pre_compute:
            conv = te.compute(
                (batches, OC, OH, OW_Pad),
                lambda b, oc, oh, ow: te.sum(
                    data_padded[b, k, oh * strides[0], ow * strides[1]]
                    * kernel[oc // tilem, k, oc % tilem],
                    axis=k,
                ),
                name="conv2d_1x1",
            )
        else:
            conv = te.compute(
                (batches, OC, OH, OW_Pad),
                lambda b, oc, oh, ow: te.sum(
                    data_padded[b, k, oh * strides[0], ow * strides[1]] * kernel[oc, k, 0, 0],
                    axis=k,
                ),
                name="conv2d_1x1",
            )

        # Get output
        C = te.compute(
            (batches, OC, OH, OW),
            lambda b, oc, oh, ow: conv[b, oc, oh, ow],
            name="output",
        )

    else:
        if pre_compute:
            C = te.compute(
                (batches, OC, OH, OW),
                lambda b, oc, oh, ow: te.sum(
                    data[b, k, oh * strides[0], ow * strides[1]]
                    * kernel[oc // tilem, k, oc % tilem],
                    axis=k,
                ),
                name="conv2d_1x1",
            )
        else:
            C = te.compute(
                (batches, OC, OH, OW),
                lambda b, oc, oh, ow: te.sum(
                    data[b, k, oh * strides[0], ow * strides[1]] * kernel[oc, k, 0, 0], axis=k
                ),
                name="conv2d_1x1",
            )

    return C


def conv2d_winograd_nchw(
    data, weight, strides, padding, dilation, out_dtype, tile_size=4, pre_computed=False
):
    """Compute winograd conv2d"""

    N, CI, H, W = get_const_tuple(data.shape)
    if isinstance(dilation, int):
        dilation_h = dilation_w = dilation
    else:
        dilation_h, dilation_w = dilation

    assert (dilation_h, dilation_w) == (1, 1), "Does not support dilation"
    HSTR, WSTR = (strides, strides) if isinstance(strides, int) else strides

    if not pre_computed:  # kernel tensor is raw tensor, do strict check
        CO, CI, KH, KW = get_const_tuple(weight.shape)
        alpha = KW + tile_size - 1
        assert HSTR == 1 and WSTR == 1 and KH == KW
    else:
        alpha, _, Co, CI, _ = get_const_tuple(weight.shape)
        CO = Co * 8
        KH = KW = alpha + 1 - tile_size
        assert HSTR == 1 and WSTR == 1 and dilation_h == 1 and dilation_w == 1

    pad_t, pad_l, pad_b, pad_r = get_pad_tuple(padding, (KH, KW))
    assert HSTR == 1 and WSTR == 1 and KH == 3 and KW == 3

    pt, pl, pb, pr = get_pad_tuple(padding, (KH, KW))
    data_pad = pad(data, (0, 0, pt, pl), (0, 0, pb, pr), name="data_pad")

    r = KW
    m = tile_size
    A, B, G = winograd_transform_matrices(m, r, out_dtype)

    H = (H + pt + pb - KH) // HSTR + 1
    W = (W + pl + pr - KW) // WSTR + 1
    nH, nW = (H + m - 1) // m, (W + m - 1) // m

    P = N * nH * nW if isinstance(N, int) else nH * nW

    # transform kernel
    if not pre_computed:
        r_kh = te.reduce_axis((0, KH), name="r_kh")
        r_kw = te.reduce_axis((0, KW), name="r_kw")
        kernel_pack = te.compute(
            (alpha, alpha, CO, CI),
            lambda eps, nu, co, ci: te.sum(
                weight[co, ci, r_kh, r_kw] * G[eps, r_kh] * G[nu, r_kw], axis=[r_kh, r_kw]
            ),
            name="kernel_pack",
        )
    else:
        kernel_pack = weight

    # pack data tile
    input_tile = te.compute(
        (CI, P, alpha, alpha),
        lambda ci, p, eps, nu: data_pad[
            p // (nH * nW), ci, ((p // nW) % nH) * m + eps, (p % nW) * m + nu
        ],
        name="input_tile",
    )

    # transform data
    r_a = te.reduce_axis((0, alpha), "r_a")
    r_b = te.reduce_axis((0, alpha), "r_b")
    data_pack0 = te.compute(
        (CI, P, alpha, alpha),
        lambda ci, p, alpha0, alpha1: te.sum(
            input_tile[ci, p, alpha0, r_b] * B[r_b, alpha1], axis=[r_b]
        ),
        name="data_pack0",
    )

    data_pack1 = te.compute(
        (CI, P, alpha, alpha),
        lambda ci, p, alpha0, alpha1: te.sum(
            data_pack0[ci, p, r_a, alpha1] * B[r_a, alpha0], axis=[r_a]
        ),
        name="data_pack1",
    )

    data_pack = te.compute(
        (alpha, alpha, CI, P),
        lambda eps, nu, ci, p: data_pack1[ci, p, eps, nu],
        name="data_pack",
    )

    # do batch gemm
    ci = te.reduce_axis((0, CI), name="ci")
    bgemm = te.compute(
        (alpha, alpha, CO, P),
        lambda eps, nu, co, p: te.sum(
            data_pack[eps, nu, ci, p] * kernel_pack[eps, nu, co // 8, ci, co % 8], axis=[ci]
        ),
        name="bgemm",
    )

    # inverse transform
    r_a = te.reduce_axis((0, alpha), "r_a")
    r_b = te.reduce_axis((0, alpha), "r_b")
    inverse = te.compute(
        (CO, P, alpha, alpha),
        lambda co, p, eps, nu: bgemm[eps, nu, co, p],
        name="inverse",
    )

    output_pack0 = te.compute(
        (CO, P, alpha, m),
        lambda co, p, alpha, m: te.sum(inverse[co, p, alpha, r_b] * A[r_b, m], axis=[r_b]),
        name="output_pack0",
    )

    output_pack1 = te.compute(
        (CO, P, m, m),
        lambda co, p, m0, m1: te.sum(output_pack0[co, p, r_a, m1] * A[r_a, m0], axis=[r_a]),
        name="output_pack1",
    )

    # output
    output = te.compute(
        (N, CO, H, W),
        lambda n, co, h, w: output_pack1[co, n * nH * nW + (h // m) * nW + (w // m), h % m, w % m],
        name="conv2d_winograd",
    )

    return output

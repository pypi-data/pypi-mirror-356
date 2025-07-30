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
# pylint: disable=invalid-name, unused-argument, missing-docstring, unused-import
# pylint: disable=import-outside-toplevel
# pylint: disable=too-many-nested-blocks
"""Custom relay pass."""
import tvm
from tvm import relay
from tvm.relay.dataflow_pattern import (
    DFPatternCallback,
    is_constant,
    is_var,
    wildcard,
    is_op,
    rewrite,
    is_tuple,
)
from tvm.relay.frontend.common import infer_shape
from tvm.relay.transform import function_pass
from tvm.relay import expr as _expr
from tvm.relay.quantize.ir.base import _qnn_attrs
from tvm.relay.quantize.optimization.qnn_fuse import fuse_params_mul_after_conv

import numpy as np


def conv2python(data):
    return [conv2python(x) if isinstance(x, tvm.ir.container.Array) else int(x) for x in data]


def InsertNOp(mod):
    """insert Nop"""

    class BetweenLekayReLUAndAdd(relay.ExprMutator):
        """insert Nop between leakyrelu and and"""

        def visit_call(self, call):
            op_args = [self.visit(arg) for arg in call.args]
            if call.op.name == "add":
                l_pre_call = op_args[0]
                r_pre_call = op_args[1]

                if isinstance(l_pre_call, _expr.Call) and l_pre_call.op.name == "nn.leaky_relu":
                    mul_call = relay.op.add(l_pre_call, relay.op.const([2.0], "float32"))
                    new_call = relay.op.add(mul_call, r_pre_call)
                    new_call = relay.op.add(new_call, relay.op.const([-2.0], "float32"))
                    new_call = _expr.Call(
                        new_call.op, new_call.args, new_call.attrs, new_call.type_args, call.span
                    )
                    return new_call
            new_call = _expr.Call(call.op, op_args, call.attrs, call.type_args, call.span)
            return new_call

    mod["main"] = BetweenLekayReLUAndAdd().visit(mod["main"])

    return mod


def InsertRelu(mod):
    """insert relu"""

    class BetweenSigmoidAndMul(relay.ExprMutator):
        """insert relu between simoid and mul"""

        def visit_call(self, call):
            op_args = [self.visit(arg) for arg in call.args]
            if call.op.name == "multiply":
                new_pre_list = []
                for pre in op_args:
                    if isinstance(pre, _expr.Call) and pre.op.name == "sigmoid":
                        new_call = relay.op.nn.relu(pre)
                        new_pre_list.append(new_call)
                    else:
                        new_pre_list.append(pre)
                new_call = _expr.Call(call.op, new_pre_list, call.attrs, call.type_args, call.span)
                return new_call
            new_call = _expr.Call(call.op, op_args, call.attrs, call.type_args, call.span)
            return new_call

    mod["main"] = BetweenSigmoidAndMul().visit(mod["main"])

    return mod


@function_pass(opt_level=1)
class FuseCacheMatMul:
    r"""
    (Cache)
    Gather   Other
       \      /
        Concat
          |
        MatMUl               --> CacheMatMul
          |
         Add
          |
       Reshape
          |
       Transpose
    """

    def transform_function(self, func, mod, ctx):
        """patten and convert op"""

        class MyCallback(DFPatternCallback):
            def __init__(self):
                super(MyCallback, self).__init__()
                # Gathe
                self.input = wildcard()
                # concat
                self.concat = is_op("concatenate")(self.input)
                # Matmul
                self.weight = wildcard()
                self.dense = is_op("nn.dense")(self.concat, self.weight)
                self.b = wildcard()
                self.reshape2 = is_op("reshape")(self.dense)
                self.add = is_op("add")(self.reshape2, self.b)
                self.reshape3 = is_op("reshape")(self.add)
                # transpose
                self.transpose = is_op("transpose")(self.reshape3)
                self.pattern = self.transpose

            def callback(self, pre, post, node_map):
                """taget op"""
                cache, in_node = node_map[self.input][0]
                weight = node_map[self.weight][0]
                bias = node_map[self.b][0]
                t_dims = conv2python(node_map[self.transpose][0].attrs.axes)

                cache_shape = infer_shape(cache)
                reshape = infer_shape(node_map[self.reshape3][0])

                new_node = relay.op.custom_op.cache_matmul(
                    in_node, weight, bias, cache_shape, reshape, t_dims
                )
                return new_node

        out = rewrite(MyCallback(), mod["main"].body)
        res = tvm.IRModule.from_expr(out)

        return res["main"]


@function_pass(opt_level=1)
class FuseCacheConv1d:
    r"""
    (Cache)    Input
      |          |
    Gather   Transpose
       \        /
         Concat               --> CacheConv1d
           |
         Conv1d
           |
        BiasAdd
    """

    def transform_function(self, func, mod, ctx):
        """patten and convert op"""

        class MyCallback(DFPatternCallback):
            def __init__(self):
                super(MyCallback, self).__init__()
                # Input
                self.input = wildcard()
                # Gather
                self.gather = is_op("take")(is_var(), wildcard())
                # Transpose
                self.transpose = is_op("transpose")(self.input)
                # Concat
                self.tup = is_tuple([self.gather, self.transpose])
                self.concat = is_op("concatenate")(self.tup)
                # Conv1d
                self.weight = wildcard()
                self.conv1d = is_op("nn.conv1d")(self.concat, self.weight)
                # BiasAdd
                self.bias = wildcard()
                self.bias_add = is_op("nn.bias_add")(self.conv1d, self.bias)
                self.pattern = self.bias_add

            def callback(self, pre, post, node_map):
                """taget op"""
                in_node = node_map[self.input][0]
                weight = node_map[self.weight][0]
                bias = node_map[self.bias][0]
                cache_shape = infer_shape(node_map[self.gather][0])
                new_node = relay.op.custom_op.cache_conv1d(in_node, weight, bias, cache_shape)
                return new_node

        out = rewrite(MyCallback(), mod["main"].body)
        res = tvm.IRModule.from_expr(out)

        return res["main"]


@function_pass(opt_level=1)
class FuseLayerNormal:
    r"""
        input
       /     \
      |     Mean
       \     /
         Sub
       /     \
      |      Power
              |
      |      Mean
              |
      |      Add               --> LayNormal
              |
      |      Sqrt
       \     /
         Div
          |
         Mul
          |
         Add

    """

    def transform_function(self, func, mod, ctx):
        """patten and convert op"""

        class MyCallback(DFPatternCallback):
            def __init__(self):
                super(MyCallback, self).__init__()
                # input
                self.input = wildcard()
                # mean1
                self.mean1 = is_op("mean")(self.input)
                # sub
                self.sub = is_op("subtract")(self.input, self.mean1)
                # power
                self.power_val = is_constant()
                self.power = is_op("power")(self.sub, self.power_val)
                # mean2
                self.mean2 = is_op("mean")(self.power)
                # add1
                self.add1_val = is_constant()
                self.add1 = is_op("add")(self.mean2, self.add1_val)
                # sqrt
                self.sqrt = is_op("sqrt")(self.add1)
                # div
                self.div = is_op("divide")(self.sub, self.sqrt)

                # reshape optition
                self.reshape = is_op("reshape")(self.div)

                # mul
                self.mul_val = is_constant()
                self.mul = is_op("multiply")(self.div, self.mul_val) | is_op("multiply")(
                    self.reshape, self.mul_val
                )

                # add2
                self.add2_val = is_constant()
                self.add2 = is_op("add")(self.mul, self.add2_val)

                self.pattern = self.add2

            def callback(self, pre, post, node_map):
                """taget op"""
                in_node = node_map[self.input][0]
                axis = int(node_map[self.mean1][0].attrs.axis[0])
                eps = node_map[self.add1_val][0].data.asnumpy().reshape(-1)[0]
                gamma = node_map[self.mul_val][0]
                beta = node_map[self.add2_val][0]

                new_node = relay.op.nn.layer_norm(in_node, gamma, beta, axis, eps)
                new_shape = infer_shape(new_node)
                old_shape = infer_shape(pre)
                if new_shape == old_shape:
                    return new_node
                else:
                    return relay.op.reshape(new_node, old_shape)

        out = rewrite(MyCallback(), mod["main"].body)
        res = tvm.IRModule.from_expr(out)

        return res["main"]


@function_pass(opt_level=1)
class TConv1dAddT:
    r"""
      Input
        |
    Transpose           Dense
        |           -->   |
      Conv1D           BiasAdd
        |
     BiasAdd
        |
    Transpose

    """

    def transform_function(self, func, mod, ctx):
        """patten and convert op"""

        class MyCallback(DFPatternCallback):
            def __init__(self):
                super(MyCallback, self).__init__()
                # input
                self.input = wildcard()
                # transpose1
                self.transpose1 = is_op("transpose")(self.input)
                # conv1d
                self.weight_val = is_constant()
                self.bias_val = is_constant()
                self.conv1d = is_op("nn.conv1d")(self.transpose1, self.weight_val).has_attr(
                    {"kernel_size": [1], "groups": 1, "strides": [1], "padding": [0, 0]}
                )
                self.bias_add = is_op("nn.bias_add")(self.conv1d, self.bias_val)
                # transpose2
                self.transpose2 = is_op("transpose")(self.bias_add)
                self.pattern = self.transpose2

            def callback(self, pre, post, node_map):
                """taget op"""
                in_node = node_map[self.input][0]
                in_shape = infer_shape(in_node)
                if len(in_shape) != 2:
                    in_node = relay.op.reshape(in_node, [-1, in_shape[-1]])
                weight = node_map[self.weight_val][0].data.asnumpy().squeeze(2)
                weight_exp = relay.const(weight)
                bias = node_map[self.bias_val][0]
                new_dense = relay.op.nn.dense(in_node, weight_exp)
                new_out = relay.op.nn.bias_add(new_dense, bias, axis=-1)

                return new_out

        out = rewrite(MyCallback(), mod["main"].body)
        res = tvm.IRModule.from_expr(out)

        return res["main"]


@function_pass(opt_level=1)
class Swish:
    r"""fusion pass for qnn

        Input
       /     \
      |   Sigmoid    -->   Swish
       \     /
         Mul

    """

    def transform_function(self, func, mod, ctx):
        """patten and convert op"""

        class MyCallback(DFPatternCallback):
            def __init__(self):
                super(MyCallback, self).__init__()
                # input
                self.input = wildcard()
                # sigmoid
                self.sigmoid = is_op("sigmoid")(self.input)
                # mul
                self.mul = is_op("multiply")(self.input, self.sigmoid) | is_op("multiply")(
                    self.sigmoid, self.input
                )
                self.pattern = self.mul

            def callback(self, pre, post, node_map):
                """taget op"""
                in_node = node_map[self.input][0]
                new_node = relay.op.nn.swish(in_node)
                return new_node

        out = rewrite(MyCallback(), mod["main"].body)
        res = tvm.IRModule.from_expr(out)

        return res["main"]


def ConvertBatchFlatten2Reshape(mod):
    """Convert nn.batch_flatten into reshape op."""

    class Internal(relay.ExprMutator):
        """Helper"""

        def visit_call(self, call):
            op_args = [self.visit(arg) for arg in call.args]
            if call.op.name == "nn.batch_flatten":
                inp = op_args[0]
                inp_shape = infer_shape(inp)
                new_shape = (inp_shape[0], -1)

                return relay.op.reshape(inp, new_shape)
            new_call = _expr.Call(call.op, op_args, call.attrs, call.type_args, call.span)
            return new_call

    mod["main"] = Internal().visit(mod["main"])

    return mod


def OptStridedSlice(mod):
    """Optimize strided_slice and ensure the ends is valid."""

    class Internal(relay.ExprMutator):
        """Helper"""

        def visit_call(self, call):
            op_args = [self.visit(arg) for arg in call.args]
            if call.op.name == "strided_slice":
                inp = op_args[0]
                inp_shape = infer_shape(inp)

                begin = call.attrs.begin
                end = call.attrs.end
                strides = call.attrs.strides
                slice_mode = call.attrs.slice_mode
                axes = call.attrs.axes

                if end:
                    new_end = []
                    if len(end) == len(inp_shape):
                        for idx in range(len(end)):
                            if end[idx].value > inp_shape[idx]:
                                new_end.append(inp_shape[idx])
                            else:
                                new_end.append(end[idx].value)
                    else:
                        for idx, ax in enumerate(axes):
                            axes_val = ax.value
                            if end[idx].value > inp_shape[axes_val]:
                                new_end.append(inp_shape[axes_val])
                            else:
                                new_end.append(end[idx].value)
                    end = new_end

                return relay.op.strided_slice(inp, begin, end, strides, axes, slice_mode)
            new_call = _expr.Call(call.op, op_args, call.attrs, call.type_args, call.span)
            return new_call

    mod["main"] = Internal().visit(mod["main"])

    return mod


@function_pass(opt_level=1)
class ReorderConvAddMul:
    """Reorder conv+add/bias_add+mul -> conv+mul+add."""

    def transform_function(self, func, mod, ctx):
        """patten and convert op"""

        class MyCallback(DFPatternCallback):
            def __init__(self):
                super(MyCallback, self).__init__()
                # input
                self.input = wildcard()
                # conv2d
                self.conv2d = is_op("nn.conv2d")(self.input, is_constant())
                # add
                self.add_const = is_constant()
                self.add = is_op("add")(self.conv2d, self.add_const) | is_op("add")(
                    self.add_const, self.conv2d
                )
                # mul
                self.mul_const = is_constant()
                self.mul = is_op("multiply")(self.add, self.mul_const) | is_op("multiply")(
                    self.mul_const, self.add
                )
                self.pattern = self.mul

            def callback(self, pre, post, node_map):
                """taget op"""
                conv2d_node = node_map[self.conv2d][0]

                add_const = node_map[self.add_const][0]
                mul_const = node_map[self.mul_const][0]

                add_const_val = add_const.data.asnumpy()
                mul_const_val = mul_const.data.asnumpy()

                out = relay.multiply(conv2d_node, mul_const)
                out = relay.add(out, relay.const(add_const_val * mul_const_val))

                return out

        out = rewrite(MyCallback(), mod["main"].body)
        res = tvm.IRModule.from_expr(out)

        return res["main"]


@function_pass(opt_level=1)
class FuseMulAfterConv:
    """Fuse mul op in behind the convolution op."""

    def transform_function(self, func, mod, ctx):
        """patten and convert op"""
        func = relay.Function(func.params, func.body, None, func.type_params, func.attrs)

        class FuseMulAfterConvMutator(relay.ExprMutator):
            """Fuse mul after conv"""

            def visit_call(self, call):
                op_args = [self.visit(arg) for arg in call.args]
                if call.op.name == "multiply" and isinstance(op_args[1], relay.expr.Constant):
                    pre_call = op_args[0]
                    if isinstance(pre_call, relay.expr.Call) and pre_call.op.name == "nn.conv2d":
                        data = pre_call.args[0]
                        weight = pre_call.args[1]

                        weight_val = weight.data.asnumpy()
                        mul_rhs_val = op_args[1].data.asnumpy()

                        if mul_rhs_val.size != weight_val.shape[0]:
                            new_call = relay.expr.Call(
                                call.op, op_args, call.attrs, call.type_args, call.span
                            )
                            return new_call

                        new_weight_val = fuse_params_mul_after_conv(weight_val, mul_rhs_val)

                        weight.data.copyfrom(new_weight_val)

                        attrs = pre_call.attrs
                        new_call = relay.nn.conv2d(
                            data,
                            weight,
                            strides=attrs.strides,
                            padding=attrs.padding,
                            dilation=attrs.dilation,
                            groups=attrs.groups,
                            channels=attrs.channels,
                            kernel_size=attrs.kernel_size,
                            data_layout=attrs.data_layout,
                            kernel_layout=attrs.kernel_layout,
                            out_layout=attrs.out_layout,
                            out_dtype=attrs.out_dtype,
                        )
                        return new_call

                new_call = relay.Call(call.op, op_args, call.attrs, call.type_args, call.span)
                return new_call

        return FuseMulAfterConvMutator().visit(func)


@function_pass(opt_level=1)
class ConvertFasterConv:
    """Convert conv2d into faster implemention."""

    def transform_function(self, func, mod, ctx):
        """patten and convert op"""
        func = relay.Function(func.params, func.body, None, func.type_params, func.attrs)

        class ConvertFasterConvMutator(relay.ExprMutator):
            """Helper"""

            def visit_call(self, call):
                op_args = [self.visit(arg) for arg in call.args]
                if call.op.name == "nn.conv2d":
                    # Parse the attributes.
                    attrs = call.attrs
                    padding = attrs.get_int_tuple("padding")
                    strides = attrs.get_int_tuple("strides")
                    dilation = attrs.get_int_tuple("dilation")
                    data_layout = attrs["data_layout"]
                    kernel_layout = attrs["kernel_layout"]
                    group = attrs["groups"]
                    N, CI, H, W = infer_shape(op_args[0])
                    CO, _, KH, KW = infer_shape(op_args[1])
                    if (
                        data_layout == "NCHW"
                        and kernel_layout == "OIHW"
                        and KH == 3
                        and KW == 3
                        and strides == (1, 1)
                        and dilation == (1, 1)
                        and group == 1
                        and CO > 32
                        and CI > 32
                    ):
                        new_attrs = {k: attrs[k] for k in attrs.keys()}

                        tile_size = 4
                        weight = relay.nn.contrib_conv2d_winograd_weight_transform(
                            op_args[1], tile_size=tile_size
                        )

                        # pack weight
                        curr_shape = infer_shape(weight)
                        weight = relay.reshape(
                            weight,
                            [curr_shape[0], curr_shape[1], curr_shape[2] // 8, 8, curr_shape[3]],
                        )
                        weight = relay.transpose(weight, [0, 1, 2, 4, 3])

                        new_attrs["tile_size"] = tile_size
                        new_attrs["channels"] = CO
                        return relay.nn.contrib_conv2d_winograd_without_weight_transform(
                            op_args[0], weight, **new_attrs
                        )
                    elif (
                        data_layout == "NCHW"
                        and kernel_layout == "OIHW"
                        and KH == 1
                        and KW == 1
                        and dilation == (1, 1)
                        and group == 1
                    ):
                        new_attrs = {k: attrs[k] for k in attrs.keys()}
                        tile_n = 8
                        tile_k = 8
                        new_attrs["channels"] = CO
                        weight = relay.nn.contrib_conv2d_gemm_weight_transform(
                            op_args[1], tile_n, tile_k, "OIHW"
                        )
                        return relay.nn.contrib_conv2d_gemm_without_weight_transform(
                            op_args[0], weight, **new_attrs
                        )

                new_call = relay.Call(call.op, op_args, call.attrs, call.type_args, call.span)
                return new_call

        return ConvertFasterConvMutator().visit(func)


@function_pass(opt_level=1)
class ConvertBiasAdd2Add:
    """Convert nn.bias_add into add."""

    def transform_function(self, func, mod, ctx):
        """patten and convert op"""
        func = relay.Function(func.params, func.body, None, func.type_params, func.attrs)

        class ConvertBiasAdd2AddMutator(relay.ExprMutator):
            """Fuse mul after conv"""

            def visit_call(self, call):
                op_args = [self.visit(arg) for arg in call.args]
                if call.op.name == "nn.bias_add":
                    pre_call = op_args[0]
                    if isinstance(pre_call, relay.expr.Call) and pre_call.op.name == "nn.conv2d":
                        assert pre_call.attrs.data_layout in (
                            "NCHW",
                            "NHWC",
                        ), f"Only support for NCHW/NHWC, but get {pre_call.attrs.data_layout}"

                        pre_call_shape = infer_shape(pre_call)

                        new_shape = [1, 1, 1, 1]
                        if pre_call.attrs.data_layout == "NCHW":
                            new_shape[1] = pre_call_shape[1]
                        elif pre_call.attrs.data_layout == "NHWC":
                            new_shape[3] = pre_call_shape[3]

                        bias_add_rhs = op_args[1].data.asnumpy()
                        bias_add_rhs = np.reshape(bias_add_rhs, new_shape)

                        bias_add_rhs = relay.const(bias_add_rhs)
                        return relay.add(pre_call, bias_add_rhs)

                new_call = relay.Call(call.op, op_args, call.attrs, call.type_args, call.span)
                return new_call

        return ConvertBiasAdd2AddMutator().visit(func)


@function_pass(opt_level=1)
class FuseAddAdd:
    """Fuse input -> add(lhs, const) -> add(lhs, const) => input -> add(lhs, const)."""

    def transform_function(self, func, mod, ctx):
        """patten and convert op"""

        class MyCallback(DFPatternCallback):
            def __init__(self):
                super(MyCallback, self).__init__()
                # input
                self.input = wildcard()
                # add
                self.add1_const = is_constant()
                self.add1 = is_op("add")(self.input, self.add1_const) | is_op("add")(
                    self.add1_const, self.input
                )
                # add
                self.add2_const = is_constant()
                self.add2 = is_op("add")(self.add1, self.add2_const) | is_op("add")(
                    self.add2_const, self.add1
                )
                self.pattern = self.add2

            def callback(self, pre, post, node_map):
                """taget op"""
                input_node = node_map[self.input][0]

                add1_const = node_map[self.add1_const][0]
                add2_const = node_map[self.add2_const][0]

                new_add_const = relay.const(add1_const.data.asnumpy() + add2_const.data.asnumpy())
                out = relay.add(input_node, new_add_const)
                return out

        out = rewrite(MyCallback(), mod["main"].body)
        res = tvm.IRModule.from_expr(out)

        return res["main"]

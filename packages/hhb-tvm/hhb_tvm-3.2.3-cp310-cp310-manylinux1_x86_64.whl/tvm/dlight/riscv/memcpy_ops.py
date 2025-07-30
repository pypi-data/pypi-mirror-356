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
"""A schedule rule for memcpy_ops"""
from typing import List, Union
from tvm import tir
from tvm.target import Target
from .base import RISCVScheduleRule


class Memcpy_Ops(RISCVScheduleRule):
    """A rule for memcpy_ops."""

    def apply(  # pylint: disable=too-many-locals,missing-docstring
        self,
        func: tir.PrimFunc,
        target: Target,
        _: bool,
    ) -> Union[None, tir.Schedule, List[tir.Schedule]]:
        if not isinstance(func, tir.PrimFunc) or not self.is_target_available(target):
            return None

        sch = tir.Schedule(func)
        root_block = sch.get_block("root")
        blocks = sch.get_child_blocks(root_block)
        memcpy_ops = [
            "T_reshape",
            "T_expand_dims",
            "T_take",
            "T_strided_slice_with_axes",
            "T_split",
            "T_split_sections",
            "T_squeeze",
        ]
        if sch.get(blocks[0]).name_hint not in memcpy_ops:
            return None

        # After testing, the performance of naive memcpy is close
        # to vle/vse, so it is not necessary to schedule reshape,
        # expand_dims, take, strided_slice, split, and squeeze.
        # Just mark is_scheduled=1 here.
        return sch

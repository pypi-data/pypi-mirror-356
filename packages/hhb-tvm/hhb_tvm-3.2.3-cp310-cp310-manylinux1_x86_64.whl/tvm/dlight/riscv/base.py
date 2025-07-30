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
"""Base schedule rule for RISCV operators."""

from tvm.target import Target

from ..base import ScheduleRule


class RISCVScheduleRule(ScheduleRule):  # pylint: disable=too-few-public-methods
    """The Schedule Rule specific to RISCV targets, will return None if the target is not RISCV."""

    def __init__(self):
        super().__init__()
        self.cpu_list_vector = ["c920", "c907fdvm", "c908v"]

    def is_target_available(self, target: Target) -> bool:
        """Check whether the target is available for riscv rule.

        Parameters
        ----------
        target : Target
            The compilation target to check.

        Returns
        -------
        available : bool
            Whether the target is available for this rule.
        """

        target_cpu = target.mcpu
        return super().is_target_available(target) and (
            "+xtheadv" in target.mattr or target_cpu in self.cpu_list_vector
        )


class RISCVMatrixScheduleRule(ScheduleRule):  # pylint: disable=too-few-public-methods
    """The Schedule Rule specific to RISCV targets with matrix unit
    will return None if the target is not RISCV or without matrix unit."""

    def __init__(self):
        super().__init__()
        self.cpu_list_matrix = ["c907fdvm"]

    def is_target_available(self, target: Target) -> bool:
        """Check whether the target is available for riscv rule.

        Parameters
        ----------
        target : Target
            The compilation target to check.

        Returns
        -------
        available : bool
            Whether the target is available for this rule.
        """
        target_cpu = target.mcpu
        return super().is_target_available(target) and target_cpu in self.cpu_list_matrix

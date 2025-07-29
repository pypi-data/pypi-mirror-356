#
# MIT License
#
# Copyright (c) 2024-2025 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""Synchronizer with Edge Detector."""

import ucdp as u
from ucdp_glbl.dft import DftModeType

from ucdp_common.fileliststandard import HdlFileList

from .ucdp_sync_leaf_one import UcdpSyncLeafOneMod
from .ucdp_sync_leaf_zero import UcdpSyncLeafZeroMod


class EdgeSpecType(u.AEnumType):
    """
    Edge detection type specification.

        >>> e = EdgeSpecType()
        >>> e.keytype
        UintType(2)
        >>> for item in e.values():
        ...     item
        EnumItem(0, 'none', doc=Doc(title='None', descr='No edge detection, edge_o is tied to 0'))
        EnumItem(1, 'rise', doc=Doc(title='Rising edge.', descr='Detection of rising edges'))
        EnumItem(2, 'fall', doc=Doc(title='Falling edge.', descr='Detection of falling edges'))
        EnumItem(3, 'any', doc=Doc(title='Any edge.', descr='Detection of positive and negative edges'))
    """

    keytype: u.UintType = u.UintType(2, default=0)

    def _build(self) -> None:
        self._add(0, "none", title="None", descr="No edge detection, edge_o is tied to 0")
        self._add(1, "rise", title="Rising edge.", descr="Detection of rising edges")
        self._add(2, "fall", title="Falling edge.", descr="Detection of falling edges")
        self._add(3, "any", title="Any edge.", descr="Detection of positive and negative edges")


class UcdpSyncMod(u.AMod):
    """
    Synchronizer with Edge Detector.

    Two-flop synchronizer with optional edge detection.

    Parameters:

        >>> for param in UcdpSyncMod().params: print(param.name, param.type_)
        edge_type_p EdgeSpecType()
        rstval_p BitType()
        norstvalchk_p BitType()

    Ports:

        >>> for port in UcdpSyncMod().ports: print(port.name, port.type_)
        tgt_i ClkRstAnType()
        dft_mode_i DftModeType()
        d_i BitType()
        q_o BitType()
        edge_o BitType()

    """

    filelists: u.ClassVar[u.ModFileLists] = (HdlFileList(gen="inplace"),)

    def _build(self) -> None:
        if self.parent:
            self.parent.add_type_consts(EdgeSpecType(), exist_ok=True)

        # -----------------------------
        # Parameter List
        # -----------------------------
        self.add_param(
            EdgeSpecType(),
            "edge_type_p",
            title="Type of edge detection",
            descr="Specifies type of optional edge detection",
        )
        self.add_param(
            u.BitType(),
            "rstval_p",
            title="Reset Value",
            descr="Data Reset Value to avoid edge detection after reset.",
        )
        self.add_param(
            u.BitType(),
            "norstvalchk_p",
            title="No Reset Value Check",
            descr=(
                "Do NOT ensure Data Input Value is identical to rstval_p at reset release. "
                "This parameter has NO influence on the implementation. Simulation Only."
            ),
        )

        # -----------------------------
        # Port List
        # -----------------------------
        self.add_port(u.ClkRstAnType(), "tgt_i")
        self.add_port(DftModeType(), "dft_mode_i")
        self.add_port(u.BitType(), "d_i", title="Data Input", comment="Data Input")
        self.add_port(u.BitType(), "q_o", title="Data Output", comment="Data Output")
        self.add_port(u.BitType(), "edge_o", title="Edge Output", comment="Edge Output")
        UcdpSyncLeafZeroMod(self, "u_sync0", virtual=True)
        UcdpSyncLeafOneMod(self, "u_sync1", virtual=True)

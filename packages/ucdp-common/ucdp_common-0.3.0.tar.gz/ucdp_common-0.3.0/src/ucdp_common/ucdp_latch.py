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

"""Latch."""

import ucdp as u
from ucdp_glbl.dft import DftModeType

from ucdp_common.fileliststandard import HdlFileList


class UcdpLatchMod(u.AMod):
    """
    Latch.

    Testable Latch.
    """

    filelists: u.ClassVar[u.ModFileLists] = (HdlFileList(gen="inplace"),)

    def _build(self) -> None:
        width_p = self.add_param(u.IntegerType(default=1), "width_p", title="Width in Bits")
        self.add_param(u.UintType(width_p), "rstval_p", title="Reset Value")

        # -----------------------------
        # Port List
        # -----------------------------
        self.add_port(u.ClkRstAnType(), "main_i")
        self.add_port(DftModeType(), "dft_mode_i")
        self.add_port(u.BitType(), "ld_i", title="Load")
        self.add_port(u.UintType(width_p), "d_i", title="Data Input", comment="Data Input")
        self.add_port(u.UintType(width_p), "q_o", title="Data Output", comment="Data Output")

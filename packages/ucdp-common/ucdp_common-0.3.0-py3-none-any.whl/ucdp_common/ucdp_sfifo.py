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

"""
Unified Chip Design Platform - Common IP - Synchronous FIFO.
"""

import ucdp as u
from ucdp_glbl.dft import DftModeType

from ucdp_common.fileliststandard import HdlFileList


class UcdpSfifoMod(u.AMod):
    """
    Synchronous FIFO.
    """

    filelists: u.ClassVar[u.ModFileLists] = (HdlFileList(gen="inplace"),)

    def _build(self) -> None:
        # -----------------------------
        # Parameter List
        # -----------------------------
        dwidth_p = self.add_param(u.IntegerType(default=8), "dwidth_p", title="FIFO Data Width")
        depth_p = self.add_param(u.IntegerType(default=4), "depth_p", title="FIFO Depth")
        awidth_p = self.add_param(
            u.IntegerType(default=self.parser.log2(depth_p + 1)), "awidth_p", title="FIFO Address Width"
        )

        # -----------------------------
        # Port List
        # -----------------------------
        self.add_port(u.ClkRstAnType(), "src_i", title="Clock and Reset")
        self.add_port(DftModeType(), "dft_mode_i")
        self.add_port(u.EnaType(), "wr_en_i", title="Write Enable")
        self.add_port(u.UintType(dwidth_p), "wr_data_i", title="Write Data")
        self.add_port(u.BitType(), "wr_full_o", title="FIFO Full")
        self.add_port(u.UintType(awidth_p), "wr_space_avail_o", title="FIFO Space Available")
        self.add_port(u.EnaType(), "rd_en_i", title="Read Enable")
        self.add_port(u.UintType(dwidth_p), "rd_data_o", title="Read Data")
        self.add_port(u.BitType(), "rd_empty_o", title="FIFO empty")
        self.add_port(u.UintType(awidth_p), "rd_data_avail_o", title="FIFO Data Available")

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
Unified Chip Design Platform - Common IP - Asynchronous FIFO.
"""

import ucdp as u
from ucdp_glbl.dft import DftModeType

from ucdp_common.fileliststandard import HdlFileList
from ucdp_common.ucdp_sync import UcdpSyncMod


class UcdpAfifoMod(u.AMod):
    """
    Asynchronous FIFO.

    A-FIFO is designed according a paper from Clifford E. Cummings and Peter Alfke.
    The paper location is  http://www.sunburst-design.com/papers/CummingsSNUG2002SJ_FIFO1.pdf.
    """

    filelists: u.ClassVar[u.ModFileLists] = (HdlFileList(gen="inplace"),)

    def _build(self) -> None:
        # -----------------------------
        # Parameter List
        # -----------------------------
        dwidth_p = self.add_param(u.IntegerType(default=8), "dwidth_p", title="Data Width")
        awidth_p = self.add_param(u.IntegerType(default=4), "awidth_p", title="FIFO Address Width")

        self.add_const(u.IntegerType(default=1 << (awidth_p - 1)), "depth_p")
        # -----------------------------
        # Port List
        # -----------------------------
        self.add_port(u.ClkRstAnType(), "src_i", title="Clock and Reset for Source Domain")
        self.add_port(u.ClkRstAnType(), "tgt_i", title="Clock and Reset for Target Domain")
        self.add_port(DftModeType(), "dft_mode_i")
        self.add_port(u.EnaType(), "src_wr_en_i", title="Source Write Enable")
        self.add_port(u.UintType(dwidth_p), "src_wr_data_i", title="Source Write Data")
        self.add_port(u.BitType(), "src_wr_full_o", title="FIFO Full")
        self.add_port(u.UintType(awidth_p), "src_wr_space_avail_o", title="FIFO Space Available")
        self.add_port(u.EnaType(), "tgt_rd_en_i", title="Target Read Enable")
        self.add_port(u.UintType(dwidth_p), "tgt_rd_data_o", title="Target Read Data")
        self.add_port(u.BitType(), "tgt_rd_empty_o", title="FIFO empty")
        self.add_port(u.UintType(awidth_p), "tgt_rd_data_avail_o", title="FIFO Data Available")
        UcdpSyncMod(self, "u_sync", virtual=True)  # just for proper dependency resolution

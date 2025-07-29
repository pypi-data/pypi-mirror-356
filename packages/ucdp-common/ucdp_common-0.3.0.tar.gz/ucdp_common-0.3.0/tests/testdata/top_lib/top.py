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
Top.
"""

import ucdp as u

from ucdp_common.fileliststandard import HdlFileList
from ucdp_common.ucdp_afifo import UcdpAfifoMod
from ucdp_common.ucdp_clk_buf import UcdpClkBufMod
from ucdp_common.ucdp_clk_gate import UcdpClkGateMod
from ucdp_common.ucdp_clk_mux import UcdpClkMuxMod
from ucdp_common.ucdp_clk_or import UcdpClkOrMod
from ucdp_common.ucdp_latch import UcdpLatchMod
from ucdp_common.ucdp_sfifo import UcdpSfifoMod
from ucdp_common.ucdp_sync import UcdpSyncMod


class TopMod(u.AMod):
    """Top Module."""

    filelists: u.ClassVar[u.ModFileLists] = (HdlFileList(gen="full"),)

    def _build(self) -> None:
        UcdpClkBufMod(self, "u_clk_buf")
        UcdpClkMuxMod(self, "u_clk_mux")
        UcdpClkOrMod(self, "u_clk_or")
        UcdpClkGateMod(self, "u_clk_gate")
        UcdpLatchMod(self, "u_latch")
        UcdpSyncMod(self, "u_sync0", paramdict={"rstval_p": 0})
        UcdpSyncMod(self, "u_sync1", paramdict={"rstval_p": 1})
        UcdpAfifoMod(self, "u_afifo")
        UcdpSfifoMod(self, "u_sfifo")

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
"""Simulate generated System Verilog using CocoTB."""

import os
import subprocess
from pathlib import Path

import pytest
from cocotb_test.simulator import run

# fixed seed for reproduceability
SEED = 161411072024

sim = os.getenv("SIM")
gui = os.getenv("GUI", "")
waves = "1" if os.getenv("WAVES") or gui else ""

if not sim:
    sim = os.environ["SIM"] = "verilator"
if not os.getenv("COCOTB_REDUCED_LOG_FMT"):
    os.environ["COCOTB_REDUCED_LOG_FMT"] = "1"


prjroot = os.environ["PRJROOT"] = os.getenv("VIRTUAL_ENV", "") + "/../../"

sync_fl = [
    f"{prjroot}/src/ucdp_common/ucdp_sync/rtl/ucdp_sync.sv",
    f"{prjroot}/src/ucdp_common/ucdp_sync_leaf_zero/rtl/ucdp_sync_leaf_zero.sv",
    f"{prjroot}/src/ucdp_common/ucdp_sync_leaf_one/rtl/ucdp_sync_leaf_one.sv",
]

top_fl = [
    f"{prjroot}/src/ucdp_common/ucdp_clk_buf/rtl/ucdp_clk_buf.sv",
    f"{prjroot}/src/ucdp_common/ucdp_clk_mux/rtl/ucdp_clk_mux.sv",
    f"{prjroot}/src/ucdp_common/ucdp_clk_or/rtl/ucdp_clk_or.sv",
    f"{prjroot}/src/ucdp_common/ucdp_clk_gate/rtl/ucdp_clk_gate.sv",
    f"{prjroot}/src/ucdp_common/ucdp_latch/rtl/ucdp_latch.sv",
    f"{prjroot}/src/ucdp_common/ucdp_afifo/rtl/ucdp_afifo.sv",
    f"{prjroot}/src/ucdp_common/ucdp_sfifo/rtl/ucdp_sfifo.sv",
    f"{prjroot}/tests/testdata/top_lib/top/rtl/top.sv",
]
top_fl.extend(sync_fl)

afifo_fl = [
    f"{prjroot}/src/ucdp_common/ucdp_afifo/rtl/ucdp_afifo.sv",
]
afifo_fl.extend(sync_fl)

sfifo_fl = [
    f"{prjroot}/src/ucdp_common/ucdp_sfifo/rtl/ucdp_sfifo.sv",
]

tests = [
    ("compile_test", "top", top_fl),
    ("afifo_test", "ucdp_afifo", afifo_fl),
    ("sfifo_test", "ucdp_sfifo", sfifo_fl, {"depth_p": 13}),
]


@pytest.mark.parametrize("test", tests, ids=[f"{t[1]}:{t[0]}" for t in tests])
def test_generic(test):
    """Generic, parametrized test runner."""
    top = test[1]
    sim_build = f"sim_build_{top}"
    run(
        verilog_sources=test[2],
        toplevel=top,
        module=test[0],
        parameters=test[3] if (len(test) > 3) else None,
        python_search=[f"{prjroot}/tests/"],
        extra_args=["-Wno-fatal"],
        sim_build=sim_build,
        workdir=f"sim_run_{top}_{test}",
        timescale="1ns/1ps",
        seed=SEED,
        waves=waves,
        gui=gui,
        make_args=["PYTHON3=python3"],
        plus_args=["--trace"],
    )

    # gui param above does nothing for verilator as the handling is a bit special, so we do it here
    if sim == "verilator" and waves:
        subprocess.check_call(
            ["verilator", "-Wno-fatal"]
            + test[2]
            + ["-xml-only", "--bbox-sys", "-top", top, "--xml-output", f"{sim_build}/{top}.xml"]
        )
        subprocess.check_call(["xml2stems", f"{sim_build}/{top}.xml", f"{sim_build}/{top}.stems"])

    if sim == "verilator" and gui:
        restore_path = Path(prjroot) / "tests" / f"{test[0]}.gtkw"
        restore = str(restore_path) if restore_path.exists() else ""
        cmd = [
            "gtkwave",
            "-t",
            f"{sim_build}/{top}.stems",
            "-f",
            f"{sim_build}/dump.fst",
            "-r",
            ".gtkwaverc",
        ]
        if restore:
            cmd.append("-a")
            cmd.append(restore)
        subprocess.check_call(cmd)

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
"""Systemverilog Tests."""

import os
from pathlib import Path
from shutil import which

import ucdp as u
from cocotb_test.simulator import run
from pytest import mark

SEED = 161411072024


@mark.skipif(not which("verilator"), reason="no-verilator")
def test_top(tmp_path, testdata):
    """Top."""
    top = u.load("top_lib.top", paths=(testdata,))
    u.generate(top, "*")
    _compile(tmp_path, top)


def _compile(tmp_path: Path, top: u.Top) -> None:
    fileset = u.FileSet.from_mod(top.mod, "*")

    os.environ.setdefault("SIM", "verilator")
    os.environ.setdefault("COCOTB_REDUCED_LOG_FMT", "1")

    run(
        verilog_sources=list(fileset),
        toplevel="top",
        module="tests.compile_only",
        extra_args=["-Wno-fatal"],
        sim_build=tmp_path,
        timescale="1ns/1ps",
        seed=SEED,
        make_args=["PYTHON3=python3"],
    )

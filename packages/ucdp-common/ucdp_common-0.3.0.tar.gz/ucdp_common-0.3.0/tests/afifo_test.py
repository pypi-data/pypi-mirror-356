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
Unified Chip Design Platform - AFIFO Tests.
"""

import logging

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Combine, FallingEdge, RisingEdge


# TODO put this is a generic tb lib
async def wait_clocks(clock, cycles):
    """Helper Function."""
    for _ in range(cycles):
        await RisingEdge(clock)


async def push_data(num, src_clk, src_wr_en, src_wr_data, src_wr_full):
    """Push a total of 'num' data into FIFO."""
    src_wr_en.value = 0
    for i in range(num):
        await FallingEdge(src_clk)
        while src_wr_full.value == 1:
            src_wr_en.value = 0
            await RisingEdge(src_clk)
        src_wr_en.value = 1
        src_wr_data.value = i + 0x10
        await RisingEdge(src_clk)
    src_wr_en.value = 0


async def pop_data(num, tgt_clk, tgt_rd_en, tgt_rd_data, tgt_rd_empty):
    """Pop a total of 'num' data from FIFO."""
    tgt_rd_en.value = 0
    for i in range(num):
        await FallingEdge(tgt_clk)
        while tgt_rd_empty.value == 1:
            tgt_rd_en.value = 0
            await RisingEdge(tgt_clk)
        assert tgt_rd_data == i + 0x10, f"FIFO Read Data Incorrect! Got {tgt_rd_data} expected {i + 0x10}"
        tgt_rd_en.value = 1
        await RisingEdge(tgt_clk)
    tgt_rd_en.value = 0


@cocotb.test()
async def afifo_test(dut):  # noqa: PLR0915
    """Main Test Loop."""
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)

    src_clk = dut.src_clk_i
    src_rst_an = dut.src_rst_an_i
    tgt_clk = dut.tgt_clk_i
    tgt_rst_an = dut.tgt_rst_an_i

    src_wr_en = dut.src_wr_en_i
    src_wr_data = dut.src_wr_data_i
    src_wr_full = dut.src_wr_full_o
    src_wr_space_avail = dut.src_wr_space_avail_o
    tgt_rd_en = dut.tgt_rd_en_i
    tgt_rd_data = dut.tgt_rd_data_o
    tgt_rd_empty = dut.tgt_rd_empty_o
    tgt_rd_data_avail = dut.tgt_rd_data_avail_o

    depth = 1 << (dut.awidth_p.value - 1)

    for src_period, tgt_period in [(18, 26), (26, 18)]:
        src_clk_gen = cocotb.start_soon(Clock(src_clk, period=src_period).start(cycles=220))
        tgt_clk_gen = cocotb.start_soon(Clock(tgt_clk, period=tgt_period).start(cycles=220))

        # init
        src_wr_en.value = 0
        src_wr_data.value = 0
        tgt_rd_en.value = 0

        # initial reset
        src_rst_an.value = 0
        tgt_rst_an.value = 0
        await wait_clocks(src_clk, 10)
        src_rst_an.value = 1
        tgt_rst_an.value = 1
        await wait_clocks(src_clk, 10)

        assert src_wr_full == 0, "FIFO already full?!"
        assert src_wr_space_avail == depth, "Avail Space Incorrect!"
        assert tgt_rd_empty == 1, "FIFO not empty?!"
        assert tgt_rd_data_avail == 0, "FIFO Data Avail not 0!"

        for i in range(depth):
            src_wr_en.value = 1
            src_wr_data.value = i
            await RisingEdge(src_clk)
            src_wr_en.value = 0
            await FallingEdge(src_clk)
            assert src_wr_space_avail == depth - 1 - i, "Avail Space Incorrect!"
            await wait_clocks(tgt_clk, 5)
            assert tgt_rd_data_avail == i + 1, "FIFO Data Avail Incorrect!!"
            await RisingEdge(src_clk)
        assert src_wr_full == 1, "FIFO not full?!"
        await wait_clocks(src_clk, 3)
        await RisingEdge(tgt_clk)
        for i in range(depth):
            assert tgt_rd_data == i, "FIFO Read Data Incorrect!"
            tgt_rd_en.value = 1
            await RisingEdge(tgt_clk)
            tgt_rd_en.value = 0
            await FallingEdge(tgt_clk)
            await wait_clocks(src_clk, 5)
            await RisingEdge(tgt_clk)
            assert src_wr_space_avail == i + 1, "Avail Space Incorrect!"
        assert tgt_rd_empty == 1, "FIFO not empty?!"
        await wait_clocks(src_clk, 10)

        wrburst = cocotb.start_soon(push_data(depth * 3, src_clk, src_wr_en, src_wr_data, src_wr_full))
        rdburst = cocotb.start_soon(pop_data(depth * 3, tgt_clk, tgt_rd_en, tgt_rd_data, tgt_rd_empty))
        await Combine(wrburst, rdburst)

        await Combine(src_clk_gen, tgt_clk_gen)

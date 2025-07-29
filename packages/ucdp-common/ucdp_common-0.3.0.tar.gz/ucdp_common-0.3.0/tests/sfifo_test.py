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
Unified Chip Design Platform - SFIFO Tests.
"""

import logging
import random

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Combine, FallingEdge, RisingEdge


# TODO put this is a generic tb lib
async def wait_clocks(clock, cycles):
    """Helper Function."""
    for _ in range(cycles):
        await RisingEdge(clock)


async def push_data(num, src_clk, wr_en, wr_data, wr_full):
    """Push a total of 'num' data into FIFO."""
    wr_en.value = 0
    for i in range(num):
        await FallingEdge(src_clk)
        while wr_full.value == 1:
            wr_en.value = 0
            await RisingEdge(src_clk)
        wr_en.value = 1
        wr_data.value = i + 0x10
        await RisingEdge(src_clk)
        if random.randint(1, 10) > 8:
            wr_en.value = 0
            await RisingEdge(src_clk)
    wr_en.value = 0


async def pop_data(num, src_clk, rd_en, rd_data, rd_empty):
    """Pop a total of 'num' data from FIFO."""
    rd_en.value = 0
    for i in range(num):
        await FallingEdge(src_clk)
        while rd_empty.value == 1:
            rd_en.value = 0
            await RisingEdge(src_clk)
        assert rd_data == i + 0x10, f"FIFO Read Data Incorrect! Got {rd_data} expected {i + 0x10}"
        rd_en.value = 1
        await RisingEdge(src_clk)
        if random.randint(1, 10) > 8:
            rd_en.value = 0
            await RisingEdge(src_clk)
    rd_en.value = 0


@cocotb.test()
async def afifo_test(dut):
    """Main Test Loop."""
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)

    src_clk = dut.src_clk_i
    src_rst_an = dut.src_rst_an_i

    wr_en = dut.wr_en_i
    wr_data = dut.wr_data_i
    wr_full = dut.wr_full_o
    wr_space_avail = dut.wr_space_avail_o
    rd_en = dut.rd_en_i
    rd_data = dut.rd_data_o
    rd_empty = dut.rd_empty_o
    rd_data_avail = dut.rd_data_avail_o

    depth = dut.depth_p.value

    cocotb.start_soon(Clock(src_clk, period=10).start())

    # init
    wr_en.value = 0
    wr_data.value = 0
    rd_en.value = 0

    # initial reset
    src_rst_an.value = 0
    await wait_clocks(src_clk, 10)
    src_rst_an.value = 1
    await wait_clocks(src_clk, 10)

    assert wr_full == 0, "FIFO already full?!"
    assert wr_space_avail == depth, "Avail Space Incorrect!"
    assert rd_empty == 1, "FIFO not empty?!"
    assert rd_data_avail == 0, "FIFO Data Avail not 0!"

    for i in range(depth):
        wr_en.value = 1
        wr_data.value = i
        await RisingEdge(src_clk)
        wr_en.value = 0
        await FallingEdge(src_clk)
        assert wr_space_avail == depth - 1 - i, "Avail Space Incorrect!"
        assert rd_data_avail == i + 1, "FIFO Data Avail Incorrect!"
        await wait_clocks(src_clk, 5)
    assert wr_full == 1, "FIFO not full?!"

    for i in range(depth):
        assert rd_data == i, "FIFO Read Data Incorrect!"
        rd_en.value = 1
        await RisingEdge(src_clk)
        rd_en.value = 0
        await FallingEdge(src_clk)
        assert wr_space_avail == i + 1, "Avail Space Incorrect!"
        await wait_clocks(src_clk, 5)
    assert rd_empty == 1, "FIFO not empty?!"

    wrburst = cocotb.start_soon(push_data(3 * depth, src_clk, wr_en, wr_data, wr_full))
    rdburst = cocotb.start_soon(pop_data(3 * depth, src_clk, rd_en, rd_data, rd_empty))
    await Combine(wrburst, rdburst)
    await wait_clocks(src_clk, 10)

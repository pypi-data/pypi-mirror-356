// GENERATE INPLACE BEGIN head() ===============================================
//
//  MIT License
//
//  Copyright (c) 2024-2025 nbiotcloud
//
//  Permission is hereby granted, free of charge, to any person obtaining a copy
//  of this software and associated documentation files (the "Software"), to deal
//  in the Software without restriction, including without limitation the rights
//  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//  copies of the Software, and to permit persons to whom the Software is
//  furnished to do so, subject to the following conditions:
//
//  The above copyright notice and this permission notice shall be included in all
//  copies or substantial portions of the Software.
//
//  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//  SOFTWARE.
//
// =============================================================================
//
// Library:    ucdp_common
// Module:     ucdp_clk_gate
// Data Model: UcdpClkGateMod
//             ucdp_common/ucdp_clk_gate.py
//
// =============================================================================

`begin_keywords "1800-2009"
`default_nettype none  // implicit wires are forbidden

module ucdp_clk_gate (
  input  wire  clk_i, // Clock
  input  wire  en_i,  // Enable
  output logic clk_o  // Clock output
);


// GENERATE INPLACE END head ===================================================

  logic latch_r;

  always_latch begin : proc_latch
    if (clk_i == 1'b0) begin
      latch_r <= en_i;
    end
  end

  assign clk_o = clk_i & latch_r;


  `ifdef SIM
  `ifndef SYN

  logic issue_seen_r;
  logic ignorepos_r;
  logic ignoreneg_r;
  initial issue_seen_r = 1'b0;
  initial ignorepos_r = 1'b1;  // ignore first prop at startup to initialize latch
  initial ignoreneg_r = 1'b1;  // ignore first prop at startup to initialize latch

  always_ff @(posedge clk_i) begin : proc_ignorepos_r
    ignorepos_r <= 1'b0;
  end

  always_ff @(negedge clk_i) begin : proc_ignoreneg_r
    if (ignorepos_r == 1'b0) begin
      ignoreneg_r <= 1'b0;
    end
  end

  always_comb @(clk_i) begin : proc_test_x
    if ((clk_i == 1'b1) && (clk_o === 1'bx) && (issue_seen_r == 1'b0) && (ignorepos_r == 1'b0) && (ignoreneg_r == 1'b0)) begin
      $display("Warning! Issue in clock propagation, clock becomes X in ucdp_clock_gate %m. Check your enable! Time:", $time);
      issue_seen_r = 1'b1;
    end
  end

  `endif
  `endif

// GENERATE INPLACE BEGIN tail() ===============================================
endmodule // ucdp_clk_gate

`default_nettype wire
`end_keywords
// GENERATE INPLACE END tail ===================================================

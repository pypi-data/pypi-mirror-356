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
// Module:     ucdp_clk_or
// Data Model: UcdpClkOrMod
//             ucdp_common/ucdp_clk_or.py
//
// =============================================================================

`begin_keywords "1800-2009"
`default_nettype none  // implicit wires are forbidden

module ucdp_clk_or (
  input  wire  clka_i, // Clock A
  input  wire  clkb_i, // Clock B
  output logic clk_o   // Clock output
);


// GENERATE INPLACE END head ===================================================

  assign clk_o = clka_i | clkb_i;

`ifdef SIM
  // pragma coverage off
  `ifndef UCDP_NO_CLK_VERIF
  logic warna;
  logic seena0;
  logic seena1;

  logic warnb;
  logic seenb0;
  logic seenb1;

  initial begin: proc_init
    warna = 1'b1;
    seena0 = 1'b0;
    seena1 = 1'b0;
    warnb = 1'b1;
    seenb0 = 1'b0;
    seenb1 = 1'b0;
  end

  //lint_checking METAEQ off
  always_comb begin : proc_warn
    // notify about corrupt clk just once
    if (clka_i === 1'b0) begin
      seena0 = 1'b1;
    end else if (clka_i === 1'b1) begin
      seena1 = 1'b1;
    end else begin
      if (warna == 1'b0) begin
        $display($time, "ps\t SIMERROR: %m Corrupt Clock clka_i",);
      end
      warna = 1'b1;
      seena0 = 1'b0;
      seena1 = 1'b0;
    end
    if ((seena0 == 1'b1) && (seena1 == 1'b1)) begin
      warna = 1'b0;
    end

    if (clkb_i === 1'b0) begin
      seenb0 = 1'b1;
    end else if (clkb_i === 1'b1) begin
      seenb1 = 1'b1;
    end else begin
      if (warnb == 1'b0) begin
        $display($time, "ps\t SIMERROR: %m Corrupt Clock clkb_i",);
      end
      warnb = 1'b1;
      seenb0 = 1'b0;
      seenb1 = 1'b0;
    end
    if ((seenb0 == 1'b1) && (seenb1 == 1'b1)) begin
      warnb = 1'b0;
    end
  end
  //lint_checking METAEQ on
  `endif // UCDP_NO_CLK_VERIF
  // pragma coverage on
`endif // SIM

// GENERATE INPLACE BEGIN tail() ===============================================
endmodule // ucdp_clk_or

`default_nettype wire
`end_keywords
// GENERATE INPLACE END tail ===================================================

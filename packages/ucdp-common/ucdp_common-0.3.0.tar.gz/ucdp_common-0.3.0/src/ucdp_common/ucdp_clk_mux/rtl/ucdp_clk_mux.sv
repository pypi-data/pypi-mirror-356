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
// Module:     ucdp_clk_mux
// Data Model: UcdpClkMuxMod
//             ucdp_common/ucdp_clk_mux.py
//
// =============================================================================

`begin_keywords "1800-2009"
`default_nettype none  // implicit wires are forbidden

module ucdp_clk_mux (
  input  wire  clka_i, // Clock A
  input  wire  clkb_i, // Clock B
  input  wire  sel_i,  // Select
  output logic clk_o   // Clock output
);



  // ------------------------------------------------------
  //  Local Parameter
  // ------------------------------------------------------
  // sel
  localparam integer sel_width_p   = 1;    // Width in Bits
  localparam logic   sel_min_p     = 1'b0; // Minimal Value
  localparam logic   sel_max_p     = 1'b1; // Maximal Value
  localparam logic   sel_a_e       = 1'b0;
  localparam logic   sel_b_e       = 1'b1;
  localparam logic   sel_default_p = 1'b0; // Default Value

// GENERATE INPLACE END head ===================================================


  assign clk_o = (sel_i == sel_b_e) ? clkb_i : clka_i;


// GENERATE INPLACE BEGIN tail() ===============================================
endmodule // ucdp_clk_mux

`default_nettype wire
`end_keywords
// GENERATE INPLACE END tail ===================================================

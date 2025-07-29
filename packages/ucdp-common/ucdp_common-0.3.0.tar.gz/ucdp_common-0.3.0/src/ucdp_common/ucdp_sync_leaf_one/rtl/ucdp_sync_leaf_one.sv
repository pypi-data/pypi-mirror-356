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
// Module:     ucdp_sync_leaf_one
// Data Model: UcdpSyncLeafOneMod
//             ucdp_common/ucdp_sync_leaf_one.py
//
// =============================================================================

`begin_keywords "1800-2009"
`default_nettype none  // implicit wires are forbidden

module ucdp_sync_leaf_one (
  // tgt_i: Clock and Reset
  input  wire  tgt_clk_i,    // Clock
  input  wire  tgt_rst_an_i, // Async Reset (Low-Active)
  // -
  input  wire  scan_shift_i, // Scan Shift Phase
  input  wire  d_i,          // data input
  output logic q_o           // data output
);


// GENERATE INPLACE END head ===================================================


  logic firststage_sync_line_r;
  logic sync_line_r;
  logic d_s;

  always_ff @ (posedge tgt_clk_i or negedge tgt_rst_an_i) begin : proc_sync
    if (tgt_rst_an_i == 1'b0) begin
      firststage_sync_line_r <= 1'b1;
      sync_line_r            <= 1'b1;
    end else begin
      firststage_sync_line_r  <= d_s;
      sync_line_r             <= firststage_sync_line_r;
    end
  end

  assign q_o = sync_line_r;


  // jitter emulation
  // pragma coverage off
`ifdef SIM
  `ifndef UCDP_SYNC_NO_JITTER
    reg  jitter_d_r;
    reg  jitter_sel_r;
    reg  jitter_sel_s;

    always_ff @ (posedge tgt_clk_i or negedge tgt_rst_an_i) begin : proc_jitter_seq
      if (tgt_rst_an_i == 1'b0) begin
        jitter_d_r   <= 1'b1;
        jitter_sel_r <= 1'b0;
      end else begin
        jitter_d_r   <= d_i;
        jitter_sel_r <= jitter_sel_s;
      end
    end

    // trigger new jitter selection only after edges and if there is no influence on the resulting signal
    always_comb begin : proc_jitter_sel
      if ((jitter_d_r == d_i) && (firststage_sync_line_r != sync_line_r)) begin
        jitter_sel_s = (($random % 32'd2) == 32'd0) ? 1'b1 : 1'b0;
      end else begin
        jitter_sel_s = jitter_sel_r;
      end
    end

    assign d_s = (jitter_sel_s == 1'b1) ? jitter_d_r : d_i;
  `else // UCDP_SYNC_NO_JITTER
    assign d_s = d_i;
  `endif // UCDP_SYNC_NO_JITTER

`else // SIM
  assign d_s = d_i;
`endif // SIM
  // pragma coverage on


// GENERATE INPLACE BEGIN tail() ===============================================
endmodule // ucdp_sync_leaf_one

`default_nettype wire
`end_keywords
// GENERATE INPLACE END tail ===================================================

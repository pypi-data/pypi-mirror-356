// =============================================================================
//
//   @generated @fully-generated
//
//   THIS FILE IS GENERATED!!! DO NOT EDIT MANUALLY. CHANGES ARE LOST.
//
// =============================================================================
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
// Library:    top_lib
// Module:     top
// Data Model: TopMod
//             top_lib/top.py
//
// =============================================================================

`begin_keywords "1800-2009"
`default_nettype none  // implicit wires are forbidden

module top();



  // ------------------------------------------------------
  //  Local Parameter
  // ------------------------------------------------------
  // edge_spec
  localparam integer       edge_spec_width_p   = 2;    // Width in Bits
  localparam logic   [1:0] edge_spec_min_p     = 2'h0; // Minimal Value
  localparam logic   [1:0] edge_spec_max_p     = 2'h3; // Maximal Value
  localparam logic   [1:0] edge_spec_none_e    = 2'h0; // None
  localparam logic   [1:0] edge_spec_rise_e    = 2'h1; // Rising edge.
  localparam logic   [1:0] edge_spec_fall_e    = 2'h2; // Falling edge.
  localparam logic   [1:0] edge_spec_any_e     = 2'h3; // Any edge.
  localparam logic   [1:0] edge_spec_default_p = 2'h0; // Default Value


  // ------------------------------------------------------
  //  ucdp_common.ucdp_clk_buf: u_clk_buf
  // ------------------------------------------------------
  ucdp_clk_buf u_clk_buf (
    .clk_i(1'b0), // TODO - Clock input
    .clk_o(    )  // TODO - Clock output
  );


  // ------------------------------------------------------
  //  ucdp_common.ucdp_clk_mux: u_clk_mux
  // ------------------------------------------------------
  ucdp_clk_mux u_clk_mux (
    .clka_i(1'b0), // TODO - Clock A
    .clkb_i(1'b0), // TODO - Clock B
    .sel_i (1'b0), // TODO - Select
    .clk_o (    )  // TODO - Clock output
  );


  // ------------------------------------------------------
  //  ucdp_common.ucdp_clk_or: u_clk_or
  // ------------------------------------------------------
  ucdp_clk_or u_clk_or (
    .clka_i(1'b0), // TODO - Clock A
    .clkb_i(1'b0), // TODO - Clock B
    .clk_o (    )  // TODO - Clock output
  );


  // ------------------------------------------------------
  //  ucdp_common.ucdp_clk_gate: u_clk_gate
  // ------------------------------------------------------
  ucdp_clk_gate u_clk_gate (
    .clk_i(1'b0), // TODO - Clock
    .en_i (1'b0), // TODO - Enable
    .clk_o(    )  // TODO - Clock output
  );


  // ------------------------------------------------------
  //  ucdp_common.ucdp_latch: u_latch
  // ------------------------------------------------------
  ucdp_latch u_latch (
    .main_clk_i           (1'b0      ), // TODO - Clock
    .main_rst_an_i        (1'b0      ), // TODO - Async Reset (Low-Active)
    .dft_mode_test_mode_i (1'b0      ), // TODO - Test Mode
    .dft_mode_scan_mode_i (1'b0      ), // TODO - Logic Scan-Test Mode
    .dft_mode_scan_shift_i(1'b0      ), // TODO - Scan Shift Phase
    .dft_mode_mbist_mode_i(1'b0      ), // TODO - Memory Built-In Self-Test
    .ld_i                 (1'b0      ), // TODO - Load
    .d_i                  ({1 {1'b0}}), // TODO - Data Input
    .q_o                  (          )  // TODO - Data Output
  );


  // ------------------------------------------------------
  //  ucdp_common.ucdp_sync: u_sync0
  // ------------------------------------------------------
  ucdp_sync #(
    .rstval_p(1'b0) // Reset Value
  ) u_sync0 (
    .tgt_clk_i            (1'b0), // TODO - Clock
    .tgt_rst_an_i         (1'b0), // TODO - Async Reset (Low-Active)
    .dft_mode_test_mode_i (1'b0), // TODO - Test Mode
    .dft_mode_scan_mode_i (1'b0), // TODO - Logic Scan-Test Mode
    .dft_mode_scan_shift_i(1'b0), // TODO - Scan Shift Phase
    .dft_mode_mbist_mode_i(1'b0), // TODO - Memory Built-In Self-Test
    .d_i                  (1'b0), // TODO - Data Input
    .q_o                  (    ), // TODO - Data Output
    .edge_o               (    )  // TODO - Edge Output
  );


  // ------------------------------------------------------
  //  ucdp_common.ucdp_sync: u_sync1
  // ------------------------------------------------------
  ucdp_sync #(
    .rstval_p(1'b1) // Reset Value
  ) u_sync1 (
    .tgt_clk_i            (1'b0), // TODO - Clock
    .tgt_rst_an_i         (1'b0), // TODO - Async Reset (Low-Active)
    .dft_mode_test_mode_i (1'b0), // TODO - Test Mode
    .dft_mode_scan_mode_i (1'b0), // TODO - Logic Scan-Test Mode
    .dft_mode_scan_shift_i(1'b0), // TODO - Scan Shift Phase
    .dft_mode_mbist_mode_i(1'b0), // TODO - Memory Built-In Self-Test
    .d_i                  (1'b0), // TODO - Data Input
    .q_o                  (    ), // TODO - Data Output
    .edge_o               (    )  // TODO - Edge Output
  );


  // ------------------------------------------------------
  //  ucdp_common.ucdp_afifo: u_afifo
  // ------------------------------------------------------
  ucdp_afifo u_afifo (
    .src_clk_i            (1'b0      ), // TODO - Clock
    .src_rst_an_i         (1'b0      ), // TODO - Async Reset (Low-Active)
    .tgt_clk_i            (1'b0      ), // TODO - Clock
    .tgt_rst_an_i         (1'b0      ), // TODO - Async Reset (Low-Active)
    .dft_mode_test_mode_i (1'b0      ), // TODO - Test Mode
    .dft_mode_scan_mode_i (1'b0      ), // TODO - Logic Scan-Test Mode
    .dft_mode_scan_shift_i(1'b0      ), // TODO - Scan Shift Phase
    .dft_mode_mbist_mode_i(1'b0      ), // TODO - Memory Built-In Self-Test
    .src_wr_en_i          (1'b0      ), // TODO - Source Write Enable
    .src_wr_data_i        ({8 {1'b0}}), // TODO - Source Write Data
    .src_wr_full_o        (          ), // TODO - FIFO Full
    .src_wr_space_avail_o (          ), // TODO - FIFO Space Available
    .tgt_rd_en_i          (1'b0      ), // TODO - Target Read Enable
    .tgt_rd_data_o        (          ), // TODO - Target Read Data
    .tgt_rd_empty_o       (          ), // TODO - FIFO empty
    .tgt_rd_data_avail_o  (          )  // TODO - FIFO Data Available
  );


  // ------------------------------------------------------
  //  ucdp_common.ucdp_sfifo: u_sfifo
  // ------------------------------------------------------
  ucdp_sfifo u_sfifo (
    .src_clk_i            (1'b0      ), // TODO - Clock
    .src_rst_an_i         (1'b0      ), // TODO - Async Reset (Low-Active)
    .dft_mode_test_mode_i (1'b0      ), // TODO - Test Mode
    .dft_mode_scan_mode_i (1'b0      ), // TODO - Logic Scan-Test Mode
    .dft_mode_scan_shift_i(1'b0      ), // TODO - Scan Shift Phase
    .dft_mode_mbist_mode_i(1'b0      ), // TODO - Memory Built-In Self-Test
    .wr_en_i              (1'b0      ), // TODO - Write Enable
    .wr_data_i            ({8 {1'b0}}), // TODO - Write Data
    .wr_full_o            (          ), // TODO - FIFO Full
    .wr_space_avail_o     (          ), // TODO - FIFO Space Available
    .rd_en_i              (1'b0      ), // TODO - Read Enable
    .rd_data_o            (          ), // TODO - Read Data
    .rd_empty_o           (          ), // TODO - FIFO empty
    .rd_data_avail_o      (          )  // TODO - FIFO Data Available
  );

endmodule // top

`default_nettype wire
`end_keywords

// =============================================================================
//
//   @generated @fully-generated
//
//   THIS FILE IS GENERATED!!! DO NOT EDIT MANUALLY. CHANGES ARE LOST.
//
// =============================================================================

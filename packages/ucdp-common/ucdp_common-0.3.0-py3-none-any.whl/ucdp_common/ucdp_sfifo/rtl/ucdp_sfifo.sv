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
// Module:     ucdp_sfifo
// Data Model: UcdpSfifoMod
//             ucdp_common/ucdp_sfifo.py
//
// =============================================================================

`begin_keywords "1800-2009"
`default_nettype none  // implicit wires are forbidden

module ucdp_sfifo #(
  parameter integer dwidth_p = 8,                  // FIFO Data Width
  parameter integer depth_p  = 4,                  // FIFO Depth
  parameter integer awidth_p = $clog2(depth_p + 1) // FIFO Address Width
) (
  // src_i: Clock and Reset
  input  wire                 src_clk_i,             // Clock
  input  wire                 src_rst_an_i,          // Async Reset (Low-Active)
  // dft_mode_i: Test Control
  input  wire                 dft_mode_test_mode_i,  // Test Mode
  input  wire                 dft_mode_scan_mode_i,  // Logic Scan-Test Mode
  input  wire                 dft_mode_scan_shift_i, // Scan Shift Phase
  input  wire                 dft_mode_mbist_mode_i, // Memory Built-In Self-Test
  // -
  input  wire                 wr_en_i,               // Write Enable
  input  wire  [dwidth_p-1:0] wr_data_i,             // Write Data
  output logic                wr_full_o,             // FIFO Full
  output logic [awidth_p-1:0] wr_space_avail_o,      // FIFO Space Available
  input  wire                 rd_en_i,               // Read Enable
  output logic [dwidth_p-1:0] rd_data_o,             // Read Data
  output logic                rd_empty_o,            // FIFO empty
  output logic [awidth_p-1:0] rd_data_avail_o        // FIFO Data Available
);


// GENERATE INPLACE END head ===================================================

  localparam integer        pwidth_p = $clog2(depth_p);
  localparam [pwidth_p-1:0] ptr_inc_p = 1;
  localparam [pwidth_p-1:0] ptr_max_p = depth_p-1;
  localparam [awidth_p-1:0] load_inc_p = 1;
  localparam [awidth_p-1:0] almost_full_p = depth_p-1;
  localparam [awidth_p-1:0] almost_empty_p = 1;

  logic [pwidth_p-1:0] wr_ptr_r;
  logic [pwidth_p-1:0] rd_ptr_r;
  logic [awidth_p-1:0] load_r;
  logic [awidth_p-1:0] space_r;
  logic empty_r;
  logic full_r;
  logic wr_en_s;
  logic rd_en_s;

  logic [dwidth_p-1:0] mem_r [depth_p-1:0];


  assign wr_en_s = wr_en_i & (~full_r | rd_en_i);
  assign rd_en_s = rd_en_i & ~empty_r;


  always_ff @ (posedge src_clk_i or negedge src_rst_an_i) begin: proc_ctrl
    if (src_rst_an_i == 1'b0) begin
      wr_ptr_r <= {pwidth_p{1'b0}};
      rd_ptr_r <= {pwidth_p{1'b0}};
      load_r <= {awidth_p{1'b0}};
      space_r <= depth_p[awidth_p-1:0];
      empty_r <= 1'b1;
      full_r <= 1'b0;
    end else begin
      if (wr_en_s == 1'b1) begin
        if (wr_ptr_r == ptr_max_p) begin
          wr_ptr_r <= {pwidth_p{1'b0}};
        end else begin
          wr_ptr_r <= wr_ptr_r + ptr_inc_p;
        end
      end

      if (rd_en_s == 1'b1) begin
        if (rd_ptr_r == ptr_max_p) begin
          rd_ptr_r <= {pwidth_p{1'b0}};
        end else begin
          rd_ptr_r <= rd_ptr_r + ptr_inc_p;
        end
      end

      if ((wr_en_s == 1'b1) && (rd_en_s == 1'b0)) begin // increase load
        load_r <= load_r + load_inc_p;
        space_r <= space_r - load_inc_p;
        if (load_r == almost_full_p) begin
          full_r <= 1'b1;
        end else begin
          full_r <= 1'b0;
        end
        empty_r <= 1'b0;
      end else if ((rd_en_s == 1'b1) && (wr_en_s == 1'b0)) begin // decrease load
        load_r <= load_r - load_inc_p;
        space_r <= space_r + load_inc_p;
        if (load_r == almost_empty_p) begin
          empty_r <= 1'b1;
        end else begin
          empty_r <= 1'b0;
        end
        full_r <= 1'b0;
      end
    end
  end


  always_ff @ (posedge src_clk_i) begin: proc_mem
    if (wr_en_i & (~full_r | rd_en_i)) begin
      mem_r[wr_ptr_r] <= wr_data_i;
    end
  end

  assign rd_data_o = mem_r[rd_ptr_r];
  assign wr_full_o = full_r;
  assign rd_empty_o = empty_r;
  assign wr_space_avail_o = space_r;
  assign rd_data_avail_o = load_r;

// GENERATE INPLACE BEGIN tail() ===============================================
endmodule // ucdp_sfifo

`default_nettype wire
`end_keywords
// GENERATE INPLACE END tail ===================================================

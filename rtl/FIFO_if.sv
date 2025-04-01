interface FIFO_if (clk);
    input clk;
    localparam FIFO_WIDTH = 16;
    localparam FIFO_DEPTH = 8;
    logic [FIFO_WIDTH-1:0] data_in;
    logic clk, rst_n, wr_en, rd_en;
    logic [FIFO_WIDTH-1:0] data_out;
    logic wr_ack, overflow;
    logic full, empty, almostfull, almostempty, underflow;

modport dut (input clk ,data_in, rst_n, wr_en, rd_en, 
            output data_out,wr_ack, overflow,full, empty, almostfull, almostempty, underflow);

endinterface 
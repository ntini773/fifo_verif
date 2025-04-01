module FIFO #(
    parameter FIFO_WIDTH = 16,
    parameter FIFO_DEPTH = 8
)(
    input  logic clk,
    input  logic rst_n,
    input  logic [FIFO_WIDTH-1:0] data_in,
    input  logic wr_en,
    input  logic rd_en,

    output logic [FIFO_WIDTH-1:0] data_out,
    output logic wr_ack,
    output logic overflow,
    output logic full,
    output logic empty,
    output logic almostfull,
    output logic almostempty,
    output logic underflow
);

    localparam max_fifo_addr = $clog2(FIFO_DEPTH);

    reg [FIFO_WIDTH-1:0] mem [FIFO_DEPTH-1:0];
    reg [max_fifo_addr-1:0] wr_ptr, rd_ptr;
    reg [max_fifo_addr:0] count;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            wr_ptr <= 0;
            overflow <= 0;
        end else if (wr_en && count < FIFO_DEPTH) begin
            mem[wr_ptr] <= data_in;
            wr_ack <= 1;
            overflow <= 0;
            wr_ptr <= wr_ptr + 1;
        end else begin
            wr_ack <= 0;
            if (full && wr_en)
                overflow <= 1;
            else
                overflow <= 0;
        end
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rd_ptr <= 0;
            underflow <= 0;
        end else if (rd_en && count != 0) begin
            data_out <= mem[rd_ptr];
            rd_ptr <= rd_ptr + 1;
            underflow <= 0;
        end else begin
            if (empty && rd_en)
                underflow <= 1;
            else
                underflow <= 0;
        end
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count <= 0;
        end else begin
            if ((wr_en && !rd_en) && !full)
                count <= count + 1;
            else if ((!wr_en && rd_en) && !empty)
                count <= count - 1;
            else if ((wr_en && rd_en) && empty)
                count <= count + 1;
            else if ((wr_en && rd_en) && full)
                count <= count - 1;
        end
    end

    assign full         = (count == FIFO_DEPTH);
    assign empty        = (count == 0);
    assign almostfull   = (count == FIFO_DEPTH - 1);
    assign almostempty  = (count == 1);

    `ifdef SIM
    // Assertions and covers
    property full_check;
        @(posedge clk) disable iff(!rst_n) (count == FIFO_DEPTH) |-> (full == 1'b1);
    endproperty

    property empty_check;
        @(posedge clk) disable iff(!rst_n) (count == 0) |-> (empty == 1'b1);
    endproperty

    property underflow_check;
        @(posedge clk) disable iff(!rst_n) (empty && rd_en) |-> (underflow == 1'b1);
    endproperty

    property overflow_check;
        @(posedge clk) disable iff(!rst_n) (full && wr_en) |-> (overflow == 1'b1);
    endproperty

    full_check_assertion       : assert property(full_check);
    empty_check_assertion      : assert property(empty_check);
    underflow_check_assertion  : assert property(underflow_check);
    overflow_check_assertion   : assert property(overflow_check);

    full_check_cover       : cover property(full_check);
    empty_check_cover      : cover property(empty_check);
    underflow_check_cover  : cover property(underflow_check);
    overflow_check_cover   : cover property(overflow_check);
    `endif

endmodule

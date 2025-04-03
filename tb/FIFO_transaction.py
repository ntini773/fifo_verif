from pyuvm import *

class FifoTransaction(uvm_sequence_item):
    def __init__(self, name="FifoTransaction"):
        super().__init__(name)
        self.data_in = 0
        self.rst_n = 1
        self.wr_en = 0
        self.rd_en = 0

        self.data_out = 0
        self.wr_ack = 0
        self.overflow = 0
        self.full = 0
        self.empty = 0
        self.almostfull = 0
        self.almostempty = 0
        self.underflow = 0

    def __str__(self):
        return (f"data_in={self.data_in:016b}, rst_n={self.rst_n}, wr_en={self.wr_en}, rd_en={self.rd_en}, "
                f"data_out={self.data_out:016b}, wr_ack={self.wr_ack}, overflow={self.overflow}, "
                f"full={self.full}, empty={self.empty}, almostfull={self.almostfull}, "
                f"almostempty={self.almostempty}, underflow={self.underflow}")

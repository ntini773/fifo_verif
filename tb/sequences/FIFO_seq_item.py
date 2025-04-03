from pyuvm import *
import random

class FIFOSeqItem(uvm_sequence_item):

    FIFO_WIDTH = 16

    def __init__(self, name="FIFOSeqItem"):
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

    def randomize(self):
        # Reset signal biased to be 1 (inactive)
        self.rst_n = random.choices([1, 0], weights=[95, 5])[0]
        self.wr_en = random.choices([1, 0], weights=[70, 30])[0]
        self.rd_en = random.choices([1, 0], weights=[70, 30])[0]

        self.data_in = random.getrandbits(self.FIFO_WIDTH)

        return True  # indicate success like SV `randomize()`

    def convert2string(self):
        return (
            f"data_in={self.data_in:016b}, rst_n={self.rst_n}, wr_en={self.wr_en}, rd_en={self.rd_en},\n"
            f"data_out={self.data_out:016b}, wr_ack={self.wr_ack}, overflow={self.overflow},\n"
            f"full={self.full}, empty={self.empty}, almostfull={self.almostfull},\n"
            f"almostempty={self.almostempty}, underflow={self.underflow}"
        )

    def compare_response(self, other):
        if not isinstance(other, FIFOSeqItem):
            uvm_fatal("COMPARE", "compare_response called with invalid type")

        return (
            self.wr_ack == other.wr_ack and
            self.overflow == other.overflow and
            self.full == other.full and
            self.empty == other.empty and
            self.almostfull == other.almostfull and
            self.almostempty == other.almostempty and
            self.underflow == other.underflow
        )

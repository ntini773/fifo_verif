from pyuvm import *
from pyuvm import uvm_scoreboard, uvm_tlm_analysis_fifo 
from .sequences.FIFO_seq_item import FIFOSeqItem

class FIFOScoreboard(uvm_scoreboard):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        # FIFO to receive transactions from monitor or other producer
        self.received_items = []

        # Local memory and reference model state
        self.ref_seq_item = FIFOSeqItem("ref_seq_item")
        self.mem = []
        self.FIFO_DEPTH = 8
        self.FIFO_WIDTH = 16
    
    def write(self, seq_item):
        self.logger.info(f"[SCOREBOARD] Got item: {seq_item}")
        self.received_items.append(seq_item)

    def connect_phase(self):
        # No connect needed from scoreboard side
        pass

    async def run_phase(self):
        while True:
            # Wait for incoming data via the FIFO
            seq_item = await self.out_fifo.get()
            self.predict_output(seq_item)

            self.logger.info(f"MEM SIZE = {len(self.mem)}")
            if seq_item.rst_n:
                data_str = f"Expected: {self.ref_seq_item.convert2string()} \nFound: {seq_item.convert2string()}"
                if not self.ref_seq_item.compare_response(seq_item):
                    self.logger.error(f"\nFAIL: {data_str}")
                else:
                    self.logger.info(f"\nPASS: {data_str}")

    def predict_output(self, seq_item):
        if not seq_item.rst_n:
            self.mem.clear()
            return

        ref = self.ref_seq_item
        ref.copy_from(seq_item)

        # Default predictions
        ref.wr_ack = 0
        ref.overflow = 0
        ref.underflow = 0
        ref.data_out = 0

        if not seq_item.wr_en and not seq_item.rd_en:
            return

        if seq_item.wr_en and seq_item.rd_en:
            if self.is_empty():
                ref.underflow = 1
                ref.wr_ack = 1
                self.mem.append(seq_item.data_in)
            elif self.is_full():
                ref.overflow = 1
                ref.data_out = self.mem.pop(0)
            else:
                ref.data_out = self.mem.pop(0)
                self.mem.append(seq_item.data_in)
                ref.wr_ack = 1

        elif seq_item.rd_en:
            if self.is_empty():
                ref.underflow = 1
            else:
                ref.data_out = self.mem.pop(0)

        elif seq_item.wr_en:
            if self.is_full():
                ref.overflow = 1
            else:
                self.mem.append(seq_item.data_in)
                ref.wr_ack = 1

        # Update status flags
        ref.full = self.is_full()
        ref.empty = self.is_empty()
        ref.almostfull = (len(self.mem) == self.FIFO_DEPTH - 1)
        ref.almostempty = (len(self.mem) == 1)

    def is_empty(self):
        return len(self.mem) == 0

    def is_full(self):
        return len(self.mem) == self.FIFO_DEPTH

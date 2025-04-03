from pyuvm import *
from .FIFO_seq_item import FIFOSeqItem  # Assuming FIFOSeqItem is defined in this file

class FIFOReadSeq(uvm_sequence):

    def __init__(self, name="FIFOReadSeq"):
        super().__init__(name)

    async def body(self):
        for _ in range(10):
            seq_item = FIFOSeqItem("seq_item")
            seq_item.randomize()
            seq_item.wr_en = 0
            seq_item.rd_en = 1
            await self.start_item(seq_item)
            self.finish_item(seq_item)

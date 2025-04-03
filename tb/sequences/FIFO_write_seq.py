from pyuvm import *
from .FIFO_seq_item  import FIFOSeqItem

class FIFOWriteSeq(uvm_sequence):
    def __init__(self, name="FIFOWriteSeq"):
        super().__init__(name)

    async def body(self):
        for _ in range(10):
            seq_item = FIFOSeqItem("seq_item")
            await self.start_item(seq_item)

            # Randomize with constraints
            seq_item.randomize()
            seq_item.wr_en = 1
            seq_item.rd_en = 0

            await self.finish_item(seq_item)

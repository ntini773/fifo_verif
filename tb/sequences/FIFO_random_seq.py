from pyuvm import *
from .FIFO_seq_item import FIFOSeqItem  # Import the sequence item class you defined

class FIFORandomSeq(uvm_sequence):

    def __init__(self, name="FIFORandomSeq"):
        super().__init__(name)

    async def body(self):
        for _ in range(1000):
            seq_item = FIFOSeqItem("seq_item")
            seq_item.randomize()
            await self.start_item(seq_item)
            self.finish_item(seq_item)

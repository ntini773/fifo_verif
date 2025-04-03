from pyuvm import *
from .FIFO_seq_item import FIFOSeqItem  # Assuming you have FIFOSeqItem defined already

class FIFOResetSeq(uvm_sequence):

    def __init__(self, name="FIFOResetSeq"):
        super().__init__(name)

    async def body(self):
        seq_item = FIFOSeqItem("seq_item")
        seq_item.randomize()
        seq_item.rst_n = 0  # Apply reset
        await self.start_item(seq_item)
        self.finish_item(seq_item)

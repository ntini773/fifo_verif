# fifo_driver.py

import cocotb
from cocotb.triggers import FallingEdge
from pyuvm import *

class FIFODriver(uvm_driver):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.vif = None

    async def run_phase(self):
        self.logger.info("FIFO Driver run_phase started")
        while True:
            seq_item = await self.seq_item_port.get_next_item()
            await self.drive_transaction(seq_item)
            self.seq_item_port.item_done()

    async def drive_transaction(self, seq_item):
        await FallingEdge(self.vif.clk)
        self.vif.rst_n.value = seq_item.rst_n
        self.vif.rd_en.value = seq_item.rd_en
        self.vif.wr_en.value = seq_item.wr_en
        self.vif.data_in.value = seq_item.data_in
        self.logger.debug(f"Driven: rst_n={seq_item.rst_n}, rd_en={seq_item.rd_en}, wr_en={seq_item.wr_en}, data_in={seq_item.data_in}")

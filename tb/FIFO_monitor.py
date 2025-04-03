from pyuvm import *
from .sequences.FIFO_seq_item import FIFOSeqItem
import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
from cocotb.queue import QueueEmpty

class FIFOMonitor(uvm_monitor):

    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.vif = None  # Should be set in build_phase or via config
        self.analysis_port = uvm_analysis_port("analysis_port", self)

    def build_phase(self):
        self.vif = ConfigDB().get(self, "", "vif")
        if self.vif is None:
            uvm_fatal("MON", "Virtual interface (vif) not found in config DB")

    async def run_phase(self):
        while True:
            await RisingEdge(self.vif.clk)
            await Timer(2, units="ns")  # Matches #2 delay after posedge
            seq_item = FIFOSeqItem("seq_item")

            seq_item.rst_n = int(self.vif.rst_n.value)
            seq_item.rd_en = int(self.vif.rd_en.value)
            seq_item.wr_en = int(self.vif.wr_en.value)
            seq_item.data_in = int(self.vif.data_in.value)
            seq_item.wr_ack = int(self.vif.wr_ack.value)
            seq_item.overflow = int(self.vif.overflow.value)
            seq_item.full = int(self.vif.full.value)
            seq_item.empty = int(self.vif.empty.value)
            seq_item.almostfull = int(self.vif.almostfull.value)
            seq_item.almostempty = int(self.vif.almostempty.value)
            seq_item.underflow = int(self.vif.underflow.value)
            seq_item.data_out = int(self.vif.data_out.value)

            self.analysis_port.write(seq_item)

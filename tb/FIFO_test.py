from pyuvm import (
    uvm_test, uvm_factory, ConfigDB
)

from .FIFO_env import FIFOEnv
from .agent_config import set_agent_config
from .sequences.FIFO_reset_seq import FIFOResetSeq
from .sequences.FIFO_write_seq import FIFOWriteSeq
from .sequences.FIFO_read_seq import FIFOReadSeq
from .sequences.FIFO_random_seq import FIFORandomSeq


class FIFOTest(uvm_test):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.env = None
        self.agent_config = None
        self.reset_seq = None
        self.write_seq = None
        self.read_seq = None
        self.random_seq = None

    def build_phase(self):
        # Set agent config (no vif anymore)
        set_agent_config()
        self.agent_config = ConfigDB().get(self, "", "agent_config")

        # Register config with the agent
        ConfigDB().set(None, "*", "agent_config", self.agent_config)

        # Instantiate environment
        self.env = FIFOEnv("env", self)

        # Create sequences
        self.reset_seq = FIFOResetSeq("reset_seq")
        self.write_seq = FIFOWriteSeq("write_seq")
        self.read_seq = FIFOReadSeq("read_seq")
        self.random_seq = FIFORandomSeq("random_seq")

    def start_of_simulation_phase(self):
        self.print_obj()
        uvm_factory().print()

    async def run_phase(self):
        self.raise_objection()

        self.uvm_report_info("RUN_PHASE", "Reset sequence starting", 100)
        await self.reset_seq.start(self.env.agt.sequencer)
        self.uvm_report_info("RUN_PHASE", "Reset complete", 100)

        self.uvm_report_info("RUN_PHASE", "Write sequence starting", 100)
        await self.write_seq.start(self.env.agt.sequencer)
        self.uvm_report_info("RUN_PHASE", "Write complete", 100)

        self.uvm_report_info("RUN_PHASE", "Read sequence starting", 100)
        await self.read_seq.start(self.env.agt.sequencer)
        self.uvm_report_info("RUN_PHASE", "Read complete", 100)

        self.uvm_report_info("RUN_PHASE", "Random sequence starting", 100)
        await self.random_seq.start(self.env.agt.sequencer)
        self.uvm_report_info("RUN_PHASE", "Random sequence complete", 100)

        self.drop_objection()

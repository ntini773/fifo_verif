from pyuvm import (
    uvm_component, ConfigDB, uvm_analysis_port,
    uvm_sequencer, uvm_fatal
)
from tb.FIFO_driver import FIFODriver
from tb.FIFO_monitor import FIFOMonitor

class FifoAgent(uvm_component):

    def build_phase(self):
        # Fetch agent_config from ConfigDB
        self.config = ConfigDB().get(self, "", "agent_config")
        if self.config is None:
            uvm_fatal("AGENT_BUILD", "Missing 'agent_config' in ConfigDB")

        # Safety check for 'is_active' and 'vif'
        if "is_active" not in self.config:
            uvm_fatal("AGENT_BUILD", "'is_active' not found in agent_config")
        if "vif" not in self.config:
            uvm_fatal("AGENT_BUILD", "'vif' (virtual interface) not found in agent_config")

        # Instantiate components conditionally
        if self.config["is_active"]:
            self.sequencer = uvm_sequencer("sequencer", self)
            self.driver = FIFODriver("driver", self)
            # Connect vif to driver
            ConfigDB().set(self.driver, "", "vif", self.config["vif"])

        self.monitor = FIFOMonitor("monitor", self)
        ConfigDB().set(self.monitor, "", "vif", self.config["vif"])

        # Create analysis port for the monitor to export transactions
        self.agt_ap = uvm_analysis_port("agt_ap", self)

    def connect_phase(self):
        if self.config["is_active"]:
            self.driver.seq_item_port.connect(self.sequencer.seq_item_export)

        self.monitor.analysis_port.connect(self.agt_ap)


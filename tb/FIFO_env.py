# # fifo_env.py

# from pyuvm import *
# from .FIFO_agent import FifoAgent
# from .FIFO_scoreboard import FIFOScoreboard
# # from fifo_coverage import FifoCoverage  # Uncomment if using coverage

# class FIFOEnv(uvm_env):
#     def __init__(self, name, parent):
#         super().__init__(name, parent)
#         self.agt = None
#         self.sb = None
#         # self.cov = None  # Optional coverage

#     def build_phase(self):
#         self.agt = FifoAgent("agt", self)
#         self.sb = FIFOScoreboard("sb", self)
#         # self.cov = FifoCoverage("cov", self)

#     def connect_phase(self):
#         self.agt.agt_ap.connect(self.sb.sb_export)
#         # self.agt.agt_ap.connect(self.cov.cov_export)

from pyuvm import *
from .FIFO_agent import FifoAgent
from .FIFO_scoreboard import FIFOScoreboard

class FIFOEnv(uvm_env):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        # Instantiate the agent and scoreboard
        self.agt = FifoAgent("agt", self)
        self.sb = FIFOScoreboard("sb", self)

    def connect_phase(self):
        # Connect the agent's monitor analysis port to scoreboard's TLM FIFO
        # self.agt.monitor.analysis_port.connect(self.sb.out_fifo.put_export)
        self.agt.monitor.ap.connect(self.sb)  # ← this is correct



    def end_of_elaboration_phase(self):
        super().end_of_elaboration_phase()
        self.logger.info("Environment elaboration complete.")

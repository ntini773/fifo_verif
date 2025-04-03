from pyuvm import ConfigDB
import cocotb

def set_agent_config():
    # Virtual interface (vif) mock: a dict of signals
    vif = {
        "clk": cocotb.top.clk,
        "rst_n": cocotb.top.rst_n,
        "data_in": cocotb.top.data_in,
        "wr_en": cocotb.top.wr_en,
        "rd_en": cocotb.top.rd_en,
        "data_out": cocotb.top.data_out,
        "wr_ack": cocotb.top.wr_ack,
        "overflow": cocotb.top.overflow,
        "full": cocotb.top.full,
        "empty": cocotb.top.empty,
        "almostfull": cocotb.top.almostfull,
        "almostempty": cocotb.top.almostempty,
        "underflow": cocotb.top.underflow
    }

    # agent_config contains vif and status flags
    agent_config = {
        "vif": vif,
        "is_active": True
    }

    # Register in ConfigDB
    ConfigDB().set(None, "*", "agent_config", agent_config)
    return agent_config

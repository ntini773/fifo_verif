from pyuvm import *
from tb.FIFO_test import FIFOTest  # This assumes you've built the package as described

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer
from cocotb.triggers import RisingEdge


@cocotb.test()
async def fifo_uvm_test(dut):
    """Top-level cocotb test that launches the UVM testbench."""

    # Clock generation
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    # Interface hookup (virtual interface mapping)
    # In PyUVM, we simulate the idea of `uvm_config_db` like this:
    # We assume you pass the `dut` or parts of it manually to the config_db

    # Example: assuming your agent_config or monitor/driver needs the DUT directly
    ConfigDB().set(None, "", "DUT_IF", dut)

    # Start the UVM test
    await uvm_root().run_test("FIFOTest")

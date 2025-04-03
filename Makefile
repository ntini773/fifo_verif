# Language of the RTL (SystemVerilog is okay with Verilator >= 4.0)
TOPLEVEL_LANG = verilog

# Verilator as the simulator
SIM = verilator
VERILATOR = 1

# Top-level module name (must match your FIFO module)
TOPLEVEL = FIFO

# Name of the testbench module (Python file without `.py`)
MODULE = top

# RTL sources
VERILOG_SOURCES = $(shell pwd)/rtl/FIFO.sv

# Extra Verilator arguments (optional)
EXTRA_ARGS += -Wall -Wno-fatal

# Enable assertions if needed (optional)
COMPILE_ARGS += -DSIM

# Optional: specify Python version
PYTHON_BIN = python3

# Include cocotb's default makefile flow
include $(shell cocotb-config --makefiles)/Makefile.sim

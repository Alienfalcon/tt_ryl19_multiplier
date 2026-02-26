# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
import random
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    for i in range(0,1000):
        A = LogicArray('0000', Range(7, 'downto', 0))
        B = LogicArray('0000', Range(7, 'downto', 0))
        for j in range(0,4):
            A = int(random.random()>0.5) + A;
            B = int(random.random()>0.5) + B;
        u_in = A+B;
        A_int = int(A)
        B_int = int(B)
        P_int = A_int * B_int
        P = LogicArray('00000000', Range(7, 'downto', 0))
        P.value = P_int

        dut.ui_in.value = u_in;
        await ClockCycles(dut.clk, 2);
        assert 1;


    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.

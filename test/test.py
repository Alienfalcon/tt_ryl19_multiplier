# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
import random
import logging
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
    correct = 0
    # Set the input values you want to test
    for i in range(0,1000):
        A = cocotb.types.LogicArray.from_unsigned(0x00, 8)
        B = cocotb.types.LogicArray.from_unsigned(0x00, 8)
        
        for j in range(0,4):
            A = cocotb.types.LogicArray.from_unsigned((random.random()>0.5)<<(j+4),8) | A;
            B = cocotb.types.LogicArray.from_unsigned((random.random()>0.5)<<j,8) | B;
        u_in = A | B;
        dut._log.info("U_IN")
        dut._log.info(u_in)
        A_int = int(A) >> 4
        B_int = int(B)
        P_int = A_int * B_int
        P = cocotb.types.LogicArray.from_unsigned(0x00, 4)
        P.value = P_int
        
        dut.ui_in.value = u_in

        await ClockCycles(dut.clk, 2)
        correct = (P.value == dut.uo_out.value) + correct
        assert (P.value == dut.uo_out.value)

    fin_out_str = f"{correct} out of 1000 tests have succeeded"
    dut._log.info(fin_out_str)
    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.

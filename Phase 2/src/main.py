"""
The project is developed as part of Computer Architecture class.
Project Name: Functional Simulator for subset of RISC-V Processor

-------------------------------------------------
| Developer's Name   | Developer's Email ID     |
|-----------------------------------------------|
| Akhil Arya         | 2019csb1066@iitrpr.ac.in |
| Harshwardhan Kumar | 2019csb1089@iitrpr.ac.in |
| Krithika Goyal     | 2019csb1094@iitrpr.ac.in |
| Rhythm Jain        | 2019csb1111@iitrpr.ac.in |
| Tarun Singla       | 2019csb1126@iitrpr.ac.in |
-------------------------------------------------
"""

# main.py
# Purpose of this file: This file handles the input and output, and invokes the simulator.

from Gui import display, take_input
from myRISCVSim import run_RISCVsim, reset_proc, load_program_memory
import time

'''
if control_hazard returns true, it will add a predicted instruction to the pipeline_instructions
else it will return false
if forwarding is enabled data_hazard will change the state of instruction by specifying from where it will pick data in a stage where hazard is occuring
else will add a dummy instruction
x.evaluate() will evaluate the particular stage of the instruction, all the information
needed for evaluation will be stored in the state.
State() of an instruction will also store from where to pick the data for a particular
state, default will be buffer of previous stage of the instruction but can be changed due to,
data_hazard.
PC for a branch instruction, not present in BTB will be calculated in decode stage.
expected functions:
class: State(PC): will take PC as an input
                  ins = 0
                  function evaluate(), 
                  pc_update = False
                  branch_taken = False
                  pc_val = PC
                  data_decode = [instruction_number, buffer_number]
                  data_execute = [instruction_number, buffer_number] stores from where we will pick the data for
                                                                    the execution of a particular instruction.
data_hazard(pipeline_instructions, new_instruction, pc, forwarding_enabled), pass by reference
            if forwarding_enabled:
                check if new_instruction can be added or not
                if cannot be added:
                    then change the state of new_instruction to store, from where it will pick the data
                    add it to pipeline_instructions
                    update PC accordingly
            else:
                check if the new instruction can be added or not, else add a stall
                
            return was_there_hazard, new_pc
            
buffers = [5][5]
'''

if __name__ == '__main__':
    # set .mc file
    prog_mc_file = take_input()
    # reset the processor
    reset_proc()
    # load the program memory
    load_program_memory(prog_mc_file)
    # display the data
    # display()
    pipeline_instructions = []   # instructions currently in the pipeline
    terminate = False            # has the program terminated ?
    forwarding_enabled = False
    branch_taken = {}
    while not terminate:
        pipeline_instructions = [x.evaluate() for x in pipeline_instructions]
        for _ in pipeline_instructions: # check if the pc has been updated because of a conditional branch
            if _.pc_update and _.branch_taken != branch_taken[_.pc]: # if it is not equal to the branch we predicted.
                branch_taken.pop(_.pc)
                pipeline_instructions.pop() # flushing 1 time assuming branch decision is calculated during decode stage
                PC = _.pc_val   # updated PC
        if len(x) == 5:
            x = x[1:]   # removing the first instruction since it has been executed
        new_instruction = State(PC)
        new_pc = PC
        ctrl_hazard, new_pc = control_hazard(pipeline_instructions, new_instruction, PC)
        # data_hazard will work according to whether forwarding is enabled or not.
        data_hazard, new_pc = data_hazard(pipeline_instructions, new_instruction, forwarding_enabled, PC)
        if ctrl_hazard and new_pc != PC + 4:
            branch_taken[PC] = True
        elif ctrl_hazard:
            branch_taken[PC] = False
        PC = new_pc
        if not ctrl_hazard and not data_hazard:
            pipeline_instructions.append(State(PC)) # State(PC) will return an object of a class State()
            PC += 4
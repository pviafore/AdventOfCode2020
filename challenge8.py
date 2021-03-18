from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
import common.input_data as input_data

class InstructionType(Enum):
    ACC = "acc"
    JMP = "jmp"
    NOOP = "nop"

@dataclass
class Instruction:
    instruction_type: InstructionType
    value: int

def to_instruction(data: str) -> Instruction:
    type_lookup =  {
        "acc": InstructionType.ACC,
        "jmp": InstructionType.JMP,
        "nop": InstructionType.NOOP
    }
    itype, value = data.split()
    return Instruction(type_lookup[itype], int(value))

class Computer:

    def __init__(self, instructions: list[Instruction]):
        self.instructions = instructions
        self.accumulator = 0
        self.instruction_pointer = 0

    # the bool is true if we stopped due to infinite loop
    # false if program ended normally
    def get_accumulator_after_stop(self) -> tuple[bool, int]:
        instructions_seen: set[int] = set()
        while (self.instruction_pointer not in instructions_seen and
               self.instruction_pointer < len(self.instructions)):
            instructions_seen.add(self.instruction_pointer)
            self.do_operation(self.instructions[self.instruction_pointer])
        return self.instruction_pointer in instructions_seen, self.accumulator

    def do_operation(self, instruction: Instruction):
        if instruction.instruction_type == InstructionType.ACC:
            self.accumulator += instruction.value
        if instruction.instruction_type == InstructionType.JMP:
            self.instruction_pointer += instruction.value
            return # early return for jump

        # for acc/noop, update instruction pointer to next instruction
        self.instruction_pointer +=1


def get_accumulator_after_fixing_program(instructions: list[Instruction]) -> int:
    for index in range(len(instructions)):
        copied_instructions = deepcopy(instructions)
        if copied_instructions[index].instruction_type == InstructionType.NOOP:
            copied_instructions[index].instruction_type = InstructionType.JMP
        if copied_instructions[index].instruction_type == InstructionType.JMP:
            copied_instructions[index].instruction_type = InstructionType.NOOP
        test_computer = Computer(copied_instructions)
        is_infinite_loop, accum = test_computer.get_accumulator_after_stop()
        if not is_infinite_loop:
            return accum

    raise RuntimeError("No solution found, this is bad")

INSTRUCTIONS = input_data.read("input/input8.txt", to_instruction)

if __name__ == "__main__":
    computer = Computer(INSTRUCTIONS)
    print("Accumulator on first repeated instruction: "
          f"{computer.get_accumulator_after_stop()[1]}")

    print(f"Fixed program's accumulator {get_accumulator_after_fixing_program(INSTRUCTIONS)}")

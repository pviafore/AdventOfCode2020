import re

from collections import defaultdict
from dataclasses import dataclass
from typing import Optional, Union

import common.input_data as input_data

@dataclass
class MaskInstruction:
    value: str

@dataclass
class MemorySetInstruction:
    address: int
    value: int

Instruction = Union[MaskInstruction, MemorySetInstruction]

def to_instruction(data: str) -> Instruction:
    if data.startswith("mask"):
        return MaskInstruction(data.split(" ")[-1])

    address,value = re.split(r"(?:mem\[|\] = )", data)[1:]
    return MemorySetInstruction(int(address), int(value))

def get_sum_of_memory(instructions: list[Instruction]) -> int:
    mask_value = "X"*36
    memory = defaultdict(lambda: "0"*36)
    for instruction in instructions:
        if isinstance(instruction, MaskInstruction):
            mask_value = instruction.value
        else:
            bitstring = bin(instruction.value)[2:].zfill(36)
            bits = [(bit if mask == 'X' else mask) for bit, mask in zip(bitstring, mask_value)]
            memory[instruction.address] = "".join(bits)
    return sum(int(bits, 2) for bits in memory.values())

def build_address_masks(mask: list[str], accum: Optional[list[str]] = None) -> list[str]:
    if accum is None:
        accum = []
    if mask == []:
        return accum
    letter, *mask = mask
    if letter == "X":
        if not accum:
            accum = ["0", "1"]
        else:
            accum = [m + "0" for m in accum] + [m + "1" for m in accum]
    else:
        if not accum:
            accum = [letter]
        else:
            accum = [m + letter for m in accum]
    return build_address_masks(mask, accum)

def get_sum_of_memory_v2(instructions: list[Instruction]) -> int:
    mask_value = "X" * 36
    memory: dict[str, int] = defaultdict(lambda:0)
    for instruction in instructions:

        if isinstance(instruction, MaskInstruction):
            mask_value = instruction.value
        else:
            bitstring = bin(instruction.address)[2:].zfill(36)
            bits = [(bit if mask == '0' else mask) for bit, mask in zip(bitstring, mask_value)]
            mask_values = build_address_masks(bits)
            for address in mask_values:
                memory[address] = instruction.value
    return sum(memory.values())


INSTRUCTIONS = input_data.read("input/input14.txt", to_instruction)

if __name__ == "__main__":
    print(f"Sum of memory: {get_sum_of_memory(INSTRUCTIONS)}")

    print(f"Sum of memory v2: {get_sum_of_memory_v2(INSTRUCTIONS)}")

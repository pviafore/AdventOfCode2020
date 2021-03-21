import itertools
import operator
from functools import reduce

import common.input_data as input_data

def get_first_bus_after_timestamp(timestamp: str, bus_ids: str) -> int:
    busses = [int(bus) for bus in bus_ids.split(",") if bus != 'x']
    for num in itertools.count(int(timestamp)):
        for bus in busses:
            if num % bus == 0:
                return bus * (num - int(timestamp))

    raise RuntimeError("Should not reach this code")

# from Cormen's Introduction to Algorithms
def extended_euclid(a: int, b: int)-> tuple[int, int, int]: # disable=C0103
    if b == 0:
        return (a, 1, 0)

    d, x_prime, y_prime = extended_euclid(b, a % b) # disable=C0103
    return d, y_prime, x_prime - (a // b)* y_prime

def inverse_mod(a: int, n: int) -> int: # disable=C0103
    _d,x,_y = extended_euclid(a, n) # disable=C0103
    return x

def find_timestamp_for_consecutive_busses(bus_ids: str) -> int:
    busses = [(index, int(bus)) for index, bus in enumerate(bus_ids.split(",")) if bus != 'x']
    modulus = reduce(operator.mul, [bus for index, bus in busses])
    value = sum((bus - index) * modulus//bus *  inverse_mod(modulus//bus, bus)
                for index, bus in busses)
    return value % modulus


BUS_DATA: list[str] =  input_data.read("input/input13.txt")
TIMESTAMP, BUS_IDS = BUS_DATA

if __name__ == "__main__":
    print(f"First bus: {get_first_bus_after_timestamp(TIMESTAMP, BUS_IDS)}")

    print("Timestamp with consecutive busses: "
          f"{find_timestamp_for_consecutive_busses(BUS_IDS)}")

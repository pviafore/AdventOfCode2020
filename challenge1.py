import itertools
import operator
from functools import reduce

import common.input_data as input_data
def get_entries_summing_to(entries: list[int], target: int,
                           number_of_entries: int = 2) -> tuple[int, ...]:
    return next(values for values
                in itertools.combinations(entries, number_of_entries)
                if reduce(operator.add, values) == target)

ENTRIES = input_data.read_ints("input/input1.txt")
if __name__ == "__main__":
    value1, value2 = get_entries_summing_to(ENTRIES, 2020)
    print(f"The two values {value1} and {value2} multiplied together are {value1*value2}")

    value1, value2, value3 = get_entries_summing_to(ENTRIES, 2020, 3)
    print(f"The two values {value1}, {value2} and {value3} "
          f"multiplied together are {value1*value2*value3}")

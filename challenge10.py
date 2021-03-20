from collections import defaultdict

import common.input_data as input_data

def get_joltage_product(adapters: list[int]) -> int:
    sorted_adapters = [max(adapters) + 3] + sorted(adapters, reverse=True) + [0]
    differences = [n1 - n2 for n1,n2 in zip(sorted_adapters[:-1], sorted_adapters[1:])]

    return differences.count(1) * differences.count(3)

def find_all_ways_to_arrange_adapters(adapters: list[int]) -> int:
    # recurrence relation Number of Combinations C(N)  = C(N-1)+ C(N-2)+ C(N-3)
    # if N is not an adapter, then C(N) = 0
    # dynamic programming, there are overlapping recurrences, so we can do this building
    # up a table linearly
    lookup_table = defaultdict(lambda: 0, {0: 1})
    max_joltage = max(adapters) + 3
    for num in range(1, max_joltage + 1):
        lookup_table[num] = (0 if num not in adapters + [max_joltage] else
                                (lookup_table[num - 1] +
                                 lookup_table[num - 2] +
                                 lookup_table[num - 3]))
    return lookup_table[max_joltage]

ADAPTERS = input_data.read("input/input10.txt", int)

if __name__ == "__main__":
    print(f"Total Jolt difference product: {get_joltage_product(ADAPTERS)}")
    print(f"Total combinations: {find_all_ways_to_arrange_adapters(ADAPTERS)}")

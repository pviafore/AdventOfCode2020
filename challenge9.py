from collections import Counter
import common.input_data as input_data
Sums = dict[int, Counter[int]]
def find_first_wrong_number(numbers: list[int]) -> int:
    sums = make_sums(numbers[:25])
    numbers_to_check = list(numbers)
    while numbers_to_check:
        new_number = numbers_to_check[25]
        if not is_valid_number(new_number, sums):
            return new_number
        number = numbers_to_check.pop(0)
        remove_from_sums(number, sums)
        add_to_sums(new_number, sums)

    raise RuntimeError("Should not reach here, no number was detected as valid")

def is_valid_number(number: int, sums: Sums) -> bool:
    return any(sum_counter[number] != 0 for sum_counter in sums.values())

def remove_from_sums(number: int, sums: Sums):
    del sums[number]
    for number2, sum_counter in sums.items():
        sum_counter[number + number2] -= 1

def add_to_sums(number: int, sums: Sums):
    new_sums = Counter(number + number2 for number2 in sums)
    for number2, sum_counter in sums.items():
        sum_counter[number + number2] += 1
    sums[number] = new_sums

def make_sums(numbers: list[int]) -> Sums:
    sums: Sums = {}
    for index1, number in enumerate(numbers):
        sums[number] = Counter(number + num2
                               for index2, num2 in enumerate(numbers)
                               if index1 != index2)
    return sums

def find_encryption_weakness(numbers: list[int]) -> int:
    invalid_number = find_first_wrong_number(numbers)
    candidate_range: list[int] = []
    numbers_to_check = list(numbers)
    while numbers_to_check:
        sum_value = sum(candidate_range)
        if sum_value == invalid_number and len(candidate_range) > 1:
            return min(candidate_range) + max(candidate_range)
        if sum_value < invalid_number:
            candidate_range.append(numbers_to_check.pop(0))
        if sum_value > invalid_number:
            candidate_range.pop(0)

    raise RuntimeError("Cannot find an encryption weakness")


NUMBERS = input_data.read("input/input9.txt", int)

if __name__ == "__main__":
    print(f"First number that's wrong: {find_first_wrong_number(NUMBERS)}")

    print(f"Encryption Weakness: {find_encryption_weakness(NUMBERS)}")


PREAMBLE=[1,12,0,20,8,16]

def get_nth_word_spoken(preamble: list[int], target: int) -> int:
    lookup = {val: pos for pos, val in enumerate(preamble[:-1])}
    last_number = preamble[-1]
    # start at the last number
    for num in range(len(preamble)-1, target-1):
        last_numbers_position = lookup.get(last_number, num)
        lookup[last_number] = num
        last_number = num - last_numbers_position
    return last_number

print(get_nth_word_spoken(PREAMBLE, 2020))
print(get_nth_word_spoken(PREAMBLE, 30000000))

import common.input_data as input_data

def to_seat_id(boarding_pass: str) -> int:
    # convert to binary and then cast to int
    row = int(boarding_pass[:7].replace('F', '0').replace('B', '1'), 2)
    column = int(boarding_pass[7:].replace('L', '0').replace('R', '1'), 2)

    return row*8 + column

def get_highest_seat_id(boarding_passes: list[str]) -> int:
    return max(to_seat_id(bp) for bp in boarding_passes)

def find_seat_id(boarding_passes: list[str]) -> int:
    seat_ids = {to_seat_id(bp) for bp in boarding_passes}
    # 10 bit number: 1024 entries to check
    return next(seat for seat in range(1024) if is_correct_seat(seat, seat_ids))

def is_correct_seat(seat: int, seat_ids: set[int]) -> bool:
    return (seat not in seat_ids and
            seat + 1 in seat_ids and
            seat - 1 in seat_ids)

BOARDING_PASSES: list[str] = input_data.read("input/input5.txt")

if __name__ == "__main__":
    print(f"Highest seat id: {get_highest_seat_id(BOARDING_PASSES)}")
    print(f"Your seat is: {find_seat_id(BOARDING_PASSES)}")

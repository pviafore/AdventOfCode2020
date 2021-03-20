import itertools
from collections.abc import MutableMapping
from copy import deepcopy
from dataclasses import dataclass
from typing import Iterator

import common.input_data as input_data

@dataclass(frozen=True, order=True)
class Position:
    xpos: int
    ypos: int

class Grid(MutableMapping):

    def __init__(self, data: list[str]):
        self.data: dict[Position, str] = {}
        for row_index, row in enumerate(data):
            for column_index, value in enumerate(row):
                self.data[Position(row_index, column_index)] = value

    def get_neighbors(self, index: Position) -> list[str]:
        offsets = [-1, 0, 1]

        # don't count yourself at offset 0,0
        return [self.data.get(Position(index.xpos+x, index.ypos+y), '.')
                for x,y in itertools.product(offsets, offsets) if (x != 0 or y != 0)]

    def get_first_character_in_line_of_sight(self, index: Position, offset: tuple[int, int],
                                             to_ignore: str = "") -> str:
        new_index = Position(index.xpos + offset[0], index.ypos + offset[1])
        while new_index in self.data and self.data[new_index] in to_ignore:
            new_index = Position(new_index.xpos + offset[0], new_index.ypos + offset[1])

        return self.data.get(new_index, ".")


    def count(self, character: str) -> int:
        return list(self.data.values()).count(character)

    def __getitem__(self, key: Position) -> str:
        return self.data[key]

    def __setitem__(self, key:Position, value: str):
        self.data[key] = value

    def __delitem__(self, key:Position):
        del self.data[key]

    def __iter__(self) -> Iterator:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __eq__(self, rhs) -> bool:
        if not isinstance(rhs, Grid):
            return NotImplemented
        return self.data == rhs.data

    def __str__(self) -> str:
        data = itertools.groupby(sorted(self.data.items()), lambda item: item[0].xpos)
        text: list[str] = []
        for _, rows in data:
            text.append("".join(row[1] for row in rows))
        return "\n".join(text)

def get_final_seats_occupied(seats: list[str]) -> int:
    old_grid = Grid(seats)
    while (new_grid:= transform(old_grid)) != old_grid:
        old_grid = new_grid
    return new_grid.count('#')

def transform(old_grid: Grid) -> Grid:
    new_grid = deepcopy(old_grid)
    for index, seat in old_grid.items():
        if seat == ".":
            continue
        open_seats = old_grid.get_neighbors(index).count('#')
        if seat == "L" and open_seats == 0:
            new_grid[index] = "#"
        if seat == "#" and open_seats >= 4:
            new_grid[index] = "L"

    return new_grid

def get_final_seats_occupied_based_on_sight(seats: list[str]) -> int:
    old_grid = Grid(seats)
    while (new_grid:= transform_based_on_los(old_grid)) != old_grid:
        old_grid = new_grid
    return new_grid.count('#')

def transform_based_on_los(old_grid: Grid) -> Grid:
    new_grid = deepcopy(old_grid)
    for index, seat in old_grid.items():
        if seat == ".":
            continue
        offsets = [-1, 0, 1]
        seats = [old_grid.get_first_character_in_line_of_sight(index, (x,y), ".")
                      for x,y in itertools.product(offsets, offsets) if x != 0 or y != 0]
        open_seats = seats.count('#')
        if seat == "L" and open_seats == 0:
            new_grid[index] = "#"
        if seat == "#" and open_seats >= 5:
            new_grid[index] = "L"
    return new_grid



SEATS: list[str] = input_data.read("input/input11.txt")

if __name__ == "__main__":
    print(f"Final seats occupied: {get_final_seats_occupied(SEATS)}")
    print(f"Final seats occupied: {get_final_seats_occupied_based_on_sight(SEATS)}")

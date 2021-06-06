import itertools
from dataclasses import dataclass

from typing import Union

@dataclass(frozen=True)
class Point:
    xpos: int
    ypos: int
    zpos: int

    def __add__(self, rhs: 'Point') -> 'Point':
        return Point(self.xpos + rhs.xpos, self.ypos + rhs.ypos, self.zpos + rhs.zpos)

    def get_neighbors(self) -> list['Point']:
        OFFSET = [-1, 0, 1]
        return [self + Point(x,y,z) for x,y,z in itertools.product(OFFSET, OFFSET, OFFSET)
                if x != 0 or y != 0 or z != 0]

@dataclass(frozen=True)
class Point4D:
    xpos: int = 0
    ypos: int = 0
    zpos: int = 0
    wpos: int = 0

    def __add__(self, rhs: 'Point4D') -> 'Point4D':
        return Point4D(self.xpos + rhs.xpos, self.ypos + rhs.ypos,
                       self.zpos + rhs.zpos, self.wpos + rhs.wpos)

    def get_neighbors(self) -> list['Point4D']:
        OFFSET = [-1, 0, 1]
        return [self + Point4D(x,y,z,w)
                for x,y,z,w in itertools.product(OFFSET, OFFSET, OFFSET, OFFSET)
                if x != 0 or y != 0 or z != 0 or w != 0]
PointType = Union[Point, Point4D]
class Grid():
    def __init__(self, initial_data: list[str], point_type: type):
        self.grid: dict[PointType, str] = {}
        self.active_points: list[PointType] = []
        for y_pos, line in enumerate(initial_data):
            for x_pos, char in enumerate(line):
                self.grid[point_type(x_pos, y_pos, 0)] = char
                if char == '#':
                    self.active_points.append(point_type(x_pos, y_pos, 0))

    def transform(self):
        points_to_check = set(itertools.chain.from_iterable(
            point.get_neighbors() for point in self.active_points
        ))
        new_grid = dict(self.grid)
        for point in points_to_check:
            neighbors = point.get_neighbors()
            nearby_active_states = [self.grid.get(n, '.') for n in neighbors].count('#')
            char = self.grid.get(point, '.')
            if ((char == '#' and nearby_active_states in (2,3)) or
                (char == '.' and nearby_active_states == 3)):
                new_grid[point] = '#'
                self.active_points.append(point)
            else:
                new_grid[point] = '.'
        self.grid = new_grid

    def get_number_of_active_states(self):
        return list(self.grid.values()).count('#')


def get_active_squares_after_n_cycles(data: list[str], num: int,
                                      point_type: type = Point) -> int:
    grid = Grid(data, point_type)
    for _ in range(num):
        grid.transform()
    return grid.get_number_of_active_states()

with open("input/input17.txt") as input_file:
    STARTING_DATA = input_file.read().strip().split("\n")

if __name__ == "__main__":
    print(get_active_squares_after_n_cycles(STARTING_DATA, 6))
    print(get_active_squares_after_n_cycles(STARTING_DATA, 6, Point4D))

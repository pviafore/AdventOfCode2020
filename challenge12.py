from enum import Enum
from dataclasses import dataclass

from typing import Union

import common.input_data as input_data

class Direction(Enum):
    NORTH = (0,1)
    EAST = (1, 0)
    SOUTH = (0, -1)
    WEST = (-1, 0)

class Turn(Enum):
    LEFT = -1
    RIGHT = 1

@dataclass
class Forward:
    pass

MoveType = Union[Direction, Turn, Forward]

def turn_ship(heading: Direction, turn: Turn, degrees: int) -> Direction:
    headings = list(Direction)
    offset = degrees // 90 * turn.value
    return headings[(headings.index(heading) + offset) % 4]

@dataclass
class Move:
    move_type: MoveType
    amount: int

def to_move(data: str) -> Move:
    move_letter = data[0]
    value = data[1:]
    move_type_lookup: dict[str, MoveType] = {
        "N": Direction.NORTH,
        "E": Direction.EAST,
        "W": Direction.WEST,
        "S": Direction.SOUTH,
        "F": Forward(),
        "L": Turn.LEFT,
        "R": Turn.RIGHT
    }
    return Move(move_type_lookup[move_letter], int(value))

@dataclass
class Position:
    xpos: int
    ypos: int

@dataclass
class Ship:
    heading: Direction
    position: Position

def get_manhattan_distance_after_travelling(moves: list[Move]):
    ship = Ship(Direction.EAST, Position(0,0))
    for move in moves:
        if isinstance(move.move_type, Direction):
            ship.position.xpos += move.amount * move.move_type.value[0]
            ship.position.ypos += move.amount * move.move_type.value[1]
        if isinstance(move.move_type, Turn):
            ship.heading = turn_ship(ship.heading, move.move_type, move.amount)
        if isinstance(move.move_type, Forward):
            ship.position.xpos += move.amount * ship.heading.value[0]
            ship.position.ypos += move.amount * ship.heading.value[1]
    return abs(ship.position.xpos) + abs(ship.position.ypos)

def get_manhattan_distance_after_waypoint_moves(moves: list[Move]) -> int:
    waypoint = Position(10, 1)
    ship = Ship(Direction.EAST, Position(0,0))
    for move in moves:
        if isinstance(move.move_type, Direction):
            waypoint.xpos += move.amount * move.move_type.value[0]
            waypoint.ypos += move.amount * move.move_type.value[1]
        if isinstance(move.move_type, Turn):
            offset = move.amount // 90
            for _ in range(offset):
                if move.move_type == Turn.RIGHT:
                    waypoint = Position(waypoint.ypos, waypoint.xpos * -1)
                if move.move_type == Turn.LEFT:
                    waypoint = Position(waypoint.ypos * -1, waypoint.xpos)
        if isinstance(move.move_type, Forward):
            ship.position.xpos += move.amount * waypoint.xpos
            ship.position.ypos += move.amount * waypoint.ypos

    return abs(ship.position.xpos) + abs(ship.position.ypos)

MOVES = input_data.read("input/input12.txt", to_move)

if __name__ == "__main__":
    print(f"Manhattan Distance of ship: {get_manhattan_distance_after_travelling(MOVES)}")

    print("Manhattan Distance of ship w/ waypoint: "
          f"{get_manhattan_distance_after_waypoint_moves(MOVES)}")

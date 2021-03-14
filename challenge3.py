import itertools
import operator
from functools import reduce
from typing import Iterable
from common.input_data import read


def make_infinite(trees: list[str]) -> list[Iterable[str]]:
    return [itertools.cycle(t) for t in trees]

def get_number_of_trees_hit(tree_grid: list[str],
                            slope_x: int, slope_y: int=1):
    trees = make_infinite(tree_grid)
    # this is a vertical slice of trees that we can iterate over
    tree_lines = iter(zip(*trees))
    # ignore the first column
    next(tree_lines)
    number_of_trees_hit = 0

    # the idea is to advance "slope" times to the right
    # every time we move down one. We can advance to the right
    # infinitely
    for index in range(slope_y, len(TREE_GRID), slope_y):
        for _ in range(slope_x):
            tree = next(tree_lines)
        if tree[index] == "#":
            number_of_trees_hit += 1
    return number_of_trees_hit

def get_all_slopes_result(tree_grid: list[str]):
    slopes = ((1,1), (3,1), (5, 1), (7, 1), (1,2))
    return reduce(operator.mul,
                  (get_number_of_trees_hit(tree_grid, x,y) for x,y in slopes))

TREE_GRID: list[str] = read("input/input3.txt")

if __name__ == "__main__":
    print("Number of trees hit with (3,1) slope: "
          f"{get_number_of_trees_hit(TREE_GRID, 3)}")

    print(f"Result of checking all slopes: {get_all_slopes_result(TREE_GRID)}")

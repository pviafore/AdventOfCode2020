from collections import Counter
from functools import reduce
from typing import Generator, Iterable
import common.input_data as input_data

Tile = tuple[float, float]

DIRECTIONS = {
    'e': (0, 1),
    'w': (0, -1),
    'ne': (.5, .5),
    'nw': (.5, -.5),
    'se': (-.5, .5),
    'sw': (-.5, -.5),
}

def add_tile(tile1: Tile, tile2: Tile) -> Tile:
    return (tile1[0] + tile2[0], tile1[1] + tile2[1])

def to_ending_tile(tiles: str) -> Tile:
    tile_directions = to_directions(tiles)
    return reduce(add_tile, tile_directions)

def to_directions(tiles: str) -> Generator[Tile, None, None]:
    tile_iter = iter(tiles)
    try:
        while char := next(tile_iter):
            if char in 'we':
                yield DIRECTIONS[char]
            else:
                next_char = next(tile_iter)
                yield DIRECTIONS[char + next_char]
    except StopIteration:
        pass

def get_flipped_tiles(tiles: list[Tile]) -> int:
    counter = Counter(tiles)
    return len([t for t in counter.values() if t % 2 == 1])

def get_final_number_of_flipped_tiles(tiles: list[Tile]) -> int:
    counter = Counter(tiles)
    colors =  {t: 'black' if flips % 2 == 1 else 'white' for t, flips in counter.items()}
    outskirts = get_all_outskirts(colors.keys())
    for _ in range(100):
        colors, outskirts = flip_colors(colors, outskirts)
    return len([color for color in colors.values() if color == 'black'])

def flip_colors(colors: dict[Tile, str], outskirts: Iterable[Tile]) -> tuple[dict[Tile, str],
                                                                             set[Tile]]:
    tiles = list(colors.keys()) + list(outskirts)
    new_dict: dict[Tile, str] = {}
    for tile in tiles:
        number_of_black_neighbors = len([n for n in get_neighbors(tile)
                                         if colors.get(n, 'white') == 'black'])
        tile_color = colors.get(tile, 'white')
        if tile_color == 'white' and number_of_black_neighbors == 2:
            new_dict[tile] = 'black'
        elif tile_color == 'black' and number_of_black_neighbors not in [1, 2]:
            new_dict[tile] = 'white'
        else:
            new_dict[tile] = tile_color

    # figure out next round of outskirts
    new_outskirts = get_all_outskirts(outskirts)
    new_outskirts -= set(new_dict.keys())
    return new_dict, new_outskirts

def get_neighbors(tile: Tile) -> list[Tile]:
    return [add_tile(tile, t) for t in DIRECTIONS.values()]

def get_all_outskirts(tiles: Iterable[Tile]) -> set[Tile]:
    new_outskirts: set[Tile] = set()
    for tile in tiles:
        new_outskirts.update(get_neighbors(tile))
    return new_outskirts


TILES = input_data.read("input/input24.txt", to_ending_tile)

if __name__ == "__main__":
    print(get_flipped_tiles(TILES))
    print(get_final_number_of_flipped_tiles(TILES))

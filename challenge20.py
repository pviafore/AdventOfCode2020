import math
import operator
from dataclasses import dataclass
from functools import reduce

Tiles = list['Tile']

@dataclass(frozen=True)
class Tile:
    id: int
    data: list[str]

    def get_permutations(self) -> list['Tile']:
        flipped_tile = self.flip_around_horizontal_axis()
        # can only be 8 ways of flipping/rotating to something unique
        return self.get_rotations() +  flipped_tile.get_rotations()

    def get_rotations(self) -> list['Tile']:
        def rotate(tile: 'Tile') -> 'Tile':
            # transpose and horizontal flip
            return Tile(self.id, [''.join(d)[::-1] for d in zip(*tile.data)])

        t1 = rotate(self)
        t2 = rotate(t1)
        t3 = rotate(t2)

        return [self, t1, t2, t3]

    def flip_around_horizontal_axis(self) -> 'Tile':
        return Tile(self.id, self.data[::-1])

    def get_top_side(self) -> str:
        return self.data[0]

    def get_bottom_side(self) -> str:
        return self.data[-1]

    def get_left_side(self) -> str:
        return ''.join([d[0] for d in self.data])

    def get_right_side(self) -> str:
        return ''.join([d[-1] for d in self.data])

    def strip_borders(self) -> 'Tile':
        return Tile(self.id, [d[1:-1] for d in self.data[1:-1]])

    def get_lines(self) -> list[str]:
        return list(self.data)

    def count(self, text: str) -> int:
        return sum([line.count(text) for line in self.data])

    def get_number_of_sea_monsters(self):
        count = 0
        for row, line in enumerate(self.data[:-2]):
            indices = [index for index, element in enumerate(line)
                       if element == '#' and 18 <= index < len(line) - 1]
            for index in indices:
                if all(char == '#' for char in (self.data[row + 1][index - 18],
                                                self.data[row + 1][index - 13],
                                                self.data[row + 1][index - 12],
                                                self.data[row + 1][index - 7],
                                                self.data[row + 1][index - 6],
                                                self.data[row + 1][index - 1],
                                                self.data[row + 1][index],
                                                self.data[row + 1][index + 1],
                                                self.data[row + 2][index - 17],
                                                self.data[row + 2][index - 14],
                                                self.data[row + 2][index - 11],
                                                self.data[row + 2][index - 8],
                                                self.data[row + 2][index - 5],
                                                self.data[row + 2][index - 2],
                                               )):
                    count += 1
        return count

def to_tile(text: list[str]) -> Tile:
    return Tile(int(text[0].split(' ')[1].strip(':')), text[1:])


def read_tiles() -> Tiles:
    with open("input/input20.txt") as input_file:
        tile_data = input_file.read().split('\n\n')
    return [to_tile(tile.strip('\n').split('\n')) for tile in tile_data if tile]

def get_corners_multiplied(tiles: Tiles) -> int:
    square_side = int(math.sqrt(len(tiles)))
    return (tiles[0].id * tiles[square_side - 1].id *
            tiles[square_side*(square_side - 1)].id *
            tiles[square_side*square_side-1].id)

def get_rearranged(tiles: Tiles) -> Tiles:
    # branch and prune constraint satisfaction problem
    tile_options: list[tuple[Tiles, Tiles]] = [([], list(tiles))]
    while tile_options:
        candidate, remaining = tile_options.pop(-1)
        if len(candidate) == len(tiles):
            # we have a valid solution
            return candidate
        for tile in remaining:
            permutations = tile.get_permutations()
            for permutation in permutations:
                if is_valid_placement(int(math.sqrt(len(tiles))), candidate, permutation):
                    tile_options.append((candidate + [permutation],
                                         [t for t in remaining
                                          if t.id != permutation.id]))

    assert False, "No Valid Solution"

def is_valid_placement(side_length: int, tiles: Tiles, permutation: Tile) -> bool:
    position = len(tiles)
    left_tile_valid = (position % side_length == 0 or
                       tiles[position - 1].get_right_side() == permutation.get_left_side())
    top_tile_valid = (position < side_length or
                      tiles[position - side_length].get_bottom_side() == permutation.get_top_side())
    return left_tile_valid and top_tile_valid

def compose_into_picture(tiles: Tiles) -> Tile:
    stripped = [t.strip_borders() for t in tiles]
    side_length = int(math.sqrt(len(tiles)))
    grouped = [stripped[n*side_length:(n+1)*side_length] for n in range(side_length)]
    return Tile(0, list(reduce(operator.add, [stitch(group) for group in grouped])))

def stitch(tiles: Tiles) -> list[str]:
    text = zip(*[tile.get_lines() for tile in tiles])
    return [reduce(operator.add, lines) for lines in text]

def get_non_sea_monsters(tiles: Tiles) -> int:
    picture = compose_into_picture(tiles)
    for permutation in picture.get_permutations():
        number_of_sea_monsters = permutation.get_number_of_sea_monsters()
        if number_of_sea_monsters != 0:
            return permutation.count('#') - number_of_sea_monsters * 15

    raise RuntimeError("Could not find sea monsters")

ASSEMBLED_TILES = get_rearranged(read_tiles())

if __name__ == "__main__":
    print(get_corners_multiplied(ASSEMBLED_TILES))
    print(get_non_sea_monsters(ASSEMBLED_TILES))

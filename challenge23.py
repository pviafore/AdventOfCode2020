from dataclasses import dataclass

# this runs a long time (due to a linked list rather than contiguous memory)
# use a linked list and cache into the list to track all operations
@dataclass
class Cup:
    label: str
    next: 'Cup'

    def remove_next_three(self) -> 'Cup':
        cups = self.next
        self.next = cups.next.next.next # skip ahead
        return cups

    def add_next_three(self, three_cups):
        three_cups.next.next.next = self.next
        self.next = three_cups

    def is_id_in_next_three(self, label: str):
        return label in (self.label, self.next.label, self.next.next.label)

    def get_n_next_cups(self, n: int) -> list['Cup']:
        cup = self
        output_list = []
        for _ in range(n):
            output_list.append(cup.next)
            cup = cup.next
        return output_list

class Arrangement:

    def __init__(self, arrangement: tuple[str, ...]):
        self.cache: dict[str, Cup] = {}
        self.first_cup: Cup = None # type: ignore
        self._fill_out_arrangement(arrangement)

        self.highest = max([int(l) for l in self.cache])
        self.lowest = min([int(l) for l in self.cache])

    def _fill_out_arrangement(self, arrangement: tuple[str, ...]):
        cup = self.first_cup
        for label in arrangement:
            if self.first_cup is None:
                self.first_cup = Cup(label, self.first_cup)
                new_cup = self.first_cup
            else:
                new_cup = Cup(label, self.first_cup)
                cup.next = new_cup
            self.cache[label] = new_cup
            cup = new_cup

    def run_rounds(self, loops: int):
        for _ in range(loops):
            removed = self.first_cup.remove_next_three()
            destination = int(self.first_cup.label) - 1
            while removed.is_id_in_next_three(str(destination)):
                destination -= 1
            if destination < self.lowest:
                destination = self.highest
            while removed.is_id_in_next_three(str(destination)):
                destination -= 1
            self.cache[str(destination)].add_next_three(removed)
            self.first_cup = self.first_cup.next

    def get_cup(self, destination: str) -> Cup:
        return self.cache[destination]


ARRANGEMENT = tuple('916438275')
BIG_ARRANGEMENT = ARRANGEMENT + tuple(str(s) for s in range(10, 1_000_001))

def get_labels_after_1(arrangement_strs: tuple[str, ...], loops: int) -> str:
    arrangement = Arrangement(arrangement_strs)
    arrangement.run_rounds(loops)
    cups = [c.label for c in arrangement.get_cup("1").get_n_next_cups(8)]
    return ''.join(cups)

def get_product_of_next_two_labels(arrangement_strs: tuple[str, ...], loops: int) -> int:
    arrangement = Arrangement(arrangement_strs)
    arrangement.run_rounds(loops)
    label1, label2 = [c.label for c in arrangement.cache["1"].get_n_next_cups(2)]
    return int(label1) * int(label2)


if __name__ == "__main__":
    print(get_labels_after_1(ARRANGEMENT, 100))
    print(get_product_of_next_two_labels(BIG_ARRANGEMENT, 10_000_000))

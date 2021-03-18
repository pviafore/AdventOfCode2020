import functools
import re

from dataclasses import dataclass

import common.input_data as input_data
ContainedBag = tuple[int, str]
@dataclass(frozen=True)
class BagRule:
    color: str
    contains: tuple[ContainedBag, ...]

def get_number_of_bags_able_to_hold_bag(bag_rules: tuple[BagRule, ...], color: str) -> int:
    return len([bag_rule for bag_rule in bag_rules
               if can_hold(bag_rule, color, bag_rules)])

@functools.cache
def get_number_of_bags_inside(bag_rules: tuple[BagRule, ...], color: str) -> int:
    bag = find_rule(bag_rules, color)
    return sum([num + num * get_number_of_bags_inside(bag_rules, color)
                for num, color in bag.contains])

@functools.cache
def can_hold(bag_rule: BagRule, bag: str, rules: tuple[BagRule, ...]) -> bool:
    if any(color == bag for _, color in bag_rule.contains):
        return True
    return any(can_hold(find_rule(rules, color), bag, rules) for _, color in bag_rule.contains)

def find_rule(rules: tuple[BagRule, ...], color: str) -> BagRule:
    return next(r for r in rules if r.color == color)

def to_bag_rules(data: str) -> BagRule:
    color, *contains = re.split(r"(?: bags contain | bags, | bags.| bag, | bag.)", data)
    return BagRule(color, parse_containing(contains))

def parse_containing(contains: list[str]) -> tuple[ContainedBag, ...]:
    if contains[0] == "no other":
        return tuple()
    return tuple(to_contained_bag(bag) for bag in contains if bag)

def to_contained_bag(contains: str) -> tuple[int, str]:
    num, bag = contains.split(" ", maxsplit=1)
    return int(num), bag

BAG_RULES = tuple(input_data.read("input/input7.txt", to_bag_rules))

if __name__ == "__main__":
    print("Number of bags that can contain a gold bag: "
          f"{get_number_of_bags_able_to_hold_bag(BAG_RULES, 'shiny gold')}")

    print("Number bags inside a shiny gold bag: "
          f"{get_number_of_bags_inside(BAG_RULES, 'shiny gold')}")

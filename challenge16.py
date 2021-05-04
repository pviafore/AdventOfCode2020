import itertools
import operator as op
import re

from dataclasses import dataclass
from functools import reduce

Ticket = list[int]

@dataclass
class Rule:
    name: str
    range1: range
    range2: range

    def matches(self, value: int) -> bool:
        return value in self.range1 or value in self.range2

def strip_known_fields(fields, exclude_fields):
    if len(fields) <= 1:
        return fields
    return [f for f in fields if f not in exclude_fields]

@dataclass
class TicketData:
    rules: list[Rule]
    ticket: Ticket
    nearby_tickets: list[Ticket]

    def get_ticket_scanning_error_rate(self) -> int:
        return sum(itertools.chain.from_iterable(
            self.get_invalid_values(ticket) for ticket in self.nearby_tickets
        ))

    def get_invalid_values(self, ticket: Ticket) -> list[int]:
        return [v for v in ticket if not self.matches_any_rule(v)]

    def matches_any_rule(self, value: int) -> bool:
        return any(rule.matches(value) for rule in self.rules)

    def get_departure_fields_product(self) -> int:
        valid_tickets = [t for t in self.nearby_tickets if len(self.get_invalid_values(t)) == 0]
        valid_tickets.append(self.ticket)
        positions = self.resolve_fields(valid_tickets)
        return reduce(op.mul,
                      [self.ticket[pos] for field, pos in positions.items()
                       if field.startswith("departure")])

    def resolve_fields(self, tickets: list[Ticket]) -> dict[str, int]:
        possible_fields = {index: self.get_valid_fields(index, tickets)
                           for index in range(len(tickets[0]))}
        while any(len(f) > 1 for f in possible_fields.values()):
            single_fields = [f[0] for f in possible_fields.values() if len(f) == 1]
            possible_fields = {index: strip_known_fields(fields, single_fields)
                               for index, fields in possible_fields.items()}
        return {field[0]: index for index, field in possible_fields.items()}

    def get_valid_fields(self, index: int, tickets: list[Ticket]) -> list[str]:
        ticket_fields = [t[index] for t in tickets]
        return [r.name for r in self.rules if all(r.matches(t) for t in ticket_fields)]


def to_rule(data: str) -> Rule:
    field, min1, max1, min2, max2 = re.split(r': |\-| or ', data)
    return Rule(field, range(int(min1), int(max1) + 1), range(int(min2), int(max2) + 1))

def to_ticket(data: str) -> Ticket:
    return [int(n) for n in data.split(',')]

def parse_ticket_data(data: str) -> TicketData:
    rules, ticket, nearby_tickets = re.split(r'\nyour ticket:\n|\nnearby tickets:\n', data)
    return TicketData(
        [to_rule(rule.strip()) for rule in rules.strip().split("\n")],
        to_ticket(ticket.strip()),
        [to_ticket(t.strip()) for t in nearby_tickets.strip().split("\n")]
    )

with open("input/input16.txt") as input_file:
    TICKET_DATA = parse_ticket_data(input_file.read())

if __name__ == "__main__":
    print(TICKET_DATA.get_ticket_scanning_error_rate())
    print(TICKET_DATA.get_departure_fields_product())

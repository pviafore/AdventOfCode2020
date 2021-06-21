from dataclasses import dataclass
from functools import reduce

from typing import Optional, Iterable, Union


Rule = list[str]

@dataclass
class Node:
    value: Union[str, list[list['Node']]]

    def get_text_with_matching_nodes_removed(self, text: str) -> Optional[list[str]]:
        if text == "":
            # we have exhausted the string
            # this is useful for self referential nodes
            return None
        if isinstance(self.value, str):
            if text.startswith(self.value):
                return [text.replace(self.value, '', 1)]
            return None
        options = []
        for nodes in self.value:
            # each individual branch, start with original text each time
            options += reduce(resolve_node, nodes, [text])
        return options

def resolve_node(text: Iterable[str], node: 'Node') -> list[str]:
    remaining_text: list[str] = []
    # keep adding it onto whatever text we've seen so far
    for potential_text in text:
        candidate = node.get_text_with_matching_nodes_removed(potential_text)
        # if we prefixed correctly
        if candidate is not None:
            remaining_text += candidate
    # set the next options for the next part in the branch
    return remaining_text


def resolve_graph(rules: dict[str, list[Rule]]) -> dict[str, Node]:
    # create the nodes up front so that self-referential nodes work
    rules_graph = {num: Node([]) for num in rules.keys()}
    for num, rule in rules.items():
        for option in rule:
            if (len(option) == 1 and option[0].startswith('"') and option[0].endswith('"')):
                rules_graph[num].value = option[0][1]
            else:
                value = rules_graph[num].value
                if isinstance(value, list):
                    value.append([rules_graph[n] for n in option])
    return rules_graph

class MessageData: # pylint: disable=R0903

    def __init__(self, rules: dict[str, list[Rule]], messages: list[str]):
        self.__graph: dict[str, Node] = resolve_graph(rules)
        self.__messages = messages

    def get_number_of_matching_rules(self, rule_number: str):
        answers = [self.__graph[rule_number].get_text_with_matching_nodes_removed(m)
                   for m in self.__messages]
        return len([a for a in answers if a is not None and '' in a])

def get_message_data(substitutions: list[str]) -> MessageData:
    with open("input/input19.txt") as message_file:
        message = message_file.read()
    split_data = message.split("\n\n")
    rules = dict(to_rule(line) for line in split_data[0].split("\n"))
    messages = [line.strip() for line in split_data[1].split("\n")]
    for subst in substitutions:
        key, val = to_rule(subst)
        rules[key] = val
    return MessageData(rules, messages)

def to_rule(text: str)-> tuple[str, list[Rule]]:
    rule_number, rules = text.split(": ")
    rule_parts = [rule.split(" ") for rule in rules.split(" | ")]
    return (rule_number, rule_parts)

MESSAGE_DATA = get_message_data([])
MESSAGE_DATA_WITH_SUBSTITUTIONS = get_message_data(['8: 42 | 42 8', '11: 42 31 | 42 11 31'])

if __name__ == "__main__":
    print(MESSAGE_DATA.get_number_of_matching_rules("0"))
    print(MESSAGE_DATA_WITH_SUBSTITUTIONS.get_number_of_matching_rules("0"))

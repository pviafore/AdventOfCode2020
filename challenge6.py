import itertools

from collections import Counter
from itertools import chain
from typing import Iterable

import common.input_data as input_data

def get_sum_of_any_yes_counts(questions: list[str]) -> int:
    grouped_data = itertools.groupby(questions, lambda s: s != "")
    return sum(get_any_yes_count(q) for has_data, q in grouped_data if has_data)

def get_any_yes_count(questions: Iterable[str]) -> int:
    return len(set(letter for letter in chain.from_iterable(questions)))

def get_sum_of_all_yes_counts(questions: list[str]) -> int:
    grouped_data = itertools.groupby(questions, lambda s: s != "")
    return sum(get_all_yes_count(q) for has_data, q in grouped_data if has_data)

def get_all_yes_count(questions: Iterable[str]) -> int:
    question_list = list(questions)
    yes_answers = Counter(letter for letter in chain.from_iterable(question_list))

    return len([count for count in yes_answers.values()
                if count == len(question_list)])


QUESTIONS: list[str] = input_data.read("input/input6.txt")

if __name__ == "__main__":
    print(f"Sum of any yes counts: {get_sum_of_any_yes_counts(QUESTIONS)}")
    print(f"Sum of all yes counts: {get_sum_of_all_yes_counts(QUESTIONS)}")

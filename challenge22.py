import copy
import itertools
import operator
from typing import Literal

Decks = tuple[list[int], list[int]]

def get_player_decks() -> Decks:
    with open("input/input22.txt") as input_file:
        player_1, player_2 = input_file.read().strip().split("\n\n")
    return [int(n) for n in player_1.split('\n')[1:]], [int(n) for n in player_2.split('\n')[1:]]

def play_game(decks: Decks) -> list[int]:
    player1, player2 = decks
    while player1 != [] and player2 != []:
        card1, card2 = player1.pop(0), player2.pop(0)
        if card1 > card2:
            player1 += [card1, card2]
        else:
            player2 += [card2, card1]
    return player1 if player1 else player2

def play_game_recursively(decks: Decks) -> tuple[Literal[1,2], list[int]]:
    previously_seen_hashes: set[int] = set()
    player1, player2 = decks
    while player1 != [] and player2 != []:
        cards = hash((tuple(player1), tuple(player2)))
        if cards in previously_seen_hashes:
            return (1, player1)
        previously_seen_hashes.add(cards)

        card1, card2 = player1.pop(0), player2.pop(0)
        if card1 > len(player1) or card2 > len(player2):
            winner = 1 if card1 > card2 else 2
        else:
            # play sub game
            winner, _ = play_game_recursively((player1[:card1], player2[:card2]))
        if winner == 1:
            player1 += [card1, card2]
        else:
            player2 += [card2, card1]

    return (1, player1) if player1 else (2, player2) # type: ignore

def get_winning_score(decks: Decks) -> int:
    winning_deck = play_game(copy.deepcopy(decks))
    return sum(itertools.starmap(operator.mul, enumerate(winning_deck[::-1], start=1)))

def get_winning_score_recursive(decks: Decks) -> int:
    _num, winning_deck = play_game_recursively(copy.deepcopy(decks))
    return sum(itertools.starmap(operator.mul, enumerate(winning_deck[::-1], start=1)))


DECKS = get_player_decks()

if __name__ == "__main__":
    print(get_winning_score(DECKS))
    print(get_winning_score_recursive(DECKS))

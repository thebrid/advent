from collections.abc import Iterable
from enum import Enum

from pytest import mark


class Choice(Enum):
    Rock = 0
    Paper = 1
    Scissors = 2


CHOICE_SCORE = {Choice.Rock: 1, Choice.Paper: 2, Choice.Scissors: 3}

OPPONENT_LOOKUP = {"A": Choice.Rock, "B": Choice.Paper, "C": Choice.Scissors}
PLAYER_LOOKUP = {"Y": Choice.Paper, "X": Choice.Rock, "Z": Choice.Scissors}

Guide = Iterable[tuple[str, str]]


def rock_paper_scissors(input_string: str) -> int:
    guide = _parse_input(input_string)
    total_score = 0

    for opponent, player in guide:
        opponent_choice = OPPONENT_LOOKUP[opponent]
        player_choice = PLAYER_LOOKUP[player]

        total_score += CHOICE_SCORE[player_choice] + _get_player_score(opponent_choice, player_choice)

    return total_score


def rock_paper_scissors_with_decryption(input_string: str) -> int:
    guide = _parse_input(input_string)
    total_score = 0

    for opponent, player in guide:
        opponent_choice = OPPONENT_LOOKUP[opponent]
        player_choice = _get_player_choice(player, opponent_choice)

        total_score += CHOICE_SCORE[player_choice] + _get_player_score(opponent_choice, player_choice)

    return total_score


def _get_player_choice(player: str, opponent_choice: Choice) -> Choice:
    if player == "Y":
        return opponent_choice

    match (opponent_choice):
        case Choice.Rock:
            match (player):
                case "X":
                    return Choice.Scissors
                case "Z":
                    return Choice.Paper
        case Choice.Paper:
            match (player):
                case "X":
                    return Choice.Rock
                case "Z":
                    return Choice.Scissors
        case Choice.Scissors:
            match (player):
                case "X":
                    return Choice.Paper
                case "Z":
                    return Choice.Rock

    raise RuntimeError(f"Found no matching combination of {player=} and {opponent_choice=}")


def _get_player_score(opponent_choice: Choice, player_choice: Choice) -> int:
    match (opponent_choice):
        case Choice.Rock:
            match (player_choice):
                case Choice.Rock:
                    return 3
                case Choice.Paper:
                    return 6
                case Choice.Scissors:
                    return 0
        case Choice.Paper:
            match (player_choice):
                case Choice.Rock:
                    return 0
                case Choice.Paper:
                    return 3
                case Choice.Scissors:
                    return 6
        case Choice.Scissors:
            match (player_choice):
                case Choice.Rock:
                    return 6
                case Choice.Paper:
                    return 0
                case Choice.Scissors:
                    return 3


def _parse_input(input_string: str) -> Guide:
    for line in input_string.split("\n"):
        chars = line.split(" ")
        yield chars[0], chars[1]


EXAMPLE_INPUT = """A Y
B X
C Z"""
PUZZLE_INPUT = """C Y
C Y
B Y
A Z
B Z
A X
A Y
A Y
A X
A Y
B Y
A Y
B Y
B Y
B Z
B Z
B Z
B Z
A Y
B Z
A Y
B X
B Y
B X
A X
A X
B Z
A X
A X
B Z
B Z
B Y
B Z
B Z
B Z
B Y
A X
A X
B Z
A X
B X
B X
C Y
B Z
C X
A X
A Y
B Y
A Y
B X
A X
B Y
B Z
B Z
B Y
B Z
C Z
B X
B X
B Z
B Z
B Z
B Z
A Y
B X
A X
C X
B Y
B Z
A Y
B Z
B Z
B Y
B Y
B Z
B Y
B Z
A X
B X
B X
A X
A X
B Z
B Z
B Z
B Z
B Y
B X
B Z
A X
A Y
B Z
A Y
B Z
B Y
B Z
A X
B Y
A Y
B Z
A Z
A Y
A Y
C Y
B Z
B X
A Z
B Z
A X
B Z
A Z
B Z
A X
B Y
A X
B Y
B Z
B X
B X
B Z
B Z
B Z
A X
B Z
A X
B X
B Z
A X
C Z
B Z
B Z
B Y
B Y
B Y
B Z
B Z
A Y
B Z
B Z
C Y
C Z
A X
B Z
B X
B Z
B Z
B Y
A X
B Z
B Y
A Z
B Z
A X
A X
B Y
A Y
B Z
B Z
B X
B Y
A X
A Y
B X
C Z
A Y
B Z
B Z
B Z
A Z
C Y
B Y
B Y
B Z
C Y
B Y
B X
B X
B Z
C Z
A X
B Z
B Z
B Z
B Z
B X
B X
A X
A Z
A Z
A X
C Y
B X
A X
A Y
A X
B X
A Y
B Z
B Z
A Y
A X
B Y
B Z
B Z
A X
A Z
B Z
B X
A X
B Z
B Y
A Y
A Z
B X
A Y
B Z
A Z
B Z
A Y
B Z
B X
B Y
A Y
B Z
B Z
A X
A X
B Y
B Z
A X
B Z
B Z
B Z
B Z
B Z
A Z
B Z
B Z
B X
A Y
C X
B Z
B Y
B Y
B Z
B Z
B Z
B Y
B X
B Y
C X
B Z
A Z
A Y
C X
A X
B X
A X
B X
A Y
B Z
A Y
A Y
B Z
B X
B Z
A Y
B Z
B X
C Z
C X
C Z
B Y
B X
B Z
B Z
B Y
B Z
B Y
B Z
A X
B X
B Z
A X
B Z
B Y
B Z
A X
B Y
C Y
A Z
B Z
C Z
A Y
B Z
A Y
A Z
B Y
A X
A X
B Z
B Z
B Z
A Y
B Z
A Z
B Z
A Y
A Z
B Y
C Z
B Z
A Z
B X
B Z
B Y
B Z
A Z
A Z
B Z
B X
C Z
B X
B Z
B Y
A X
B Z
A X
B X
B Z
B Z
A X
B X
C X
C X
B X
B Y
B Z
B X
B Y
B Y
B Z
A Z
B Z
C X
A Y
C X
B Z
A Y
B Z
B Y
B Z
B X
A X
B X
B Z
A Y
A Y
B Z
B Z
B Z
A Y
B Z
B X
C X
B Z
B Z
C Y
B Z
C Y
B Z
C Y
C X
B Z
C Y
A Y
A Y
C Z
B Z
B X
B Z
B X
C Z
B Z
A Z
B Z
C Y
B Z
A X
A Y
B Y
B Y
B Z
A Y
B X
B Z
B Z
A Z
B X
A Y
A Y
B Z
B Z
B Z
C X
A Z
B X
C Z
B Y
B Z
B X
A Y
B Z
A X
B X
B Y
A Y
B Z
B Z
B Y
A Z
B Z
A X
B Y
A Y
A X
A Y
A X
A X
B X
B Y
B X
B Y
B Z
B Y
B X
A X
B Z
A Z
A X
B Z
B Y
A X
B Y
A X
B X
C Y
B X
B X
B X
C Y
B X
B Y
B Y
B Y
B Y
B X
A Y
C Y
B Z
B Z
B X
B Z
C Y
B Y
B Z
B Z
B Y
B Z
A X
B X
B Y
A X
C Y
B Z
A Y
B Z
B Z
B Z
A X
B Y
B Z
B Y
B Z
A X
B Z
A X
B Y
B Y
B X
B X
A Y
B Z
C Y
A X
A X
B X
B Z
B X
B X
B Z
B Z
A X
B X
B Z
A Z
B Y
A X
B Z
C Y
B Z
B X
B Z
B Z
A Y
A Y
B Z
B X
B Y
B Z
A Y
A Y
B X
B X
C X
B Z
C Z
B X
A Y
B Z
A Z
B Y
A Y
B Z
B X
B X
A Y
B Z
B Y
A X
B Y
B Y
B Y
B X
B Y
B Z
B Y
B Y
A X
C Z
B Z
B Z
A Z
B Z
B Z
A X
B X
A Y
A X
B X
C X
B X
B Z
B Y
A Z
A Y
B Y
B Z
B X
B X
B Z
B Z
B Y
A X
B Z
A Y
A X
B Y
B Z
B Z
B X
A X
A Y
C X
A Y
B Z
B Y
B Z
B Z
C Z
B Z
B X
A X
C Y
B X
B Z
A Z
A X
A Y
B Z
B Z
A Y
A Y
B X
A Y
A Y
B Z
A Y
B Y
B Z
A Y
A Z
B X
B X
B Y
B Z
B Z
A X
B X
C X
B Y
A Y
A X
A X
A X
B Y
A X
A Z
A Y
B X
A Y
B Z
C X
B X
B X
B Z
B X
B X
B Z
A X
B Z
B X
B Z
A Y
B Y
B Z
B Y
B Z
B Z
A X
B Z
A Y
C Z
A Y
B Z
A Y
B X
B Z
B X
C Y
A X
B Z
B Y
A X
A X
B X
B Z
A Z
B Z
B X
B X
B X
B Z
B Z
B Y
B X
B X
A X
B Z
B X
A X
A X
A X
B X
B Z
A Z
B X
B Y
B Y
B Z
B Z
C Z
A Y
A X
B Y
B X
B Z
B X
A X
B Z
B Z
B Y
B Z
B X
B Z
B Z
B X
B X
A X
A X
B X
B Z
B Z
C X
C X
B Z
B Z
B X
B Z
B Y
B X
A X
B Y
A Y
A X
B Z
B Z
C X
B Y
B Z
B Z
B X
B Z
B Z
C Z
B Z
B Y
B Z
B X
A X
B X
B Z
B Z
A Y
B Z
B Z
B Z
B Z
A X
B Z
B Z
B X
B Y
B Y
B Z
A X
B Z
B Y
B X
A X
B X
B Z
B Z
B Z
B X
B Z
B Z
B Z
A Y
B Z
C X
B Y
B Y
B Y
A Y
B Z
B Z
A X
C Z
B Z
B Z
B Z
B X
B Z
A Z
B Z
B Z
B Z
A Z
B Z
C Y
B X
A X
A Y
B Z
B Z
A Z
B Z
B X
A Z
B Y
B Z
B X
B Z
B X
B Y
B Z
A X
B Z
B Z
A Y
B X
B X
B X
A Z
C X
A Z
B Z
B Z
B Z
B X
A Y
C X
A Z
A Y
B X
B Z
B X
B Z
B Y
A Y
B X
C X
A Y
C Z
A X
B Z
B Z
A Z
B X
B Y
B Z
A Y
B Y
A X
A X
C Y
A Y
B X
A X
B Y
B X
B Y
A Y
A X
C Y
B Y
B Y
B Z
B Y
B X
B Z
B Z
B X
A X
B Z
B Z
B Z
B X
B Z
B X
B Z
B Z
B Y
B Y
B X
A X
B Z
B Y
A Y
B Z
B X
B Z
B Z
A Z
B Z
A Y
B Z
A X
B Z
B Z
A Y
B Z
A X
B Z
A Y
A Y
A Z
B X
B Z
B Y
A Z
C Z
B Z
A X
A X
B X
A Z
B X
B X
B Z
C X
B Z
B Z
B Z
B Z
B X
A Z
A Y
B Z
B Y
C Z
B Y
B Z
A Y
B X
B X
B Z
A X
A Y
B Z
B X
B Y
A Y
C Y
C Y
B Z
A Y
B Y
A Y
B Z
B Z
A X
B X
A X
B X
A Y
A X
B Z
A X
B Z
B X
B Z
B X
B X
A X
A Y
B Z
B X
B X
A X
A Y
A X
B Y
B Z
B Z
B Z
B Z
B Z
B X
B Y
A Y
B X
B Z
A Y
B X
A X
B Z
C X
B Y
A Y
A X
A X
B X
B X
B Z
B Z
B Z
B X
B Y
B X
B Z
B X
B Y
B X
B Z
B X
B Y
B X
B Z
B Z
B Z
A X
C X
C Y
A Y
B X
B X
A Y
B Z
B X
B Z
B X
B X
C X
B Z
B Z
B Y
A Z
A Z
C X
B X
C Y
B Z
C X
B Z
A Y
C Z
B X
B Y
A Y
B Y
B X
B Z
A Y
A Z
C X
B Z
A X
B X
B Z
C Z
A Y
B Z
B Z
A X
A X
B Z
B Y
C Z
B Z
B X
B Z
A X
A X
B Y
A X
B X
A Y
B Z
A Y
B Z
A Y
B Z
A X
B Y
B Z
B Z
B Z
A X
A X
B X
B Z
A X
B Z
A X
A X
B Z
B Z
B Z
B X
B Y
B Z
B Z
B X
B Z
B Y
B Z
C Y
B X
C Z
B Z
B Z
A Y
B Z
B X
A Y
B Z
B X
B Z
B Z
B Y
B Z
A Z
A Y
B Z
B Z
B Y
A Y
B Z
A X
B X
A Z
A X
B X
B Z
B X
B Z
B Z
B Y
B Y
B Z
B Y
B Z
B Z
A X
B X
B Y
B Y
C Z
A X
B Y
A Y
B Z
B Z
B Z
C X
B X
A Z
B Y
A X
C X
B Z
B Z
B Z
B Y
A Y
A Y
B Y
B Z
B Z
B Z
C X
A X
B Z
A Y
B X
B Z
B Z
B Z
B Z
B X
B Y
B Z
B Z
A Y
C X
A X
B Z
B Z
A Y
A Y
B Z
A Y
B Y
A X
B Z
B Z
A Y
B Z
B Z
A X
A X
B X
B Z
B Z
A X
B Z
B Z
C Y
B Z
A X
B Z
A X
B Z
A X
B X
A X
A Y
B Z
B X
A X
B Z
A X
A Z
B Z
B Z
B Z
A Y
B X
A X
B Y
A Y
B Z
B Z
B X
B Z
B X
B X
A X
B Z
A Y
A X
B X
A Z
B X
B Y
B Z
B X
B X
B Z
C X
A X
B Z
B Y
C Z
B Z
A Z
A Z
A X
A Y
B Z
B Z
B X
A Z
B Z
B Z
B X
B Y
B X
B Z
B X
B Z
A Y
A X
B Z
B X
B Y
B Z
B Z
B Z
B Z
C X
C X
B Z
B X
B Z
B Z
B Z
B X
B Z
B Z
B Z
B X
B Z
B Z
B Z
C Y
B Z
B Y
B Z
A Z
A Y
B Z
A Y
C X
A X
B X
A Y
B Z
A Y
B Z
B Y
B Z
B Z
C Y
B Y
B Z
B Z
B X
B Y
B Z
B Y
B Z
B X
B Y
B Z
B Z
B Z
B Y
B Y
B Z
B Z
C X
B Z
A Y
B Z
B Z
B Y
B Y
B Z
B Z
A Y
B Z
A Z
C X
A Y
A Y
A X
B Z
A X
C Y
A Z
C Y
C X
B Z
A X
A Y
B Z
B Z
B Z
B Z
B Y
A Z
A Y
B Y
A Y
A Z
B X
B Z
B Z
A X
C Y
B Z
B X
C X
A Z
B Z
B X
B Y
A X
A X
B Z
C X
B Z
B Z
B X
B Z
B Z
B Z
A X
B Z
B Y
B Z
B Z
B Y
B X
A X
B Z
A X
A X
B Y
B Z
B X
A Y
C X
B Y
A X
A X
A X
C Y
B X
C Z
A X
B Z
A Z
B Z
A X
A Y
B Z
A X
B X
A Y
A X
A Y
B X
B Y
B Z
B Y
C X
C Y
B Z
B Y
B Z
A X
C Z
B Z
A X
B X
A X
B X
B Z
B X
B Z
B Z
B Z
A X
A X
B Z
B X
B Z
B Z
B Z
A X
B Z
B X
A X
C Z
A Y
B Z
A Y
B Z
B Z
B Z
C Z
B Z
B Z
A X
B X
A X
B X
A X
B Z
B Z
B X
B Z
A X
A Y
A Y
A Y
B Z
B Z
B Z
B Z
A X
B Z
B Z
B Y
B Z
A Z
B Z
A Y
B Y
B Y
C Y
B X
B Z
B Y
B Z
B Y
B Z
B Z
A Y
B X
A Z
B Z
A X
B Y
A X
B Z
B Y
A X
B X
B Z
B Z
B Z
A Y
A Y
A X
A Y
A Y
B X
B Z
B Y
B Y
B X
B Y
B X
B X
B X
B Z
B Z
B Z
A Y
A Z
B Y
C X
B X
B Z
C Y
B Z
C Y
B Z
B Z
B Z
B X
A X
B Z
B Z
A X
B Z
B Z
B Z
B Z
B Z
B Z
B X
A X
A Y
B Y
B Z
B Y
B X
A Z
A X
B X
B Y
B Z
B Z
B Z
B X
C X
B X
A Z
A X
A Y
B Z
B Z
A X
B Z
A Y
B X
B Z
B Y
B Y
A X
B X
B Z
B Z
B Z
B Z
B Y
A Z
A Y
B X
A X
B Y
B Z
C Y
B Z
B Z
B X
A Z
A Y
B Y
B Z
A Y
B Y
A Y
A X
A Y
B Y
C X
C Z
B X
A Z
A X
B Y
B X
A X
B Z
A Y
A Z
B Z
B Z
B Z
A X
B Z
B Y
B Z
A X
A Y
B Z
B X
C X
B Z
A Y
B Z
B Z
B X
B Z
B Z
A Y
A X
B Z
C Y
A Y
B Y
B Z
A X
B Z
B Z
B Z
B Z
C X
B Y
B Z
B X
B Z
B Z
B Z
B Z
B Z
B Y
A X
B Y
A Y
A X
A X
B Z
B Z
B Z
C X
B X
B Z
A X
A X
B Y
A X
B Z
B Z
B X
B Y
B Y
B Y
A Y
A Y
A X
A X
B Z
B Y
B Y
B X
B Y
B Z
A Z
B Z
A Z
B X
B Y
C Y
B X
B X
A X
A X
A X
A X
B Z
B Z
A Z
B X
B X
B X
B X
B X
B Z
B Z
B Z
B Z
B Z
B Y
B Z
B Z
A Y
A Z
C Y
B Y
A X
B Z
B X
A Y
B Y
A Y
C Z
A X
A Y
B X
B X
C Z
B Y
A Y
A Y
A X
B X
A X
B X
A Y
B Z
B Z
A Z
B X
B Z
B Z
B Y
A Y
B Z
B Y
B Z
B Z
B Z
C X
B Y
A Y
B Z
A Y
A Y
A X
B X
B Y
C Y
C X
B Z
B Z
B Z
A Y
A Z
B Y
B X
B X
B Y
B Z
B Z
A Y
B Y
B Z
B Z
B Z
A X
C Y
B Z
A Z
C Z
B X
B Y
B Z
A Z
A X
B X
A X
C X
B Z
A X
B Y
C Y
B Y
B Z
B X
A Y
B Z
B Z
B Z
A X
B Z
B Z
B Z
B Z
A X
B Z
B X
B X
B Z
C X
A Y
B Z
B X
B Z
B Y
B Z
B Y
C Y
A X
B Y
B Z
B Z
B X
B Z
A X
B Z
A X
B Y
B Z
A X
B Z
B X
A Z
B Z
C X
B Z
B Y
B Y
B Y
B Z
B X
B X
A X
A X
B Z
B Z
A X
A X
A Z
A Y
C Z
B Z
B Y
C X
B X
B Y
B Y
A Y
B Z
B Z
B Y
C Y
B Z
A Y
B Z
B Z
B Z
B Z
A Y
B Z
B Z
B Z
A X
B X
A Y
B Y
B Z
B Z
B Z
A Y
B Z
B Z
B Z
B Y
B Y
B X
B X
B Y
C Z
B X
B Y
C Y
A Y
B Z
A Z
B Z
A Y
B X
B Z
B X
C Z
A Y
B X
B Z
A X
A X
B Z
B Z
B Y
B Z
C Y
C X
B Z
B Z
A X
B X
A Y
B Y
B Y
C Z
A X
B X
B Z
A Y
B Z
C X
B Z
A Z
C X
A Y
A Z
B Z
A Y
A X
B Z
B Y
B Z
B X
B Z
A X
B Z
A Z
B Z
B Z
B Y
A X
B Z
B X
B Y
B Y
A Y
A X
C Z
B Y
C Z
A X
B X
B Z
B X
C X
B Z
B Z
A X
A Y
A Z
A Z
B Z
B Z
A X
B Z
B Y
A X
A Y
B Z
B X
A Y
B Z
B Y
B X
B Z
A Z
B Y
A Y
A X
B Z
B Z
B Z
B Z
A X
B Y
B Z
B Z
B Z
A Z
B Y
A X
C Y
B Z
B Z
B Y
B X
B Z
A Y
A X
B Z
B Y
B Z
A Y
C X
B Y
B Z
B Z
A Y
B X
B Z
B Z
A X
B X
B Z
A Z
B Y
B Z
B Z
B Z
B Z
B Z
A Z
B X
A Y
C Y
B Z
A Y
B Z
B Z
A Y
B Z
B Z
A Y
A Y
B X
B Y
A X
B Z
A Y
B Z
A Z
B Z
B X
B Z
B Z
B Y
B Y
B Z
A X
B Y
B Z
B Z
B Z
B Y
A Y
B Z
B Y
B Z
B Z
B X
A X
B Y
A X
A X
B Z
A X
B Z
C X
B Y
B Z
B Z
B Y
A X
B Z
B Z
B Y
B X
B Z
B X
B Z
C Y
B Y
B Z
B Z
A Z
B Z
B Z
A Y
B Z
B Y
A X
B Z
B Z
B Z
B X
B Z
B Y
B Z
B X
C Z
B Y
B Z
B Z
B Y
A X
A X
B Y
A Y
B Z
B X
B Y
B Z
B Y
B Z
A X
C X
B Z
A Z
C Y
A X
B Y
B Y
A X
A X
B Y
B Z
C Y
B Z
B Y
A X
B Y
B Y
B Z
B X
B Z
C X
C Y
B X
A Y
B Z
B Z
B Z
A X
B Z
B Z
B X
B X
B X
B X
B Y
A Y
B Z
B Z
B Z
A Z
B X
B X
B X
B X
B Z
A Y
B Y
B Z
A X
A X
A X
B Y
B Z
B X
B Z
A Z
B Z
B Z
A Y
C Z
A X
B Z
C X
B Z
B Z
B Z
B Y
B Y
B Z
C X
B Z
A Y
B X
C X
A Y
C X
B Z
B X
A Z
B Z
C Y
B Y
B X
B Z
B Y
A Y
B X
A Z
B Z
B Z
C Z
B Z
B Y
B Z
A Y
C Y
B Z
B X
A Y
B Z
B Z
B Y
B Y
B Z
A X
A Y
A X
A Z
B Z
B Z
B Y
A Y
B Y
B Z
B Y
A Y
B X
A X
B Y
B Y
B X
B Z
B Y
C X
B Z
B Z
B Z
A X
B Z
B X
A Y
A Y
B Z
A Y
A Y
A Y
B Y
B Z
A X
C X
B Y
A X
C X
B Z
B Y
A Y
B X
B Z
B Y
B Y
B Z
B Z
A Y
B X
B X
A X
B Z
B X
B Z
B Z
C Z
C Y
A X
B X
C X
B X
A Z
A X
B Y
C X
B Y
A X
A X
A X
B X
B Z
B X
B Y
B Z
B Z
B Z
B Z
A X
A X
B X
B Z
A Z
A X
B Z
C Y
B Z
A X
B Z
A Z
B Z
B Z
A Y
B Y
B Z
B X
B Z
B Z
C Y
B Z
B X
A X
B Y
B Z
A Y
A X
B Z
B Y
B Z
B X
A Y
C Z
B X
B Z
A X
B X
B Z
B Z
A X
B Y
B X
B Z
B Z
B Y
B X
B X
C X
B Z
C X
B Z
C Y
A Y
C X
B X
B Y
B Z
B Y
B Z
A X
B Z
B Z
B Y
B Y
A X
A X
A Y
B Z
B Z
A Y
B Z
A X
B Z
B X
B X
B X
A Y
B Z
B Z
A Y
B Z
A Z
B Y
B X
A Z
A Z
B Z
A Y
B Z
B Y
B Y
B X
A Y
B X
B Z
B Z
B Y
B X
B Z
B Z
B Z
B Z
A X
B X
B X
B Z
A X
B X
B Z
B Z
B Y
A Y
B Z
B Y
B Y
A X
B X
B Y
C X
C X
B Y
A Y
A Z
B X
B Z
B Z
B Z
B Z
A X
A Y
A Y
B Y
C X
B Z
A Y
B X
C Z
B X
B Y
A Y
B X
B Y
B Z
B Y
B X
B Y
A Z
B Z
A X
B X
B X
B Z
B Y
B Y
B Y
A X
B X
B Y
B Z
A Y
A X
B X
B Z
B Z
C X
A Z
B Z
A X
A Y
C X
B Z
B Z
A X
B X
A Y
A Y
B Z
B Z
B X
A Z
B Z
B Y
A Y
B Z
B Y
A Y
B Y
B Z
A X
B Y
A X
A Y
A X
A X
B Y
A Z
B Z
A Y
B Z
A Z
A Y
B Z
B Y
B Z
B X"""


@mark.parametrize(("input_string", "expected_output"), [(EXAMPLE_INPUT, 15), (PUZZLE_INPUT, 14827)])
def test_rock_paper_scissors(input_string: str, expected_output: int) -> None:
    assert rock_paper_scissors(input_string) == expected_output


@mark.parametrize(("input_string", "expected_output"), [(EXAMPLE_INPUT, 12), (PUZZLE_INPUT, 13889)])
def test_rock_paper_scissors_with_decryption(input_string: str, expected_output: int) -> None:
    assert rock_paper_scissors_with_decryption(input_string) == expected_output

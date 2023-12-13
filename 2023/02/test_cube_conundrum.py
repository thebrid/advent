# flake8: noqa: E501
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from math import prod

from pytest import mark

DrawCount = dict[str, int]


@dataclass
class Game:
    game_id: int
    draws: list[DrawCount]


def cube_conundrum(puzzle_input: str) -> int:
    games = _parse_input(puzzle_input)
    return sum(game.game_id for game in games if _is_game_possible(game))


def cube_conundrum2(puzzle_input: str) -> int:
    games = _parse_input(puzzle_input)
    return sum(_get_minimum_set_power(game) for game in games)


def _is_game_possible(game: Game) -> bool:
    possible = all(_is_draw_possible(draw) for draw in game.draws)
    return possible


def _is_draw_possible(draw: DrawCount) -> bool:
    EXPECTED = {"red": 12, "green": 13, "blue": 14}
    output = all(colour in EXPECTED and count <= EXPECTED[colour] for colour, count in draw.items())
    return output


def _parse_input(puzzle_input: str) -> Iterable[Game]:
    for line in puzzle_input.splitlines():
        yield _parse_game(line)


def _parse_game(line: str) -> Game:
    colon_loc = line.find(":")
    return Game(game_id=int(line[5:colon_loc]), draws=_parse_draws(line[colon_loc + 2 :]))


def _parse_draws(line: str) -> list[DrawCount]:
    draws = line.split("; ")
    return [_parse_draw(draw) for draw in draws]


def _parse_draw(draw: str) -> dict[str, int]:
    cubes = draw.split(", ")
    output = dict[str, int]()

    for cube in cubes:
        tokens = cube.split(" ")
        output[tokens[1]] = int(tokens[0])

    return output


def _get_minimum_set_power(game: Game) -> int:
    minimums = defaultdict[str, int](int)

    for draw in game.draws:
        for colour, count in draw.items():
            minimums[colour] = max(minimums[colour], count)

    return prod(minimums.values())


EXAMPLE_INPUT = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

PUZZLE_INPUT = """Game 1: 1 red, 10 blue, 5 green; 11 blue, 6 green; 6 green; 1 green, 1 red, 12 blue; 3 blue; 3 blue, 4 green, 1 red
Game 2: 3 red, 5 green; 5 green, 7 red; 1 blue, 7 red, 3 green; 3 red, 2 blue; 5 green, 4 red
Game 3: 4 blue, 4 green; 2 green, 2 blue; 8 green, 2 red, 3 blue
Game 4: 3 blue, 15 green; 16 green; 2 red, 7 green; 2 blue, 14 green
Game 5: 8 green, 6 red, 16 blue; 8 red, 12 green; 1 red, 9 green, 16 blue; 8 red, 3 green; 2 blue, 5 red, 10 green; 15 red, 4 blue, 8 green
Game 6: 5 blue, 2 green; 6 red, 3 green; 4 green, 4 blue, 2 red; 14 blue, 2 red
Game 7: 2 green, 6 blue, 1 red; 2 blue, 1 red; 8 blue; 5 blue, 1 green; 6 blue, 1 red; 2 blue
Game 8: 1 red, 10 blue, 1 green; 6 blue, 1 red; 3 blue, 2 green; 1 red, 1 blue, 3 green; 13 blue; 10 blue, 3 green, 3 red
Game 9: 2 blue; 8 green, 3 blue; 4 green; 14 green, 1 red, 2 blue; 3 blue, 1 red, 12 green
Game 10: 1 blue, 7 green; 1 red, 3 green, 5 blue; 1 blue, 5 green, 1 red; 13 green, 5 blue, 2 red
Game 11: 1 green, 10 red, 6 blue; 15 red, 12 blue; 18 red, 1 green, 1 blue
Game 12: 16 red, 8 blue, 1 green; 15 red, 3 blue, 1 green; 5 red
Game 13: 6 red, 7 blue, 7 green; 3 blue, 4 red, 13 green; 1 blue, 6 red, 11 green; 2 red, 1 blue, 14 green; 8 green, 5 blue, 2 red; 4 blue, 18 green, 4 red
Game 14: 16 red, 3 blue, 1 green; 7 green, 3 red; 16 red, 15 green, 3 blue; 3 blue, 13 red, 10 green
Game 15: 1 blue, 1 red; 3 blue, 2 green; 1 red; 2 red, 2 green, 3 blue; 3 blue, 1 red, 3 green
Game 16: 9 red, 3 blue; 13 red, 9 blue; 9 blue, 10 red; 5 red, 10 blue, 1 green; 2 red, 6 green, 8 blue; 6 green, 13 red, 5 blue
Game 17: 15 red, 17 green, 8 blue; 18 red, 16 blue, 15 green; 8 blue, 17 green, 10 red; 5 green, 3 red, 12 blue
Game 18: 2 blue, 11 red, 2 green; 1 green, 11 red, 11 blue; 1 red, 4 blue; 10 blue, 9 red; 1 blue, 7 red
Game 19: 2 blue, 3 green, 5 red; 8 blue, 16 green; 12 red, 7 blue, 8 green; 9 green, 1 blue; 3 red, 16 green, 10 blue
Game 20: 3 blue, 5 green, 6 red; 2 red, 8 blue, 7 green; 7 green, 3 blue; 2 red, 11 blue; 1 green, 6 red, 3 blue
Game 21: 16 red, 3 blue, 8 green; 10 red, 15 blue, 3 green; 6 green, 13 red, 15 blue; 11 green, 13 blue, 10 red
Game 22: 8 green, 1 blue; 2 blue, 9 green, 3 red; 2 red, 2 blue; 1 red, 3 blue, 8 green; 2 blue, 1 green; 1 green, 2 blue
Game 23: 2 blue, 8 red, 5 green; 9 green, 2 blue; 10 red, 2 green; 12 red, 1 blue; 11 green, 2 blue, 13 red; 7 green
Game 24: 6 red; 13 green, 7 red, 10 blue; 7 green, 9 red, 1 blue; 3 blue, 2 green, 2 red
Game 25: 7 green, 1 red, 2 blue; 8 green, 2 blue, 5 red; 5 blue, 8 green, 4 red; 5 blue, 2 green, 1 red; 5 green, 3 red, 7 blue; 3 blue, 6 green, 1 red
Game 26: 6 green, 3 red; 1 blue, 2 green, 2 red; 2 green, 2 red, 3 blue; 4 blue, 8 red, 2 green; 1 red, 1 green, 1 blue; 6 red, 5 blue
Game 27: 4 green, 13 blue, 2 red; 2 red, 7 green, 10 blue; 14 blue, 11 green, 1 red; 10 blue, 15 green
Game 28: 4 green, 13 red, 7 blue; 2 red, 5 blue; 5 blue, 4 green
Game 29: 6 green, 15 red; 1 blue, 6 red, 8 green; 6 green, 1 blue; 12 red; 1 green, 7 red, 1 blue
Game 30: 4 blue, 4 green, 2 red; 6 blue, 9 red, 20 green; 9 blue, 4 red, 2 green; 8 red, 8 blue, 1 green; 6 green, 12 blue, 2 red; 8 green, 8 red
Game 31: 9 blue; 1 red, 2 blue, 5 green; 2 blue, 2 red, 9 green; 2 blue, 1 red, 8 green; 11 green, 2 red, 3 blue; 7 green, 5 blue
Game 32: 15 red, 5 green; 4 green, 2 blue, 3 red; 1 blue, 9 red; 1 blue, 15 red; 4 blue, 2 red, 8 green; 3 green, 3 blue
Game 33: 13 blue, 1 red, 1 green; 8 blue, 6 red; 4 blue, 2 red
Game 34: 5 blue, 9 red, 7 green; 8 red, 6 green, 5 blue; 2 blue, 7 green, 12 red
Game 35: 4 blue, 15 red; 1 green, 10 blue, 7 red; 9 red, 3 green, 1 blue; 13 red, 9 blue; 3 blue, 2 red
Game 36: 4 blue, 18 green, 2 red; 5 green, 6 blue, 11 red; 6 red, 12 blue, 14 green; 19 green, 10 blue, 7 red; 7 red, 8 green, 9 blue
Game 37: 16 blue, 5 green, 18 red; 3 blue, 14 green, 1 red; 4 blue, 3 green, 14 red; 12 green, 7 red, 15 blue; 15 green, 11 blue, 2 red; 8 blue, 13 green, 6 red
Game 38: 6 red, 4 blue, 12 green; 3 red, 11 blue; 16 green, 2 blue, 8 red; 4 blue, 11 red, 4 green; 17 green, 7 red, 10 blue; 9 blue, 15 green, 1 red
Game 39: 1 green, 1 red, 10 blue; 1 red, 5 blue, 2 green; 4 red, 7 blue; 9 red, 6 green, 5 blue; 1 green, 2 blue, 9 red
Game 40: 13 blue, 11 red, 12 green; 8 green, 11 red, 4 blue; 2 blue, 2 green, 12 red; 2 green, 3 red, 13 blue; 13 blue, 6 red, 2 green; 4 green, 6 red, 8 blue
Game 41: 12 red, 4 green, 13 blue; 4 red, 7 blue, 10 green; 17 green, 17 red, 11 blue
Game 42: 1 red, 1 green; 1 red, 4 green; 1 blue, 4 red, 4 green; 3 red; 1 blue, 3 green, 1 red
Game 43: 7 blue, 10 green; 5 blue, 2 green; 2 blue, 1 green, 4 red; 14 red, 6 green, 7 blue; 4 green, 14 red, 8 blue; 4 green, 6 red
Game 44: 9 green, 4 red; 4 red, 6 green; 5 red, 2 blue, 7 green; 9 blue, 1 green, 14 red
Game 45: 20 blue, 4 red, 6 green; 3 blue, 1 green, 6 red; 8 blue, 8 green, 11 red
Game 46: 1 green, 6 red; 6 red, 3 blue, 3 green; 6 red, 3 blue, 4 green; 1 blue, 5 red; 1 green, 4 red, 1 blue; 2 green, 4 red
Game 47: 12 green, 8 red, 4 blue; 7 green, 6 red, 11 blue; 4 red, 11 blue, 12 green
Game 48: 1 green, 3 blue; 13 green, 3 red, 11 blue; 7 blue, 1 green, 2 red; 7 red, 15 green, 4 blue; 4 red, 8 blue, 10 green; 15 green, 8 blue, 6 red
Game 49: 2 red; 2 red, 9 blue; 4 blue, 1 green
Game 50: 10 blue, 1 green, 18 red; 13 red, 1 green, 7 blue; 4 red, 2 green, 9 blue; 2 green, 4 red, 10 blue; 7 blue, 3 red; 19 red, 9 blue
Game 51: 2 green, 2 red, 5 blue; 9 red, 5 blue; 3 red, 10 blue; 9 blue, 6 red, 7 green; 2 red, 5 blue
Game 52: 6 blue, 3 green; 5 green, 3 blue, 5 red; 1 blue, 2 green, 2 red
Game 53: 2 blue, 9 green, 15 red; 18 red, 1 blue; 13 red, 12 green; 7 green, 2 blue, 9 red
Game 54: 18 green; 2 red, 6 green; 6 red, 9 green, 1 blue; 1 blue, 4 green, 5 red; 3 red; 3 green, 4 red
Game 55: 5 red, 2 blue, 5 green; 10 blue, 4 green, 8 red; 15 green, 9 blue, 9 red; 1 green, 9 blue
Game 56: 8 green, 11 blue, 1 red; 1 blue, 1 red, 4 green; 8 blue
Game 57: 5 green, 4 blue; 1 blue, 4 green; 1 red, 1 green, 3 blue; 1 red, 2 blue, 6 green
Game 58: 8 green, 10 red, 10 blue; 8 blue, 6 green, 12 red; 9 green, 11 blue, 1 red; 12 red, 5 green, 11 blue; 7 red, 2 green, 8 blue
Game 59: 10 red, 1 green, 3 blue; 16 red, 1 green, 4 blue; 9 red, 2 blue; 1 red
Game 60: 11 blue, 13 green, 10 red; 15 red, 12 blue; 3 blue, 9 green, 6 red; 12 blue, 5 green
Game 61: 2 blue, 7 red; 3 green, 14 blue, 11 red; 7 red, 10 blue; 6 blue, 3 green, 4 red; 10 blue
Game 62: 1 blue, 7 green; 6 red, 12 green, 1 blue; 8 red
Game 63: 1 blue, 3 green, 1 red; 8 green, 10 red, 1 blue; 8 green, 11 red; 1 blue, 11 green, 5 red; 8 green, 11 red, 2 blue; 2 blue, 10 red, 6 green
Game 64: 17 green, 2 blue; 12 blue, 8 green; 11 green, 3 red, 4 blue; 5 red, 9 green, 14 blue
Game 65: 7 blue, 12 green, 5 red; 13 green, 5 blue, 4 red; 4 blue, 8 green, 1 red; 5 red, 10 green, 10 blue; 5 red, 5 blue, 15 green; 4 red, 9 green, 10 blue
Game 66: 8 green, 2 red; 8 red, 4 green; 5 red, 2 blue, 7 green
Game 67: 10 green, 7 blue, 2 red; 15 blue, 1 green, 9 red; 2 red, 7 green, 18 blue; 3 green, 5 blue, 8 red; 10 green, 11 blue, 1 red; 10 green, 4 red, 17 blue
Game 68: 13 green, 10 blue, 7 red; 1 red, 15 green, 7 blue; 17 green, 14 red, 3 blue; 6 green, 8 blue, 6 red; 4 red, 3 blue, 5 green
Game 69: 1 red, 6 green, 3 blue; 3 red, 4 blue, 6 green; 2 blue, 2 red, 1 green; 6 blue, 9 green, 2 red; 5 green, 6 blue
Game 70: 1 green, 1 red, 3 blue; 2 green, 4 blue, 8 red; 5 red, 2 green, 3 blue; 3 green, 1 red, 3 blue; 3 green, 4 blue
Game 71: 11 blue, 13 green; 1 red, 11 green, 3 blue; 6 blue, 14 green, 1 red; 5 blue, 17 green
Game 72: 3 blue, 10 green, 4 red; 2 green, 6 red, 13 blue; 1 green, 1 blue, 6 red; 5 red, 1 blue, 1 green; 2 green, 5 red, 5 blue; 9 blue, 10 green, 6 red
Game 73: 6 red, 4 green, 1 blue; 1 blue, 5 red, 3 green; 2 red, 11 green, 3 blue
Game 74: 13 green, 2 red, 2 blue; 5 blue, 6 green; 12 green, 3 red, 4 blue; 2 green
Game 75: 9 red, 10 blue, 6 green; 12 blue, 9 red; 11 red, 6 green; 12 blue, 2 red, 1 green
Game 76: 1 green, 2 blue, 5 red; 2 blue, 1 green; 1 blue, 2 green, 1 red; 2 blue, 1 red; 3 green, 3 red
Game 77: 5 green, 12 blue, 3 red; 11 blue, 9 green, 13 red; 8 blue, 13 green, 13 red
Game 78: 2 red, 3 blue, 1 green; 1 green, 19 blue, 1 red; 7 blue, 2 green, 2 red
Game 79: 5 red, 1 blue, 4 green; 1 blue, 9 green, 10 red; 13 red, 1 green; 1 blue, 1 red, 5 green
Game 80: 13 green, 2 blue; 1 red, 4 blue, 13 green; 5 red, 7 green, 4 blue
Game 81: 3 red, 4 blue, 12 green; 16 green, 5 red, 1 blue; 4 blue, 2 red, 2 green; 4 blue, 5 red, 13 green; 8 red, 4 blue, 13 green; 16 green, 3 red
Game 82: 6 red, 3 green, 2 blue; 1 green, 6 red, 2 blue; 3 blue, 8 green, 9 red
Game 83: 3 green, 3 red, 1 blue; 3 blue, 4 green, 3 red; 3 blue, 4 green, 1 red; 2 red, 8 green, 2 blue
Game 84: 5 red, 6 blue, 3 green; 1 blue, 2 green; 3 green, 2 blue, 2 red; 1 red, 3 green, 6 blue; 12 red, 2 green; 4 blue, 2 green, 4 red
Game 85: 11 green, 4 blue, 9 red; 13 red, 1 blue, 11 green; 7 green, 8 blue, 7 red; 1 red, 4 blue
Game 86: 3 blue, 19 green, 7 red; 19 green, 1 red, 1 blue; 9 green, 2 red; 7 red, 6 green, 1 blue
Game 87: 1 blue, 1 green, 4 red; 1 green, 6 red; 6 red, 2 blue; 8 red, 3 blue
Game 88: 9 red, 6 blue; 4 red, 1 blue, 2 green; 1 green, 10 blue, 6 red; 2 blue, 1 green, 10 red; 7 red, 9 blue
Game 89: 3 blue, 15 green, 1 red; 1 red, 13 green, 3 blue; 4 blue, 14 green, 4 red; 10 green, 1 blue
Game 90: 1 red, 13 green; 3 green, 1 red, 5 blue; 5 blue, 6 green; 14 green, 4 blue; 3 blue, 10 green; 13 green, 1 red
Game 91: 13 green, 11 red, 4 blue; 14 red, 1 green, 10 blue; 4 red, 2 green, 3 blue
Game 92: 2 red, 3 blue, 6 green; 2 red, 2 blue, 8 green; 14 blue, 1 red, 1 green
Game 93: 15 blue, 2 red, 13 green; 8 green, 2 red, 8 blue; 6 blue, 1 red, 2 green
Game 94: 5 red, 4 green, 9 blue; 1 red, 5 green, 4 blue; 11 blue, 4 green, 2 red
Game 95: 9 blue, 3 green; 2 green, 12 blue; 10 green, 3 blue; 1 green, 1 red, 10 blue
Game 96: 4 blue, 2 red; 3 green, 10 blue, 7 red; 2 blue, 7 green, 1 red; 13 blue, 9 green; 10 blue, 4 green, 1 red
Game 97: 6 red, 4 green; 1 blue, 13 red; 3 green, 13 red
Game 98: 1 red, 13 blue, 1 green; 7 green, 5 blue, 3 red; 15 blue, 6 green; 4 blue, 5 green; 13 blue, 2 green, 1 red; 4 blue, 3 red, 2 green
Game 99: 1 red, 2 green; 2 red, 2 blue, 1 green; 3 green, 1 blue, 6 red; 3 red, 4 green; 5 red, 1 blue, 4 green; 1 blue, 2 red, 1 green
Game 100: 9 green, 2 blue, 12 red; 2 blue, 14 red, 2 green; 14 red, 12 green"""


@mark.parametrize(
    ("puzzle_input", "expected_output"),
    [(EXAMPLE_INPUT, 8), (PUZZLE_INPUT, 2563)],
)
def test_cube_conundrum(puzzle_input: str, expected_output: int) -> None:
    assert cube_conundrum(puzzle_input) == expected_output


@mark.parametrize(
    ("puzzle_input", "expected_output"),
    [(EXAMPLE_INPUT, 2286), (PUZZLE_INPUT, 70768)],
)
def test_cube_conundrum2(puzzle_input: str, expected_output: int) -> None:
    assert cube_conundrum2(puzzle_input) == expected_output

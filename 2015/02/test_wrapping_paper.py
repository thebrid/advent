from dataclasses import dataclass
from os.path import dirname, join

from pytest import mark


@dataclass
class Present:
    length: int
    width: int
    height: int


def calculate_wrapping_paper(raw_input: str) -> int:
    presents = parse_input(raw_input)
    return sum(calculate_wrapping_paper_single_present(present) for present in presents)


def calculate_wrapping_paper_single_present(present: Present) -> int:
    side1 = present.length * present.width
    side2 = present.width * present.height
    side3 = present.height * present.length

    return 2 * (side1 + side2 + side3) + min(side1, side2, side3)


def calculate_ribbon(raw_input: str) -> int:
    presents = parse_input(raw_input)
    return sum(calculate_ribbon_single_present(present) for present in presents)


def calculate_ribbon_single_present(present: Present) -> int:
    side1 = 2 * (present.length + present.width)
    side2 = 2 * (present.width + present.height)
    side3 = 2 * (present.height + present.length)
    volume = present.length * present.width * present.height

    return min(side1, side2, side3) + volume


def parse_input(raw_input: str) -> list[Present]:
    return [parse_line(line) for line in raw_input.splitlines()]


def parse_line(line: str) -> Present:
    tokens = line.split("x")
    return Present(int(tokens[0]), int(tokens[1]), int(tokens[2]))


PUZZLE_INPUT = open(join(dirname(__file__), "puzzle_input.txt")).read()


@mark.parametrize(("raw_input", "expected_output"), [("2x3x4", 58), ("1x1x10", 43), (PUZZLE_INPUT, 1588178)])
def test_wrapping_paper(raw_input: str, expected_output: int) -> None:
    assert calculate_wrapping_paper(raw_input) == expected_output


@mark.parametrize(("raw_input", "expected_output"), [("2x3x4", 34), ("1x1x10", 14), (PUZZLE_INPUT, 3783758)])
def test_ribbon(raw_input: str, expected_output: int) -> None:
    assert calculate_ribbon(raw_input) == expected_output

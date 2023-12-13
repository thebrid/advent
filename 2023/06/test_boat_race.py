from collections.abc import Iterable
from dataclasses import dataclass
from math import prod

from pytest import mark


@dataclass
class Race:
    duration: int
    record_distance: int


def boat_race(input_string: str) -> int:
    races = _parse_input(input_string)
    return prod(_number_of_ways_to_win(race) for race in races)


def _number_of_ways_to_win(race: Race) -> int:
    output = 0

    for hold in range(1, race.duration):
        distance = hold * (race.duration - hold)

        if distance > race.record_distance:
            output += 1

    return output


def _parse_input(input_string: str) -> Iterable[Race]:
    lines = input_string.splitlines()
    first_line_colon = lines[0].find(":")
    second_line_colon = lines[1].find(":")
    durations = [int(token) for token in lines[0][first_line_colon + 1 :].split()]
    record_distances = [int(token) for token in lines[1][second_line_colon + 1 :].split()]

    return [Race(duration, record_distance) for duration, record_distance in zip(durations, record_distances)]


EXAMPLE_INPUT = """Time:      7  15   30
Distance:  9  40  200"""

EXAMPLE_INPUT2 = """Time:      71530
Distance:  940200"""

PUZZLE_INPUT = """Time:        46     68     98     66
Distance:   358   1054   1807   1080"""

PUZZLE_INPUT2 = """Time:        46689866
Distance:   358105418071080"""


@mark.parametrize(
    ("input_string", "expected_output"),
    [(EXAMPLE_INPUT, 288), (PUZZLE_INPUT, 138915), (EXAMPLE_INPUT2, 71503), (PUZZLE_INPUT2, 27340847)],
)
def test_boat_race(input_string: str, expected_output: int) -> None:
    assert boat_race(input_string) == expected_output

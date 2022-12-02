from collections import defaultdict
from collections.abc import MutableMapping
from dataclasses import dataclass
from enum import Enum
from re import Pattern, compile

from pytest import mark


class FlightState(Enum):
    FLYING = 0
    RESTING = 1


@dataclass
class Reindeer:
    name: str
    flight_speed: int
    flight_time: int
    rest_time: int
    distance: int = 0
    state: FlightState = FlightState.FLYING
    counter: int = 0

    def advance_one_second(self) -> None:
        self.counter += 1

        if self.state == FlightState.FLYING:
            self.distance += self.flight_speed

            if self.counter == self.flight_time:
                self.state = FlightState.RESTING
                self.counter = 0
        else:
            if self.counter == self.rest_time:
                self.state = FlightState.FLYING
                self.counter = 0


def get_distance_of_fastest_reindeer(raw_input: str, num_seconds: int) -> int:
    herd = parse_input(raw_input)

    for _ in range(num_seconds):
        for reindeer in herd:
            reindeer.advance_one_second()

    return max(reindeer.distance for reindeer in herd)


def get_point_leader(raw_input: str, num_seconds: int) -> int:
    points: MutableMapping[str, int] = defaultdict(int)
    herd = parse_input(raw_input)

    for s in range(num_seconds):
        for reindeer in herd:
            reindeer.advance_one_second()

        max_distance = max(reindeer.distance for reindeer in herd)

        for reindeer in herd:
            if reindeer.distance == max_distance:
                points[reindeer.name] += 1

    return max(points.values())


def parse_input(raw_input: str) -> list[Reindeer]:
    pattern = "([A-z]+) can fly ([0-9]+) km\\/s for ([0-9]+) seconds, but then must rest for ([1-9]+) seconds."
    regex = compile(pattern)

    return [parse_input_line(regex, line) for line in raw_input.splitlines()]


def parse_input_line(regex: Pattern, line: str) -> Reindeer:
    result = regex.match(line)

    if not result:
        raise RuntimeError(f"Input contained invalid {line=}")

    name = result.group(1)
    flight_speed = int(result.group(2))
    flight_time = int(result.group(3))
    rest_time = int(result.group(4))
    return Reindeer(name, flight_speed, flight_time, rest_time)


@mark.parametrize(
    ("seconds", "expected_distance"),
    [(0, 0), (1, 14), (10, 140), (11, 140), (137, 140), (138, 154), (147, 280), (148, 280)],
)
def test_single_reindeer(seconds: int, expected_distance: int) -> None:
    reindeer = Reindeer("Comet", 14, 10, 127)
    for _ in range(seconds):
        reindeer.advance_one_second()

    assert reindeer.distance == expected_distance


EXAMPLE_INPUT = """Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."""

PUZZLE_INPUT = """Vixen can fly 19 km/s for 7 seconds, but then must rest for 124 seconds.
Rudolph can fly 3 km/s for 15 seconds, but then must rest for 28 seconds.
Donner can fly 19 km/s for 9 seconds, but then must rest for 164 seconds.
Blitzen can fly 19 km/s for 9 seconds, but then must rest for 158 seconds.
Comet can fly 13 km/s for 7 seconds, but then must rest for 82 seconds.
Cupid can fly 25 km/s for 6 seconds, but then must rest for 145 seconds.
Dasher can fly 14 km/s for 3 seconds, but then must rest for 38 seconds.
Dancer can fly 3 km/s for 16 seconds, but then must rest for 37 seconds.
Prancer can fly 25 km/s for 6 seconds, but then must rest for 143 seconds."""


@mark.parametrize(
    ("raw_input", "num_seconds", "expected_distance"),
    [
        (EXAMPLE_INPUT, 1, 16),
        (EXAMPLE_INPUT, 10, 160),
        (EXAMPLE_INPUT, 11, 176),
        (EXAMPLE_INPUT, 1000, 1120),
        (PUZZLE_INPUT, 2503, 2660),
    ],
)
def test_get_distance_of_fastest_reindeer(raw_input: str, num_seconds: int, expected_distance: int) -> None:
    assert get_distance_of_fastest_reindeer(raw_input, num_seconds) == expected_distance


@mark.parametrize(
    ("raw_input", "num_seconds", "expected_points"),
    [
        (EXAMPLE_INPUT, 1, 1),
        (EXAMPLE_INPUT, 140, 139),
        (EXAMPLE_INPUT, 1000, 689),
        (PUZZLE_INPUT, 2503, 1256),
    ],
)
def test_get_point_leader(raw_input: str, num_seconds: int, expected_points: int) -> None:
    assert get_point_leader(raw_input, num_seconds) == expected_points

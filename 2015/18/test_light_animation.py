from collections.abc import Iterable
from os.path import dirname, join

from pytest import mark

Lights = list[list[bool]]


def parse_input(raw_input: str) -> Lights:
    return [[char == "#" for char in line] for line in raw_input.splitlines()]


def update_lights(lights: Lights) -> Lights:
    output = []

    for y, row in enumerate(lights):
        output_row = []

        for x, value in enumerate(row):
            neighbours = get_neighbours(lights, x, y)
            num_neighbours_on = sum(1 if neighbour else 0 for neighbour in neighbours)
            new_value = compute_new_value(value, num_neighbours_on)
            output_row.append(new_value)

        output.append(output_row)

    return output


def get_neighbours(lights: Lights, x: int, y: int) -> Iterable[bool]:
    height = len(lights)
    width = len(lights[0])

    for neighbour_y in range(max(y - 1, 0), min(y + 2, height)):
        for neighbour_x in range(max(x - 1, 0), min(x + 2, width)):
            if neighbour_x != x or neighbour_y != y:
                yield lights[neighbour_y][neighbour_x]


def compute_new_value(current_value: bool, num_neighbours_on: int) -> bool:
    if current_value:
        return num_neighbours_on in {2, 3}
    else:
        return num_neighbours_on == 3


def stick_corners(lights: Lights) -> Lights:
    height = len(lights)
    width = len(lights[0])

    return [
        [True if x in {0, width - 1} and y in {0, height - 1} else value for x, value in enumerate(row)]
        for y, row in enumerate(lights)
    ]


EXAMPLE_INPUT = """.#.#.#
...##.
#....#
..#...
#.#..#
####.."""

PUZZLE_INPUT = open(join(dirname(__file__), "puzzle_input.txt")).read()


def test_parse_input():
    assert parse_input(EXAMPLE_INPUT) == [
        [False, True, False, True, False, True],
        [False, False, False, True, True, False],
        [True, False, False, False, False, True],
        [False, False, True, False, False, False],
        [True, False, True, False, False, True],
        [True, True, True, True, False, False],
    ]


def test_update_lights():
    actual_input = parse_input(EXAMPLE_INPUT)
    assert update_lights(actual_input) == [
        [False, False, True, True, False, False],
        [False, False, True, True, False, True],
        [False, False, False, True, True, False],
        [False, False, False, False, False, False],
        [True, False, False, False, False, False],
        [True, False, True, True, False, False],
    ]


@mark.parametrize(("raw_input", "num_steps", "num_lights_expected"), [(EXAMPLE_INPUT, 4, 4), (PUZZLE_INPUT, 100, 814)])
def test_update_lights_steps(raw_input: str, num_steps: int, num_lights_expected: int) -> None:
    lights = parse_input(raw_input)

    for _ in range(num_steps):
        lights = update_lights(lights)

    num_lights_on = sum(sum(1 if value else 0 for value in row) for row in lights)

    assert num_lights_on == num_lights_expected


@mark.parametrize(("raw_input", "num_steps", "num_lights_expected"), [(EXAMPLE_INPUT, 5, 17), (PUZZLE_INPUT, 100, 924)])
def test_update_lights_steps_with_stuck_corners(raw_input: str, num_steps: int, num_lights_expected: int) -> None:
    lights = parse_input(raw_input)
    lights = stick_corners(lights)

    for _ in range(num_steps):
        lights = update_lights(lights)
        lights = stick_corners(lights)

    num_lights_on = sum(sum(1 if value else 0 for value in row) for row in lights)

    assert num_lights_on == num_lights_expected

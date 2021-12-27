from dataclasses import dataclass
from os.path import dirname, join

from pytest import mark


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


def present_delivery(directions: str) -> int:
    current_pos = Coord(x=0, y=0)
    visited_houses = {current_pos}

    for direction in directions:
        current_pos = update_position(current_pos, direction)
        visited_houses.add(current_pos)

    return len(visited_houses)


def present_delivery_with_robot(directions: str) -> int:
    santa_pos = Coord(x=0, y=0)
    robot_pos = Coord(x=0, y=0)
    visited_houses = {santa_pos, robot_pos}

    for index, direction in enumerate(directions):
        if index % 2 == 0:
            santa_pos = update_position(santa_pos, direction)
            visited_houses.add(santa_pos)
        else:
            robot_pos = update_position(robot_pos, direction)
            visited_houses.add(robot_pos)

    return len(visited_houses)


def update_position(current_pos: Coord, direction: str) -> Coord:
    if direction == "^":
        return Coord(current_pos.x, current_pos.y - 1)
    elif direction == ">":
        return Coord(current_pos.x + 1, current_pos.y)
    elif direction == "v":
        return Coord(current_pos.x, current_pos.y + 1)
    elif direction == "<":
        return Coord(current_pos.x - 1, current_pos.y)
    else:
        raise RuntimeError(f"Unexpected {direction=}")


PUZZLE_INPUT = open(join(dirname(__file__), "puzzle_input.txt")).read()


@mark.parametrize(("directions", "expected_output"), [(">", 2), ("^>v<", 4), ("^v^v^v^v^v", 2), (PUZZLE_INPUT, 2565)])
def test_present_delivery(directions: str, expected_output: int) -> None:
    assert present_delivery(directions) == expected_output


@mark.parametrize(("directions", "expected_output"), [("^v", 3), ("^>v<", 3), ("^v^v^v^v^v", 11), (PUZZLE_INPUT, 2639)])
def test_present_delivery_with_robot(directions: str, expected_output: int) -> None:
    assert present_delivery_with_robot(directions) == expected_output

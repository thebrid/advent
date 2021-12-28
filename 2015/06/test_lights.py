from dataclasses import dataclass
from os.path import dirname, join
from typing import Callable, Mapping, Union

from pytest import fixture, raises


@dataclass
class Coord:
    x: int
    y: int


@dataclass
class Range:
    begin: Coord
    end: Coord


FixedLights = list[list[bool]]
VariableLights = list[list[int]]
Lights = Union[FixedLights, VariableLights]


def process_instruction(instruction: str, lights: Lights, command_map: Mapping[str, Callable]) -> Lights:
    command, range = parse_instruction(instruction, command_map)
    return apply_command(lights, command, range)


def apply_command(lights: Lights, command: Callable, apply_range: Range) -> Lights:
    for y in range(apply_range.begin.y, apply_range.end.y + 1):
        for x in range(apply_range.begin.x, apply_range.end.x + 1):
            lights[y][x] = command(lights[y][x])

    return lights


def turn_on_fixed(state: bool) -> bool:
    return True


def turn_on_variable(brightness: int) -> int:
    return brightness + 1


def turn_off_fixed(state: bool) -> bool:
    return False


def turn_off_variable(brightness: int) -> int:
    return max(brightness - 1, 0)


def toggle_fixed(state: bool) -> bool:
    return not state


def toggle_variable(brightness: int) -> int:
    return brightness + 2


COMMAND_MAP_WITH_FIXED_BRIGHTNESS = {"turn on ": turn_on_fixed, "turn off ": turn_off_fixed, "toggle ": toggle_fixed}
COMMAND_MAP_WITH_VARIABLE_BRIGHTNESS = {
    "turn on ": turn_on_variable,
    "turn off ": turn_off_variable,
    "toggle ": toggle_variable,
}


def parse_instruction(instruction: str, command_map: Mapping[str, Callable]) -> tuple[Callable, Range]:
    for text, callable in command_map.items():
        if instruction.startswith(text):
            return callable, parse_range(instruction[len(text) :])

    raise RuntimeError(f"Unrecognised {instruction=}")


def parse_range(text: str) -> Range:
    tokens = text.split(" through ")
    begin_tokens = tokens[0].split(",")
    end_tokens = tokens[1].split(",")

    return Range(
        begin=Coord(x=int(begin_tokens[0]), y=int(begin_tokens[1])),
        end=Coord(x=int(end_tokens[0]), y=int(end_tokens[1])),
    )


def test_turn_on_instruction_turns_on_previously_off_lights():
    instruction = "turn on 0,0 through 0,0"
    lights = [[False]]
    assert process_instruction(instruction, lights, COMMAND_MAP_WITH_FIXED_BRIGHTNESS) == [[True]]


def test_turn_on_instruction_leaves_on_lights_on():
    instruction = "turn on 0,0 through 0,0"
    lights = [[True]]
    assert process_instruction(instruction, lights, COMMAND_MAP_WITH_FIXED_BRIGHTNESS) == [[True]]


def test_toggle_instruction_turns_on_previously_off_lights():
    instruction = "toggle 0,0 through 0,0"
    lights = [[False]]
    assert process_instruction(instruction, lights, COMMAND_MAP_WITH_FIXED_BRIGHTNESS) == [[True]]


def test_toggle_instruction_turns_off_previously_on_lights():
    instruction = "toggle 0,0 through 0,0"
    lights = [[True]]
    assert process_instruction(instruction, lights, COMMAND_MAP_WITH_FIXED_BRIGHTNESS) == [[False]]


def test_turn_off_instruction_turns_off_previously_on_lights():
    instruction = "turn off 0,0 through 0,0"
    lights = [[True]]
    assert process_instruction(instruction, lights, COMMAND_MAP_WITH_FIXED_BRIGHTNESS) == [[False]]


def test_turn_off_instruction_leaves_off_lights_off():
    instruction = "turn off 0,0 through 0,0"
    lights = [[False]]
    assert process_instruction(instruction, lights, COMMAND_MAP_WITH_FIXED_BRIGHTNESS) == [[False]]


def test_instructions_only_apply_to_correct_coordinates():
    instruction = "toggle 1,1 through 2,2"
    lights = [
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False],
    ]
    assert process_instruction(instruction, lights, COMMAND_MAP_WITH_FIXED_BRIGHTNESS) == [
        [False, False, False, False],
        [False, True, True, False],
        [False, True, True, False],
        [False, False, False, False],
    ]


def test_unknown_instruction_raises():
    instruction = "something_else 0,0 through 0,0"
    lights = [[False]]

    with raises(RuntimeError):
        process_instruction(instruction, lights, COMMAND_MAP_WITH_FIXED_BRIGHTNESS)


@fixture
def puzzle_input() -> list[str]:
    return open(join(dirname(__file__), "puzzle_input.txt")).read().splitlines()


def test_apply_instructions(puzzle_input: list[str]) -> None:
    lights = [[False for _ in range(1000)] for _ in range(1000)]

    for instruction in puzzle_input:
        process_instruction(instruction, lights, COMMAND_MAP_WITH_FIXED_BRIGHTNESS)

    assert sum(sum(int(value) for value in row) for row in lights) == 569999


def test_apply_instructions_with_variable_brightness(puzzle_input: list[str]) -> None:
    lights = [[0 for _ in range(1000)] for _ in range(1000)]

    for instruction in puzzle_input:
        process_instruction(instruction, lights, COMMAND_MAP_WITH_VARIABLE_BRIGHTNESS)

    assert sum(sum(value for value in row) for row in lights) == 17836115

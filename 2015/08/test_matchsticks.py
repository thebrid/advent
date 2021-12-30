from enum import Enum
from os.path import dirname, join

from pytest import mark


class State(Enum):
    OUTSIDE_STRING = 0
    INSIDE_STRING = 1
    ESCAPE_CHAR = 2
    HEX_CHAR = 3
    HEX_ONE = 4


def process_state_escape_char(char: str) -> tuple[State, int]:
    if char == "\\" or char == '"':
        return State.INSIDE_STRING, 1
    elif char == "x":
        return State.HEX_CHAR, 0

    raise RuntimeError(f"Unexpected {char=}")


def process_state_hex_char(char: str) -> tuple[State, int]:
    return State.HEX_ONE, 0


def process_state_hex_one(char: str) -> tuple[State, int]:
    return State.INSIDE_STRING, 1


def process_state_inside_string(char: str) -> tuple[State, int]:
    if char == "\\":
        return State.ESCAPE_CHAR, 0
    elif char == '"':
        return State.OUTSIDE_STRING, 0

    return State.INSIDE_STRING, 1


def process_state_outside_string(char: str) -> tuple[State, int]:
    if char != '"':
        raise RuntimeError(f"Unexpected {char=}")

    return State.INSIDE_STRING, 0


STATE_FUNCTORS = {
    State.ESCAPE_CHAR: process_state_escape_char,
    State.HEX_CHAR: process_state_hex_char,
    State.HEX_ONE: process_state_hex_one,
    State.INSIDE_STRING: process_state_inside_string,
    State.OUTSIDE_STRING: process_state_outside_string,
}


def get_length_of_decoded_string(s: str) -> int:
    state = State.OUTSIDE_STRING
    length = 0

    for char in s:
        state, length_change = STATE_FUNCTORS[state](char)
        length += length_change

    return length


def get_length_of_encoded_string(s: str) -> int:
    return sum(get_length_of_encoded_character(c) for c in s) + 2


def get_length_of_encoded_character(c: str) -> int:
    if c in {'"', "\\"}:
        return 2
    return 1


def get_difference_of_decoded_string(raw_input: str) -> int:
    return sum(len(s) - get_length_of_decoded_string(s) for s in raw_input.splitlines())


def get_difference_of_encoded_string(raw_input: str) -> int:
    return sum(get_length_of_encoded_string(s) - len(s) for s in raw_input.splitlines())


@mark.parametrize(
    ("input_string", "expected_length"),
    [('""', 0), ('"A"', 1), ('"A\\"A"', 3), ('"abc"', 3), ('"aaa\\"aaa"', 7), ('"\\x27"', 1)],
)
def test_get_length_of_decoded_string(input_string: str, expected_length: int) -> None:
    assert get_length_of_decoded_string(input_string) == expected_length


@mark.parametrize(("input_string", "expected_length"), [('""', 6), ('"abc"', 9), ('"aaa\\"aaa"', 16), ('"\\x27"', 11)])
def test_get_length_of_encoded_string(input_string: str, expected_length: int) -> None:
    assert get_length_of_encoded_string(input_string) == expected_length


EXAMPLE_INPUT = '''""
"abc"
"aaa\\"aaa"
"\\x27"'''

PUZZLE_INPUT = open(join(dirname(__file__), "puzzle_input.txt")).read()


@mark.parametrize(("raw_input", "expected_difference"), [(EXAMPLE_INPUT, 12), (PUZZLE_INPUT, 1371)])
def test_get_difference_of_decoded_string(raw_input: str, expected_difference: int) -> None:
    assert get_difference_of_decoded_string(raw_input) == expected_difference


@mark.parametrize(("raw_input", "expected_difference"), [(EXAMPLE_INPUT, 19), (PUZZLE_INPUT, 2117)])
def test_get_difference_of_encoded_string(raw_input: str, expected_difference: int) -> None:
    assert get_difference_of_encoded_string(raw_input) == expected_difference

from json import load
from os.path import dirname, join

from pytest import mark


def json_sum(json_input: object, ignore_red: bool) -> int:
    if type(json_input) is dict:
        if ignore_red and "red" in json_input.values():
            return 0

        return sum(json_sum(item, ignore_red) for item in json_input.values())
    elif type(json_input) is int:
        return json_input
    elif type(json_input) is list:
        return sum(json_sum(item, ignore_red) for item in json_input)
    elif type(json_input) is str:
        return 0

    raise RuntimeError(f"Unexpected type {json_input=} {type(json_input)=}")


PUZZLE_INPUT = load(open(join(dirname(__file__), "puzzle_input.json")))


@mark.parametrize(
    ("json_input", "expected_sum"),
    [
        ([1, 2, 3], 6),
        ({"a": 2, "b": 4}, 6),
        ([[[3]]], 3),
        ({"a": {"b": 4}, "c": -1}, 3),
        ({"a": [-1, 1]}, 0),
        ([-1, {"a": 1}], 0),
        ([], 0),
        ({}, 0),
        (PUZZLE_INPUT, 111754),
    ],
)
def test_json_sum(json_input: object, expected_sum: int) -> None:
    assert json_sum(json_input, ignore_red=False) == expected_sum


@mark.parametrize(
    ("json_input", "expected_sum"),
    [
        ([1, 2, 3], 6),
        ([1, {"c": "red", "b": 2}, 3], 4),
        ({"d": "red", "e": [1, 2, 3, 4], "f": 5}, 0),
        ([1, "red", 5], 6),
        (PUZZLE_INPUT, 65402),
    ],
)
def test_json_sum_ignoring_red(json_input: object, expected_sum: int) -> None:
    assert json_sum(json_input, ignore_red=True) == expected_sum

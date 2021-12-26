from os.path import dirname, join

from pytest import mark


def find_floor(directions: str) -> int:
    current_floor = 0

    for direction in directions:
        if direction == "(":
            current_floor += 1
        elif direction == ")":
            current_floor -= 1

    return current_floor


def first_basement_step(directions: str) -> int | None:
    current_floor = 0

    for index, direction in enumerate(directions):
        if direction == "(":
            current_floor += 1
        elif direction == ")":
            current_floor -= 1

        if current_floor < 0:
            return index + 1

    return None


PUZZLE_INPUT = open(join(dirname(__file__), "puzzle_input.txt")).read()


@mark.parametrize(
    ("directions", "expected_output"),
    [
        ("(())", 0),
        ("()()", 0),
        ("(((", 3),
        ("(()(()(", 3),
        ("))(((((", 3),
        ("())", -1),
        ("))(", -1),
        (")))", -3),
        (")())())", -3),
        (PUZZLE_INPUT, 280),
    ],
)
def test_find_floor(directions: str, expected_output) -> None:
    assert find_floor(directions) == expected_output


@mark.parametrize(("directions", "expected_output"), [("(", None), (")", 1), ("()())", 5), (PUZZLE_INPUT, 1797)])
def test_first_basement_step(directions: str, expected_output: int) -> None:
    assert first_basement_step(directions) == expected_output

from collections import defaultdict
from os.path import dirname, join
from typing import Callable

from pytest import mark

BANNED_STRINGS = {"ab", "cd", "pq", "xy"}
VOWELS = {"a", "e", "i", "o", "u"}


def is_string_nice(s: str) -> bool:
    last_char = None
    contains_repeat = False
    vowel_count = 0
    contains_banned_string = False

    for char in s:
        contains_repeat |= char == last_char

        if char in VOWELS:
            vowel_count += 1

        if last_char is not None and f"{last_char}{char}" in BANNED_STRINGS:
            contains_banned_string = True
            break

        last_char = char

    return vowel_count >= 3 and contains_repeat and not contains_banned_string


def is_string_nice2(s: str) -> bool:
    return _contains_duplicate_pairs(s) and _contains_letter_repeat(s)


def _contains_duplicate_pairs(s) -> bool:
    pair_locations = defaultdict(list)
    for index in range(len(s) - 1):
        pair_locations[s[index : index + 2]].append(index)

        if index - pair_locations[s[index : index + 2]][0] >= 2:
            return True

    return False


def _contains_letter_repeat(s: str) -> bool:
    return any(s[index - 2] == s[index] for index in range(2, len(s)))


def count_nice_strings(raw_input: str, func: Callable[[str], bool]) -> int:
    return sum(1 if func(line) else 0 for line in raw_input.splitlines())


@mark.parametrize(
    ("s", "expected_output"),
    [
        ("ugknbfddgicrmopn", True),
        ("aaa", True),
        ("jchzalrnumimnmhp", False),
        ("haegwjzuvuyypxyu", False),
        ("dvszwmarrgswjxmb", False),
    ],
)
def test_is_string_nice(s: str, expected_output: bool) -> None:
    assert is_string_nice(s) == expected_output


@mark.parametrize(
    ("s", "expected_output"),
    [("qjhvhtzxzqqjkmpb", True), ("xxyxx", True), ("uurcxstgmygtbstg", False), ("ieodomkazucvgmuy", False)],
)
def test_is_string_nice2(s: str, expected_output: bool) -> None:
    assert is_string_nice2(s) == expected_output


PUZZLE_INPUT = open(join(dirname(__file__), "puzzle_input.txt")).read()


def test_count_nice_strings():
    assert count_nice_strings(PUZZLE_INPUT, is_string_nice) == 255


def test_count_nice_strings2():
    assert count_nice_strings(PUZZLE_INPUT, is_string_nice2) == 55

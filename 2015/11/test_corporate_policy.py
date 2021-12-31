from collections import defaultdict
from typing import Iterable

from pytest import mark


def is_valid_password(password: str) -> bool:
    return (
        has_increasing_straight(password) and not contains_forbidden_letters(password) and contains_two_pairs(password)
    )


def has_increasing_straight(password: str) -> bool:
    for i in range(len(password) - 2):
        if ord(password[i]) == ord(password[i + 1]) - 1 and ord(password[i]) == ord(password[i + 2]) - 2:
            return True

    return False


FORBIDDEN_LETTERS = {"i", "l", "o"}


def contains_forbidden_letters(password: str) -> bool:
    return any(char in FORBIDDEN_LETTERS for char in password)


def contains_two_pairs(password: str) -> bool:
    locations = defaultdict(list)

    for i in range(len(password) - 1):
        if password[i] == password[i + 1]:
            locations[password[i]].append(i)

    location_count = 0

    for pair_indices in locations.values():
        for index, pair_index in enumerate(pair_indices):
            if index == 0 or pair_index >= pair_indices[index - 1] + 2:
                location_count += 1

    return location_count >= 2


def next_valid_password(current_password: str) -> str | None:
    for candidate_password in generate_passwords(current_password):
        if is_valid_password(candidate_password):
            return candidate_password

    return None


def generate_passwords(current_password: str) -> Iterable[str]:
    codes = list(ord(char) for char in current_password)

    while True:
        increment(codes)
        yield "".join(chr(code) for code in codes)


def increment(codes: list[int]) -> None:
    for index in range(len(codes) - 1, -1, -1):
        new_code = codes[index] + 1
        if new_code <= ord("z"):
            codes[index] = new_code
            return

        codes[index] = ord("a")

    raise RuntimeError("Overflow!")


@mark.parametrize(
    ("password", "is_valid"), [("hijklmmn", False), ("abbceffg", False), ("abbcegjk", False), ("abcdffaa", True)]
)
def test_is_valid_password(password: str, is_valid: bool) -> None:
    assert is_valid_password(password) == is_valid


@mark.parametrize(
    ("current_password", "next_password"),
    [("abcdefgh", "abcdffaa"), ("ghijklmn", "ghjaabcc"), ("hxbxwxba", "hxbxxyzz"), ("hxbxxyzz", "hxcaabcc")],
)
def test_find_next_valid_password(current_password: str, next_password: str) -> None:
    assert next_valid_password(current_password) == next_password

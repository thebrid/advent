from collections.abc import Iterable

from pytest import mark


def look_and_say(s: str) -> str:
    return "".join(look_and_say_impl(s))


def look_and_say_impl(s: Iterable[str]) -> Iterable[str]:
    last_char = None
    last_char_count = 0

    for char in s:
        if char == last_char:
            last_char_count += 1
        elif last_char is None:
            last_char = char
            last_char_count = 1
        else:
            yield str(last_char_count)
            yield last_char
            last_char = char
            last_char_count = 1

    if last_char is not None:
        yield str(last_char_count)
        yield last_char


def look_and_say_iterations(s: Iterable[str], num_iterations: int) -> int:
    iterable = s

    for _ in range(num_iterations):
        iterable = look_and_say_impl(iterable)

    return len("".join(iterable))


@mark.parametrize(
    ("s", "expected_output"), [("1", "11"), ("11", "21"), ("21", "1211"), ("1211", "111221"), ("111221", "312211")]
)
def test_look_and_say(s: str, expected_output: str) -> None:
    assert look_and_say(s) == expected_output


@mark.parametrize(
    ("s", "num_iterations", "expected_length"), [("1", 5, 6), ("1113222113", 40, 252594), ("1113222113", 50, 3579328)]
)
def test_look_and_say_iterations(s: str, num_iterations: int, expected_length: int) -> None:
    assert look_and_say_iterations(s, num_iterations) == expected_length

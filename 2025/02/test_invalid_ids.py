from collections.abc import Iterable

from pytest import mark


def _parse_input(ranges: str) -> Iterable[tuple[int, int]]:
    for formatted_range in ranges.split(","):
        tokens = formatted_range.split("-")
        yield int(tokens[0]), int(tokens[1])


def _is_invalid(n: int) -> bool:
    s = str(n)
    return s[0 : len(s) // 2] == s[len(s) // 2 :]


def _is_invalid2(n: int) -> bool:
    s = str(n)
    length = len(s)

    for i in range(1, length // 2 + 1):
        tokens = [s[j : j + i] for j in range(0, length, i)]
        if all(t == tokens[0] for t in tokens):
            return True

    return False


def _invalid_ids_in_range(start: int, end: int) -> int:
    return sum(n if _is_invalid(n) else 0 for n in range(start, end + 1))


def _invalid_ids_in_range2(start: int, end: int) -> int:
    print(start, end)
    return sum(n if _is_invalid2(n) else 0 for n in range(start, end + 1))


def invalid_ids(ranges: str) -> int:
    parsed_ranges = _parse_input(ranges)

    return sum(_invalid_ids_in_range(start, end) for start, end in parsed_ranges)


def invalid_ids2(ranges: str) -> int:
    parsed_ranges = _parse_input(ranges)

    return sum(_invalid_ids_in_range2(start, end) for start, end in parsed_ranges)


EXAMPLE_INPUT = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"  # noqa: E501
PUZZLE_INPUT = "492410748-492568208,246-390,49-90,16-33,142410-276301,54304-107961,12792-24543,3434259704-3434457648,848156-886303,152-223,1303-1870,8400386-8519049,89742532-89811632,535853-567216,6608885-6724046,1985013826-1985207678,585591-731454,1-13,12067202-12233567,6533-10235,6259999-6321337,908315-972306,831-1296,406-824,769293-785465,3862-5652,26439-45395,95-136,747698990-747770821,984992-1022864,34-47,360832-469125,277865-333851,2281-3344,2841977-2953689,29330524-29523460"  # noqa: E501


@mark.parametrize(("ranges", "expected_output"), [(EXAMPLE_INPUT, 1227775554), (PUZZLE_INPUT, 12586854255)])
def test_invalid_ids(ranges: str, expected_output: int) -> None:
    assert invalid_ids(ranges) == expected_output


@mark.parametrize(("ranges", "expected_output"), [(EXAMPLE_INPUT, 4174379265), (PUZZLE_INPUT, 17298174201)])
def test_invalid_ids2(ranges: str, expected_output: int) -> None:
    assert invalid_ids2(ranges) == expected_output

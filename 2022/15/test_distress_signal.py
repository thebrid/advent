from bisect import bisect_left
from collections.abc import Iterable
from dataclasses import dataclass
from re import compile, fullmatch

from pytest import mark

REGEX = compile(
    r"Sensor at x=(?P<sensor_x>-?[0-9]+), y=(?P<sensor_y>-?[0-9]+): "
    r"closest beacon is at x=(?P<beacon_x>-?[0-9]+), y=(?P<beacon_y>-?[0-9]+)"
)


@dataclass
class Coord:
    x: int
    y: int


@dataclass
class Range:
    begin: int
    end: int


def distress_signal(input_string: str, row: int) -> int:
    sensor_beacon_pairs = _parse_input(input_string)
    beacon_x = set()
    excluded_ranges = list[Range]()

    for sensor, beacon in sensor_beacon_pairs:
        manhattan_distance = abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y)
        vertical_distance_to_row = abs(row - sensor.y)
        remaining_horizontal_distance = manhattan_distance - vertical_distance_to_row

        if remaining_horizontal_distance > 0:
            add_range(
                excluded_ranges,
                Range(sensor.x - remaining_horizontal_distance, sensor.x + remaining_horizontal_distance + 1),
            )

        if beacon.y == row:
            beacon_x.add(beacon.x)

    return sum(range.end - range.begin for range in excluded_ranges) - len(beacon_x)


def tuning_frequency(input_string: str, area_dimension: int) -> int:
    sensor_beacon_pairs = list(_parse_input(input_string))

    for row in range(area_dimension + 1):
        beacon_x = set()
        excluded_ranges = list[Range]()

        for sensor, beacon in sensor_beacon_pairs:
            manhattan_distance = abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y)
            vertical_distance_to_row = abs(row - sensor.y)
            remaining_horizontal_distance = manhattan_distance - vertical_distance_to_row

            if remaining_horizontal_distance > 0:
                add_range(
                    excluded_ranges,
                    Range(sensor.x - remaining_horizontal_distance, sensor.x + remaining_horizontal_distance + 1),
                )

            if beacon.y == row:
                beacon_x.add(beacon.x)

        gap = _find_gap(excluded_ranges, area_dimension)

        if gap is not None:
            return gap * 4000000 + row

    raise RuntimeError("No gap found")


def _find_gap(excluded_ranges: list[Range], area_dimension: int) -> int | None:
    previous_range = excluded_ranges[0]

    if previous_range.begin > 0 and previous_range.begin <= area_dimension:
        return 0

    for range in excluded_ranges[1:]:
        if 0 <= previous_range.end <= area_dimension:
            return previous_range.end

        previous_range = range

    return None


def _parse_input(input_string: str) -> Iterable[tuple[Coord, Coord]]:
    for line in input_string.split("\n"):
        yield _parse_line(line)


def _parse_line(line: str) -> tuple[Coord, Coord]:
    match = fullmatch(REGEX, line)

    if not match:
        raise RuntimeError(f"Could not parse {line=}")

    beacon_x = int(match.group("beacon_x"))
    beacon_y = int(match.group("beacon_y"))
    sensor_x = int(match.group("sensor_x"))
    sensor_y = int(match.group("sensor_y"))

    return Coord(sensor_x, sensor_y), Coord(beacon_x, beacon_y)


def add_range(ranges: list[Range], new_range: Range) -> None:
    insertion_point = bisect_left(ranges, new_range.begin, key=lambda range: range.begin)
    ranges.insert(insertion_point, new_range)

    check = insertion_point - 1

    while check >= 0:
        if ranges[insertion_point].begin <= ranges[check].end:
            ranges[insertion_point].begin = min(ranges[insertion_point].begin, ranges[check].begin)
            ranges[insertion_point].end = max(ranges[insertion_point].end, ranges[check].end)
            ranges.pop(check)
            insertion_point -= 1

        check -= 1

    check = insertion_point + 1

    while check < len(ranges):
        if ranges[insertion_point].end >= ranges[check].begin:
            ranges[insertion_point].end = max(ranges[insertion_point].end, ranges[check].end)
            ranges.pop(check)
        else:
            check += 1


EXAMPLE_INPUT = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

PUZZLE_INPUT = """Sensor at x=1638847, y=3775370: closest beacon is at x=2498385, y=3565515
Sensor at x=3654046, y=17188: closest beacon is at x=3628729, y=113719
Sensor at x=3255262, y=2496809: closest beacon is at x=3266439, y=2494761
Sensor at x=3743681, y=1144821: closest beacon is at x=3628729, y=113719
Sensor at x=801506, y=2605771: closest beacon is at x=1043356, y=2000000
Sensor at x=2933878, y=5850: closest beacon is at x=3628729, y=113719
Sensor at x=3833210, y=12449: closest beacon is at x=3628729, y=113719
Sensor at x=2604874, y=3991135: closest beacon is at x=2498385, y=3565515
Sensor at x=1287765, y=1415912: closest beacon is at x=1043356, y=2000000
Sensor at x=3111474, y=3680987: closest beacon is at x=2498385, y=3565515
Sensor at x=2823460, y=1679092: closest beacon is at x=3212538, y=2537816
Sensor at x=580633, y=1973060: closest beacon is at x=1043356, y=2000000
Sensor at x=3983949, y=236589: closest beacon is at x=3628729, y=113719
Sensor at x=3312433, y=246388: closest beacon is at x=3628729, y=113719
Sensor at x=505, y=67828: closest beacon is at x=-645204, y=289136
Sensor at x=1566406, y=647261: closest beacon is at x=1043356, y=2000000
Sensor at x=2210221, y=2960790: closest beacon is at x=2498385, y=3565515
Sensor at x=3538385, y=1990300: closest beacon is at x=3266439, y=2494761
Sensor at x=3780372, y=2801075: closest beacon is at x=3266439, y=2494761
Sensor at x=312110, y=1285740: closest beacon is at x=1043356, y=2000000
Sensor at x=51945, y=2855778: closest beacon is at x=-32922, y=3577599
Sensor at x=1387635, y=2875487: closest beacon is at x=1043356, y=2000000
Sensor at x=82486, y=3631563: closest beacon is at x=-32922, y=3577599
Sensor at x=3689149, y=3669721: closest beacon is at x=3481800, y=4169166
Sensor at x=2085975, y=2190591: closest beacon is at x=1043356, y=2000000
Sensor at x=712588, y=3677889: closest beacon is at x=-32922, y=3577599
Sensor at x=22095, y=3888893: closest beacon is at x=-32922, y=3577599
Sensor at x=3248397, y=2952817: closest beacon is at x=3212538, y=2537816"""


@mark.parametrize(
    ("start_ranges", "new_range", "expected_ranges"),
    [
        ([], Range(0, 10), [Range(0, 10)]),
        ([Range(0, 9)], Range(10, 19), [Range(0, 9), Range(10, 19)]),
        ([Range(10, 19)], Range(0, 9), [Range(0, 9), Range(10, 19)]),
        ([Range(2, 3), Range(4, 5)], Range(0, 1), [Range(0, 1), Range(2, 3), Range(4, 5)]),
        ([Range(0, 1), Range(4, 5)], Range(2, 3), [Range(0, 1), Range(2, 3), Range(4, 5)]),
        ([Range(0, 1), Range(2, 3)], Range(4, 5), [Range(0, 1), Range(2, 3), Range(4, 5)]),
        ([Range(10, 20)], Range(0, 10), [Range(0, 20)]),
        ([Range(0, 10)], Range(10, 20), [Range(0, 20)]),
        ([Range(10, 20), Range(30, 40)], Range(0, 10), [Range(0, 20), Range(30, 40)]),
        ([Range(10, 20), Range(30, 40)], Range(20, 30), [Range(10, 40)]),
        ([Range(10, 20), Range(30, 40)], Range(40, 50), [Range(10, 20), Range(30, 50)]),
        ([Range(10, 20), Range(30, 40)], Range(0, 50), [Range(0, 50)]),
        ([Range(10, 20), Range(30, 40)], Range(5, 15), [Range(5, 20), Range(30, 40)]),
        ([Range(10, 20), Range(30, 40)], Range(15, 25), [Range(10, 25), Range(30, 40)]),
        ([Range(10, 20), Range(30, 40)], Range(25, 35), [Range(10, 20), Range(25, 40)]),
        ([Range(10, 20), Range(30, 40)], Range(35, 45), [Range(10, 20), Range(30, 45)]),
        ([Range(10, 20), Range(30, 40)], Range(5, 25), [Range(5, 25), Range(30, 40)]),
        ([Range(10, 20), Range(30, 40)], Range(25, 45), [Range(10, 20), Range(25, 45)]),
        ([Range(begin=117910, end=4305093)], Range(begin=3761200, end=3799545), [Range(begin=117910, end=4305093)]),
    ],
)
def test_add_range(start_ranges: list[Range], new_range: Range, expected_ranges: list[Range]) -> None:
    add_range(start_ranges, new_range)
    assert start_ranges == expected_ranges


@mark.parametrize(
    ("input_string", "row", "expected_output"),
    [
        (EXAMPLE_INPUT, 10, 26),
        (PUZZLE_INPUT, 2000000, 4724228),
    ],
)
def test_distress_signal(input_string: str, row: int, expected_output: int) -> None:
    assert distress_signal(input_string, row) == expected_output


@mark.parametrize(
    ("input_string", "area_dimension", "expected_output"),
    [
        (EXAMPLE_INPUT, 20, 56000011),
        (PUZZLE_INPUT, 4000000, 13622251246513),
    ],
)
def test_tuning_frequency(input_string: str, area_dimension: int, expected_output: int) -> None:
    assert tuning_frequency(input_string, area_dimension) == expected_output

# flake8: noqa: E501
from dataclasses import dataclass
from enum import IntEnum
from itertools import chain

from pytest import mark


@dataclass(frozen=True)
class Point:
    x: int
    y: int


class Direction(IntEnum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


@dataclass(frozen=True)
class PointDirection:
    point: Point
    direction: Direction


def energised_tiles(input_string: str) -> int:
    mirrors = list(input_string.splitlines())
    return _energise_tiles(mirrors, PointDirection(point=Point(x=0, y=0), direction=Direction.RIGHT))


def energised_tiles_max(input_string: str) -> int:
    mirrors = list(input_string.splitlines())
    height = len(mirrors)
    width = len(mirrors[0])
    starting_points = (
        [PointDirection(point=Point(x=width - 1, y=y), direction=Direction.LEFT) for y in range(height)]
        + [PointDirection(point=Point(x=0, y=y), direction=Direction.RIGHT) for y in range(height)]
        + [PointDirection(point=Point(x=x, y=height - 1), direction=Direction.UP) for x in range(width)]
        + [PointDirection(point=Point(x=x, y=0), direction=Direction.DOWN) for x in range(width)]
    )

    return max(_energise_tiles(mirrors, starting_point) for starting_point in starting_points)


def _energise_tiles(mirrors: list[str], starting_point: PointDirection) -> int:
    energised = [[False for col in row] for row in mirrors]
    stack = [starting_point]
    seen = set[PointDirection]()
    height = len(mirrors)
    width = len(mirrors[0])

    while stack:
        point_direction = stack.pop()
        point, direction = point_direction.point, point_direction.direction

        if point.x < 0 or point.x >= width or point.y < 0 or point.y >= height:
            continue

        current_cell = mirrors[point.y][point.x]
        energised[point.y][point.x] = True

        match direction:
            case Direction.LEFT:
                _process_left(current_cell, point, direction, stack, seen)
            case Direction.RIGHT:
                _process_right(current_cell, point, direction, stack, seen)
            case Direction.UP:
                _process_up(current_cell, point, direction, stack, seen)
            case Direction.DOWN:
                _process_down(current_cell, point, direction, stack, seen)
            case _:
                raise RuntimeError(f"Unexpected {point_direction=}")

    return sum(chain.from_iterable(energised))


def _process_down(
    current_cell: str, point: Point, direction: Direction, stack: list[PointDirection], seen: set[PointDirection]
) -> None:
    match current_cell:
        case "." | "|":
            _push(stack, seen, PointDirection(point=Point(x=point.x, y=point.y + 1), direction=direction))
        case "-":
            _push(stack, seen, PointDirection(point=Point(x=point.x - 1, y=point.y), direction=Direction.LEFT))
            _push(stack, seen, PointDirection(point=Point(x=point.x + 1, y=point.y), direction=Direction.RIGHT))
        case "/":
            _push(stack, seen, PointDirection(point=Point(x=point.x - 1, y=point.y), direction=Direction.LEFT))
        case "\\":
            _push(stack, seen, PointDirection(point=Point(x=point.x + 1, y=point.y), direction=Direction.RIGHT))
        case _:
            raise RuntimeError(f"Unexpected {point=}, {direction=}")


def _process_left(
    current_cell: str, point: Point, direction: Direction, stack: list[PointDirection], seen: set[PointDirection]
) -> None:
    match current_cell:
        case "." | "-":
            _push(stack, seen, PointDirection(point=Point(x=point.x - 1, y=point.y), direction=direction))
        case "|":
            _push(stack, seen, PointDirection(point=Point(x=point.x, y=point.y - 1), direction=Direction.UP))
            _push(stack, seen, PointDirection(point=Point(x=point.x, y=point.y + 1), direction=Direction.DOWN))
        case "/":
            _push(stack, seen, PointDirection(point=Point(x=point.x, y=point.y + 1), direction=Direction.DOWN))
        case "\\":
            _push(stack, seen, PointDirection(point=Point(x=point.x, y=point.y - 1), direction=Direction.UP))
        case _:
            raise RuntimeError(f"Unexpected {point=}, {direction=}")


def _process_right(
    current_cell: str, point: Point, direction: Direction, stack: list[PointDirection], seen: set[PointDirection]
) -> None:
    match current_cell:
        case "." | "-":
            _push(stack, seen, PointDirection(point=Point(x=point.x + 1, y=point.y), direction=direction))
        case "|":
            _push(stack, seen, PointDirection(point=Point(x=point.x, y=point.y - 1), direction=Direction.UP))
            _push(stack, seen, PointDirection(point=Point(x=point.x, y=point.y + 1), direction=Direction.DOWN))
        case "/":
            _push(stack, seen, PointDirection(point=Point(x=point.x, y=point.y - 1), direction=Direction.UP))
        case "\\":
            _push(stack, seen, PointDirection(point=Point(x=point.x, y=point.y + 1), direction=Direction.DOWN))
        case _:
            raise RuntimeError(f"Unexpected {point=}, {direction=}")


def _process_up(
    current_cell: str, point: Point, direction: Direction, stack: list[PointDirection], seen: set[PointDirection]
) -> None:
    match current_cell:
        case "." | "|":
            _push(stack, seen, PointDirection(point=Point(x=point.x, y=point.y - 1), direction=direction))
        case "-":
            _push(stack, seen, PointDirection(point=Point(x=point.x - 1, y=point.y), direction=Direction.LEFT))
            _push(stack, seen, PointDirection(point=Point(x=point.x + 1, y=point.y), direction=Direction.RIGHT))
        case "/":
            _push(stack, seen, PointDirection(point=Point(x=point.x + 1, y=point.y), direction=Direction.RIGHT))
        case "\\":
            _push(stack, seen, PointDirection(point=Point(x=point.x - 1, y=point.y), direction=Direction.LEFT))
        case _:
            raise RuntimeError(f"Unexpected {point=}, {direction=}")


def _push(stack: list[PointDirection], seen: set[PointDirection], new_item: PointDirection) -> None:
    if new_item in seen:
        return

    stack.append(new_item)
    seen.add(new_item)


EXAMPLE_INPUT = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""

PUZZLE_INPUT = r"""\................\......-.........................../..............|.\..-.................-......../..........
..\................\...........|.|../......\......../../...........|.......\....../.......\....../............
|......|./......../..........|\.......|/..|...............................|...............|...................
...................\.-.............................../.......\.....\..............././.......\...........|....
................\......................|...|\............../........./...................\......./......./....
-......\/..\/../...............................................\....\........\...............-....\......-....
....\......-......................-..|...........................-.|...-..........\................./.........
.......|..........\....|/................................/........................-/.\...-/................../
..\...-..../......................\./..........|-/......\...............|...|.............................|...
\................................\....|...........|......................|..........|.............../........-
|..../......\.....\................../............../..\.....|..............................................-.
.\...........\.-....|.....-..|......|..............\.....\...-......./..................../\....|.../\........
...........|.......-..\...............\................................../...........................\........
.........-.................../...................../.-../.........|...\..........-..........\........|........
../...../../.|......-.....|\...../.......\......-.........-............./....................../..............
.-....../.............-...../...........\........-.......\...............-|......\.....|....\.................
......................./..............................\.....\...-................................./...........
./.....\.........\-..-...-..\...................\......./....|.|.-..........|......./.........................
.................................-...............\...../....../..\..-......................|..................
...\.................\...\............\-.....................\...........-..............................-.....
.....-....-|......\..../...........-.................../............-.................../............-....|...
.....-..\.....................-............/..../..........-.../..........................-.......\...........
..|..........................-................|-..-..............|....................../.....|......|........
.\...........................\......//.....-..-............/.....................................././........-
....../...\.......................\/.\.../.........\......................................-.....\......./.....
.....|........../..................................../....-....................|....\........-.........../../.
.............|....\...................................|.....|./..........|...........................-.|......
......................................./........./..................-.......|...............\..../....|.......
.../....//.\...............\.....|..|...-......|.......-|.../.-....-..\........\...../.....|..................
............./...................................|.............../.|...................-..........-...........
...../....|.................................................|........\...........................-....../.|...
...\.....\.....................|/.-....\.....|.|...--...../...\......................../.........|............
../...................../|................/......\...|..\|............-../........-............./......./.....
...............|...................\-.................\......-/.|......./.......-....../........../....-......
.-/-.....|...|......../...\.|........-....................\..-.......-.............................|.-/.\.....
................-......|.....\...--................./....-..|.../............./.....\........../.........|....
.................\...\...........|........................\...............././........|\......./.............-
......\....\..................................././...|..|...............-.....||..............................
..../|.\-............./././....../-./.-..........-...............-..\...........|................../..........
..........\.-....|....\.|...............\.......\.........\./.....|...|........|.........-.................|-.
.|.\......................\......-....-....-...............\.....-.\............./|-...-./....../.......-.....
.........\......../.|.-.../.-...............-..-.......|......\...\..|..................................../...
/./.......|.\.....................................-...-.|......-/...........-..................../.........\..
...-..\........-................\...|.|....../...............|................................................
.....................................-......\...-.../..\....|..................\.........................-....
-........|...........-...........|//................|.....-..........|..-....../\..|../..-....\..\....../.....
.|............../.\...................................\..|....|..\..............|................/...-.../-...
........./.......|.|.................................|\....\|........\........|........|.....................\
..\....../....|......../.......\|.............\........................./............/..../...............-...
.....-........-............/../....-...............-.../......../../..-...........\.....\.......-...-.......-.
........|...../-....-......\.............................-..|\.....\.....\-..............\.......|............
......................................../.......-..\..........\.............|....-.....\/........./.|.....|...
..............-...................-.-...-............../...../.....\./........./.-....................-.......
................|........../\..../......................-.......-............\.|..|......../.........\-.......
........|.........\..........................................-....||..-..\.................-....../..-.......\
.....\.............../..\./.........\|.\.....-|..-..|...../.............../.........-.........................
...|......................//......./..........-...................\......|...../......................|..|....
....\..................|..............\........\........../..-.......-...-|...\../...../........-........./...
...|\.|.......\...........\.-.................|.........\/-...............//.......\................-./......|
.........................-/...-./........./.\.|.......\...\.........\....................\.....-....-.........
......\..\....../.\........./..........-......./.-.............................\\.............................
....................../......\|../....................-.................../..............-..\|.../............
...........\.......|.|.......................|.....................\../........../.-.........|................
...................../.||..........-..../.....-.................|\............................................
..\...\.....-./..........|......-...../.....................................................|................\
....................-.\............|../..............|..\\...........|.....|....-../..........-.....-.........
............................./...............-.........................\...\.|...\.............|...-...|......
.............|.............................|...................|...................\.................../...../
...\.....\.....................-............................/..........|....|..\...........|.|................
........./.......-.\./........................../...........................................|../....../|..\...
....../.........................\...../..-...\................/...-........\....../../......|.................
......./.-.../..-..........|......................................-....\-/.-...........|....-..\...........-..
.....-...........||\...|.......|.................\........../-.............../................-...............
|.-.............\............\.....-|...././..................................-|........-/..........-.....|...
\...................\........./.\...|..........\.|......-....-.-.........\...............|.../-.........\.....
.........../...........|.........|........................|.......................|..-.......................|
..|..................-......-..................-..............................\\............-....|............
..........|..........\......................................\...................-..................|..........
...../.........|.......................................\..././...|\................/...................|......
........\.|....................\\......|..............................\....../.-/...\.......................-.
...........\.............|....\..|......../.....././|..../........\.....|.................\.........|...-.....
.....................\......./\......|............../...........-..........\..................\\...........\..
................................................\.../.....................-...../\|............\-.............
...........\...............-........\................\................./...|....\.....................\...../.
......\........|.....-....................\../..............-...............-..............-..................
.....-............|....................\......\..|.....././...../\.....|...\...............................-.-
........././......-.-..../....|..|../..................../...-......................-.......................|.
.................................//....|............-........../.../.......................\......-...........
................../................|...................................\......./...-............./............
..|.............../.....-................-..|-.........../.....................\/.........\.../.........|.....
.........................../|.../....-..\-...../................./..........................|...............\.
.....|.........../..\........../......./........-..............|............|......................-..........
....|......................................-..|.-../........................-..............\.........-........
.-......-....................-.................././.........................-...|-......................|.....
...-......./........../...........................-........\.........|......-...........-.-...................
..........-.|.|.....\..-..-...\-..../.................|..|..-.......\..................|...|.......-..........
\...........-|....-..........................\................................|.......|...\.......\-........./
./........./-.-............\...-\.-.......................................\-.......................\..........
........|..........\\.....\.-.../............-................|.............-.-..-.....\.......-.....\-.......
...................\.......|...../.-...............\.../......../................../............\...|.........
..\..........|........-.-.......|...../..../....-...........|............|................\/../.........../...
...............\..|./............................................................/............/...............
..\........|/.|......|.............\.............\.....................|.....\..........|......|..............
.............-......|......|\....................\...|..........\\.........|.|....../..../..........\.......\.
../..|..................-................................................//........|..../-..-/..../.\.........
..\............./..........-..|......./-............../....|...............|.....................|.....--\....
....-|.\..|....|............./..........\-.......|........|....|..-................................-./..\\...\
....|..\.......................\......./.-............................||....-...................\......./.....
.|-.......................-...........|..........\.../.......\......\....................-\./.................
...................................................|.....................|...................................."""


@mark.parametrize(("input_string", "expected_output"), [(EXAMPLE_INPUT, 46), (PUZZLE_INPUT, 7111)])
def test_energised_tiles(input_string: str, expected_output: int) -> None:
    assert energised_tiles(input_string) == expected_output


@mark.parametrize(("input_string", "expected_output"), [(EXAMPLE_INPUT, 51), (PUZZLE_INPUT, 7831)])
def test_energised_tiles_max(input_string: str, expected_output: int) -> None:
    assert energised_tiles_max(input_string) == expected_output

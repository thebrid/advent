# flake8: noqa: E501
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum

from pytest import mark


@dataclass(eq=True, frozen=True)
class Coord:
    x: int
    y: int


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class ExitCondition(Enum):
    OUT_OF_BOUNDS = 0
    LOOPED = 1


Map = list[list[bool]]


def _compute_next(coord: Coord, direction: Direction) -> Coord:
    match direction:
        case Direction.NORTH:
            return Coord(x=coord.x, y=coord.y - 1)
        case Direction.EAST:
            return Coord(x=coord.x + 1, y=coord.y)
        case Direction.SOUTH:
            return Coord(x=coord.x, y=coord.y + 1)
        case Direction.WEST:
            return Coord(x=coord.x - 1, y=coord.y)


def _is_obstacle(map: Map, coord: Coord) -> bool:
    return 0 <= coord.x < len(map[0]) and 0 <= coord.y < len(map) and map[coord.y][coord.x]


def _parse_input(input_str: str) -> tuple[Map, Coord]:
    lines = input_str.splitlines()
    coord = next(Coord(x=x, y=y) for y, row in enumerate(lines) for x, char in enumerate(row) if char == "^")

    return [[char == "#" for char in row] for row in lines], coord


def _turn_right(direction: Direction) -> Direction:
    match direction:
        case Direction.NORTH:
            return Direction.EAST
        case Direction.EAST:
            return Direction.SOUTH
        case Direction.SOUTH:
            return Direction.WEST
        case Direction.WEST:
            return Direction.NORTH


def _compute_visited(map: Map, coord: Coord) -> tuple[set[Coord], ExitCondition]:
    direction = Direction.NORTH
    visited = set[tuple[Coord, Direction]]()

    while 0 <= coord.x < len(map[0]) and 0 <= coord.y < len(map):
        if (coord, direction) in visited:
            return {coord for coord, _ in visited}, ExitCondition.LOOPED

        visited.add((coord, direction))
        potential_next = _compute_next(coord, direction)
        if _is_obstacle(map, potential_next):
            direction = _turn_right(direction)
        else:
            coord = potential_next

    return {coord for coord, _ in visited}, ExitCondition.OUT_OF_BOUNDS


def guard_path(input_str: str) -> int:
    map, coord = _parse_input(input_str)
    visited, _ = _compute_visited(map, coord)
    return len(visited)


def guard_path_obstacles(input_str: str) -> int:
    map, coord = _parse_input(input_str)
    initial_visited, _ = _compute_visited(map, coord)
    count = 0

    for obstacle_coord in initial_visited:
        new_map = deepcopy(map)
        new_map[obstacle_coord.y][obstacle_coord.x] = True
        _, exit_condition = _compute_visited(new_map, coord)

        if exit_condition == ExitCondition.LOOPED:
            count += 1

    return count


EXAMPLE_INPUT = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

PUZZLE_INPUT = """.........................#...........#.#...#...............#..............##.....................#...........#..#.........#.......
.....................#.................#.......#.........................#...........#.#.......#..................................
.........#...........#........#.........#.........#...........#........................................#.........................#
.......#.........................#...........................#.............#......................................................
..................#................##...............#.#.....................##............#.......................................
......#...#................#..................................................................#....#.#............................
.......##................#........#..#.......#......................................#........#............#......###..........#...
.....................#....................................................#...........#..#...#..........................#.........
...........#....#...........................#.#...............#..#....................................#..............#......#.....
.....#........##...............#.......#..#..............................................#..........................#.............
.#.........#.#...........................#..........................#......................#...........#........#.................
.................................................................#..#.#.......#..#................................................
...............................................#.......#...................#....................#.................................
.......#......#......#......................#...............................#.....##........#...........#......#..................
........................................................................................................#.....#.#.................
..#...............................#.#..................................#.............#............................................
..............#..........................................#.....#.....#..........................#....#.........#..................
...................................#........................................#................#...........##.....#....#............
.#.....................................#.......#........................#...................##............#.......................
.#..................#...........#...........................................................................................#.....
........................#...................................................##.................................#..#..........##...
........#............................#.......#...........................#.#...#...................................#.....#........
...............................#............#.....#......................#.......#...#........................#...................
.........#.............#.................................................#.......................................#....#...........
...................................................................#...#.................................#...................#....
...#.....................#...#...............#..................................................#...#...#.........................
...................#........#....#....#..#..#...................#.........#..................#..#....#.......#.#.................#
..............................#........................................#......#.....#..............##................#............
............#..#.............#.......#........................................................##........#.....#...................
.....#.............................................................#...#.#.#.............................#..#.#...........#.......
.......#....#............................................#.................................#...................................#..
..#.................#.......#..........................#........................................#...............#..............#..
....#.#...................#............................#..#.......................................................................
.......................#...............#..............#......#......................#.....................#..............#........
.#..........#.......................................................................#....................................#........
.#.......#..................................................................#.....................................................
..................................................#.............#.............................................#................#.#
.......................#......#....#................#......................................................#.......#.........#....
..........................#.#........................................................#......#................................#....
....................................................................#...............................#.............................
..#...........#..............................#..#....#............................#...............##..............#...#...#...#..#
...................................#................................................................#....#...................#....
..#....#........#..##....#........................#...#...................................#.......................................
...................#................................................................................................#.............
.......#........#................#...#.......................................................................#....................
..............#....................#..........................##.........#.....................................#..................
.........................................................................#.................#........................#.............
.............................#..........#.......................................................#......................#..........
............###....................................................................#.......................#......................
........#........#...........#.............................#....................#..........#.........................#.#.....#....
.........................................................................................................#..#.....................
#.#.....#..........................................................#.....................#........................................
........##..........#....................................................#..#........#.......#........#................#..........
.............................................#..........................#.........#........................#......................
...........................##.............#........................#.#........................#..#................#.....#........#
#...#..............................................#........#...................................................#.................
.............#................#............................#............#.........................................................
#..........................#............#.....................#.....#.................#......#...##...#.............#.#...........
.....................#...#..#....#...................................#....................#..............#........#...............
.......................#.................#...........#....#.......#...........................................#..#................
.........#...........#.#.........#.........................#.....#................................................................
....................#........#...................................................................#............#..#.#.#............
..........#.......................#.......................#.......................................................................
......................................#......#............................#..............................................#........
.....................#...#.................#.............................#....#...................................................
..............##...................................................................#......................................##......
.....#....#...............................................#.......#.##........#.#.............#...............#...................
....................................#......................#........#.......................................................#.....
.....#.........................................#.....................#.............#.................#..................#.........
................................#.........#..#............................................#.........................#.............
....#.#.....................#......#...................................#..........................................#..#.....#...#..
.........##.......................#..........................................#.........................#...##.....................
...............................................................#................................................................#.
............#.........................................##.......................................#..................................
.............................#..............................#..................#.........#.....#..................................
..........................................................#...#.....#..................#................................#.........
......#...................#.........................................................................................#.............
#...............................#...........................#.....................................................................
.......#........#.................................................#.......................................................#.......
.#......................................................#..............#..................................#...........#...........
.............#..#.#.......................#..........#......#.##.........................................................#..#.....
.......#...............#........#......................................................................#..#...........#...........
............#.........................................#................................................#...................#......
............#...........................................#.#.......#....................................#..........................
...........................................#.........................................................#..............#.............
..................#..#....................................................#..................#....................................
..#........................#........#.............................................................................................
.............#........#......................#.......................................#...#....#............................#......
............#.......#.............#...#...........#.#.................................#.................##........................
.....................................................................................#.........#.......................#.....#....
.................#................................#..#....#......#..........................................#.....#...............
..#...............................#........................................................#.......#...#............#.............
#.........#..#..#.....................................#....................................#................#.................#...
.......................#..#...#............................................................................#..#.....#.......##....
..........#............#.......................#.........................^......#.#...................................#...........
...##........................##..........#..........#.................#...............#...........#.....##........................
..............#............#..........................#....#...........#......#......#......................#.....................
......#.....#....................................................#............#.#......................................#..........
......#.............................#......................#...............................#........#.............................
.#..........#.............................................#.............................................#.........................
...............................##.................................................................................................
.....................#................................................#...............#............#...............#.....#.....#..
..................#...........................................................................#...........#...................#...
##..............................#.#...#.#...............................#...........#.#...................#.......................
......................#.........#...................................#.................#...........................................
.......................#............................................................................#.........##...........#......
.....................................................................#.......#.....#.......................................#......
#....................................#........#.#.................................................................##.....#........
..............#..............................#......#..........###.........#................#..............#..................#...
..................................#..............................#.................##.............................#...#...........
...............#......#........................#....#........#............#.........#..........#..............#......#............
...#...........#........#...#...........................#.............#.....................................#.....................
..............###............#...........................................................#.............#.........##..#............
............#................................................#.......#..................#....#....................................
.........#.#...#.....#...........................#.....##......#.....................#..#........#......#.........................
.#....#.......#.......................#.................................................................#.......#..............#..
...................#................................................................#.............#...#...........#.........#.....
.......#.#.......#.......................#....#.....#...............#...#.....#...........................................#.......
.......#........#...........................................#...........#.........................#....#.......#..................
..................................#.#.................#.#............................................#...........#....#...........
....##......#.............#...................................#...#.........#...........................#......#..................
.........................#......#....#...#........................................................................................
...#...............#............................................................................#...........................#.....
....##.#..............................................#............#................#................................#......#.....
.........#...........................................#...#.......##..............................#................................
..................#..........#......#.......#......................................#........#...............#......#...........##.
........................................#......#..........#......................................................................#
..............#...#...................#.....#..........................................................#..............#......#....
...#........#........................#...#................#........#.............................##..........................#....
............#............................#.#........................#.................................#..........................#"""


@mark.parametrize(("input_str", "expected_output"), [(EXAMPLE_INPUT, 41), (PUZZLE_INPUT, 5242)])
def test_guard_path(input_str: str, expected_output: int) -> None:
    assert guard_path(input_str) == expected_output


@mark.parametrize(("input_str", "expected_output"), [(EXAMPLE_INPUT, 6), (PUZZLE_INPUT, 1424)])
def test_guard_path_obstacles(input_str: str, expected_output: int) -> None:
    assert guard_path_obstacles(input_str) == expected_output

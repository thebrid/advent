# flake8: noqa: E501
from dataclasses import dataclass

from pytest import mark


@dataclass
class Galaxy:
    x: int
    y: int


def cosmic_expansion(input_string: str, empty_space_multiplier: int) -> int:
    cosmos = [[char == "#" for char in line] for line in input_string.splitlines()]
    rows_to_expand, cols_to_expand = _rows_cols_to_expand(cosmos)
    galaxies = _find_galaxies(cosmos)
    return sum(
        _galaxy_distance(galaxies[index1], galaxies[index2], rows_to_expand, cols_to_expand, empty_space_multiplier)
        for index1 in range(len(galaxies) - 1)
        for index2 in range(index1 + 1, len(galaxies))
    )


def _rows_cols_to_expand(cosmos: list[list[bool]]) -> tuple[set[int], set[int]]:
    rows_to_expand = {index for index, row in enumerate(cosmos) if not any(row)}
    cols_to_expand = {index for index, _ in enumerate(cosmos[0]) if not any(row[index] for row in cosmos)}

    return rows_to_expand, cols_to_expand


def _find_galaxies(cosmos: list[list[bool]]) -> list[Galaxy]:
    return [Galaxy(x, y) for y, row in enumerate(cosmos) for x, is_galaxy in enumerate(row) if is_galaxy]


def _galaxy_distance(
    galaxy1: Galaxy, galaxy2: Galaxy, rows_to_expand: set[int], cols_to_expand: set[int], empty_space_multiplier: int
) -> int:
    min_x = min(galaxy1.x, galaxy2.x)
    max_x = max(galaxy1.x, galaxy2.x)
    num_extra_cols = len([x for x in cols_to_expand if x >= min_x and x <= max_x])

    min_y = min(galaxy1.y, galaxy2.y)
    max_y = max(galaxy1.y, galaxy2.y)
    num_extra_rows = len([y for y in rows_to_expand if y >= min_y and y <= max_y])

    return (
        abs(galaxy2.x - galaxy1.x)
        + abs(galaxy2.y - galaxy1.y)
        + (num_extra_cols + num_extra_rows) * (empty_space_multiplier - 1)
    )


EXAMPLE_INPUT = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

PUZZLE_INPUT = """..................................................................................................#..................#......................
............#...............................................#.........#........................................#............................
........................#................#.........#....................................................#......................#.......#....
....#............................................................#.............#............................................................
...............................................#....................................................#.......................................
...........................#..........................#.....................................................................................
..................................#...................................................................................#............#........
...................#.....................................................#....................................................#.........#...
.......#.................................#.......#...........#...............................#.............#.....#..........................
............................................................................................................................................
....................................................................#.........#........#....................................................
.#........#.....#.......#..............................................................................#.........................#..........
............................................#...........................................................................#...................
.......................................#.......................#............................................................................
.......#....................#............................#......................................................#...........................
.............#..............................................................#.....#......................#.................#................
...........................................................................................#................................................
.........................#............................#.....#...............................................................................
...................................#...................................#....................................................................
........................................................................................#............................#................#.....
..............#......#........#.........#.........................#................#........................................................
....#...........................................................................................#........................#..................
............................................................................................................................................
............................................................#...............#...........................#........................#..........
...................................................#.............................#.................#........................................
..#......................................................................................................................................#..
...................#....................#..............................#....................#...................#.........#.................
.......................................................#....................................................................................
......#.............................#..............................................#........................................................
...........................................................................#....................#.........#.................................
....................................................................................................................#.......................
#............................#............................................................#...................................#.......#.....
...................................................#............#...........................................................................
........................#................#........................................................#......................#..................
.......#.......................................#.................................................................#..........................
...........................................................#...............................................#................................
..#.................................#................#.......................................................................#..............
.............#....................................................#.........................................................................
.........................................................................#.........#.....#..........................#...............#.......
....................#.......#..................................................................#............................................
..................................#............#...............#............................................................................
.#.......#.............................#....................................#...............................................................
.........................#...........................#.............#................................#..........#.........#..................
.....#.........................#............................................................................................................
...............#............................................#...........#...................................................................
....................................#............................................#.....#.................#..........#........#..............
............................................................................................................................................
.#................#.................................................................................................................#.......
.........................................#..............#......................................#.....#......................................
.....#.....#...............#................................................................................................................
.................................#.........................................................................#.............#.......#..........
.............................................................................#.........................................................#....
.......................................#.......................#............................................................................
.................#.................................#.....#..........#.....................#.....................#...........................
............#..................................................................................................................#............
#...................................#.......................................................................................................
........#..............#..............................#..................................................................#..................
............................................#..............#................#......................................#........................
............................................................................................................................................
...................#......#.......................#..............#..........................................................#.....#........#
................................#............................................................#..............................................
......#...................................#.......................................#...............#.........................................
.....................................#........................#.......#......................................#.................#............
...........#...........#...............................#.............................................................................#......
.#...........................................#.........................................................................#....................
............................................................................................................................................
..................................................................#...............................................#.........................
..................................................................................#.......#................#................#...............
.........................#.......#...........................................#........................................................#.....
.....#..............#......................#.........#......#.........................................#.....................................
.....................................................................................................................#......................
....................................................................................#.....................................................#.
.............#.......................#......................................................................................................
.#......................#....................#.....................#.............................................................#..........
..................................................#.........................................................#...............................
.................................#........................................#.................................................................
.....................................................................................#..............................................#.......
............................................................................................................................................
.......#..................#.............................#........................#.................#.................#....................#.
..........................................................................................#.................................................
....................................#..........................#.........................................#.....................#............
......................#...................#..................................#....................................#.........................
....#........#.............................................................................................................#................
...............................#...............#......................#...............................#.....................................
.........#.......#.......#..................................................................................................................
.#.....................................................#....................................#.............#...........................#.....
...........................................#......#......................#.....................................#............................
.............................................................#..............................................................................
.............................#......#..........................................#............................................................
....#..................#............................................#...............................#.......................................
.........#.......#.............................#.........................................#..................#........#............#.........
.......................................................................................................................................#....
#.............................................................................................#.............................................
...................................#..............................#......................................................#..................
............................#...........................#................#.............................#.......#..............#.............
................................................#.........................................................................................#.
........#.............#.....................................................................................................................
....................................................................#......................................................#................
............................................................#........................................#......................................
.............#...................#.................................................#........................................................
.............................................................................#.......................................#......................
.........#...................#........#.........#........................................................#..............................#...
.#....................................................................#..................................................#.......#..........
................#...............................................................................................#...........................
......................#....................#............#...............................#...................................................
......#.......................................................#...................................#.........................................
.........................................................................#......#............................................#..............
..........#.........................................................#.......................................................................
............................#.........#................................................................#............#.......................
.......................#......................................................................#.............#...............................
................#.......................................#...............................................................................#...
#..............................#.....................................................#......................................................
............#....................................................................................#..............#.......#...................
.....................#..............#............................#..........................................................................
....#.............................................................................#.......................................................#.
.....................................................................................................#.....#.......................#........
...............#..............#............#.............................................#................................#.................
...........................................................#.........................................................#......................
.....................................................#...........................................#..............#...........................
...........#...............#.......................................#...............#........................................................
................................#...........................................................................................................
................#.........................#...............................#.............#.......................................#.....#.....
...............................................................#.............................#........#...............#.....................
..#.........................................................................................................................................
............................#......#................................#.............#...............#.........................................
...........#.........#.............................#.........................................................#..............................
.....#...................................................#..................#..................................................#...........#
..........................................#..............................................................#..................................
.....................................#......................................................................................................
.......................#......#............................................................#.......................#........#.....#.........
.#........#.......................................#.........................................................#...............................
................#................................................................#..........................................................
.........................................#.............................................#....................................................
...............................................#.......................................................................#........#...........
............................................................................................................................................
..............................#.........................#......#....................#.......................................................
.............................................................................................................#..............................
.................#.......................................................................................................................#..
........#................................#.........................#............#.........#......#........................#.................
........................#...............................................................................#..................................."""


@mark.parametrize(
    ("input_string", "empty_space_multiplier", "expected_output"),
    [
        (EXAMPLE_INPUT, 2, 374),
        (PUZZLE_INPUT, 2, 9799681),
        (EXAMPLE_INPUT, 10, 1030),
        (EXAMPLE_INPUT, 100, 8410),
        (PUZZLE_INPUT, 1000000, 513171773355),
    ],
)
def test_cosmic_expansion(input_string: str, empty_space_multiplier: int, expected_output: int) -> None:
    assert cosmic_expansion(input_string, empty_space_multiplier) == expected_output

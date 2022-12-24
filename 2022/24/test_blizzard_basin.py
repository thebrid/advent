from collections.abc import Iterable
from dataclasses import dataclass

from pytest import mark


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


Grid = tuple[tuple[str, ...], ...]


def blizzard_basin(grid: Grid, start_time: int, start: Coord, goal: Coord) -> int:
    time = start_time
    current_positions = {start}

    while goal not in current_positions:
        time += 1
        updated_grid = move_blizzards(grid, time)
        current_positions = {
            neighbour for position in current_positions for neighbour in _neighbours(updated_grid, position)
        }

    return time


def _neighbours(grid: Grid, current_pos: Coord) -> Iterable[Coord]:
    height = len(grid)
    width = len(grid[0])

    if current_pos.x - 1 >= 0 and grid[current_pos.y][current_pos.x - 1] == ".":
        yield Coord(current_pos.x - 1, current_pos.y)

    if current_pos.x + 1 <= width - 1 and grid[current_pos.y][current_pos.x + 1] == ".":
        yield Coord(current_pos.x + 1, current_pos.y)

    if current_pos.y - 1 >= 0 and grid[current_pos.y - 1][current_pos.x] == ".":
        yield Coord(current_pos.x, current_pos.y - 1)

    if current_pos.y + 1 <= height - 1 and grid[current_pos.y + 1][current_pos.x] == ".":
        yield Coord(current_pos.x, current_pos.y + 1)

    if grid[current_pos.y][current_pos.x] == ".":
        yield Coord(current_pos.x, current_pos.y)


def move_blizzards(grid: Grid, num_steps) -> Grid:
    height = len(grid)
    width = len(grid[0])

    output = [["#" if value == "#" else "." for value in row] for row in grid]

    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value == ">":
                new_x = (x - 1 + num_steps) % (width - 2) + 1
                _set_blizzard(output, value, new_x, y)
            elif value == "<":
                new_x = (x - 1 - num_steps) % (width - 2) + 1
                _set_blizzard(output, value, new_x, y)
            elif value == "v":
                new_y = (y - 1 + num_steps) % (height - 2) + 1
                _set_blizzard(output, value, x, new_y)
            elif value == "^":
                new_y = (y - 1 - num_steps) % (height - 2) + 1
                _set_blizzard(output, value, x, new_y)

    return tuple(tuple(row) for row in output)


def parse_input(input_string: str) -> Grid:
    return tuple(tuple(line) for line in input_string.split("\n"))


def _set_blizzard(output: list[list[str]], value: str, x: int, y: int) -> None:
    output[y][x] = value if output[y][x] == "." else str(int(output[y][x]) + 1) if output[y][x].isnumeric() else "2"


EXAMPLE_INPUT = """#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#"""

EXAMPLE_INPUT2 = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""

PUZZLE_INPUT = """#.####################################################################################################
#<<v<.^<<<v.^v<>v^^vvv<<v<^><<>^^^v^v<^<v^>>.<v<v>^vv>>vvv<^<v>v^.<v^>>>>v<^^<v^v<v>>v^.v><<^vv^<><>>#
#<<v^.<^><.<<v<vv<vv><.<^.><>vv>v<>v^^>vv^<<.<^<>.v>vv>v^v>vv<v>.<<^^<.^...<<v^.^.v>>.<<><^v>vv>>v^^<#
#>v<vv>^<^>^^^^^>v<v>v.v.v>v^v^<.^^<^>^<>>^v>v<^.v^^v<^>^>^>vvv<>>.^<>^>^>v>.>.<>v..v>>vvv^>>>vv<^vv>#
#<<>v^.>v^>>v<^><v>.^v.<^v^<<<>v><>^><>v<.v>^v^><v^<>>vvv^>>>v.v.<^^.^<v<^.<<v^<<<vv<v<<>>v><v>^<^<v>#
#>>vv<v>^^^<vv<>^>>>^.<v^<^^>.v>^<>v<<..v<>^v<v>>vvv..v>v<>>^>>^>>^^^<.^^<^>v<.v<^^v^.>^<v><>.^<^^>>.#
#<v<><.<><<<^v<v<<v<>.<^>^v>v^.^.<v>vv>v..^><^.<v<<>v<^>>v<>vvv<vv<<><vv<>>^><.v<v<^^v^>v>>v>v^<vv^^<#
#>^^v^><<<^.^<v><><v^^^^.^>>>>.^v.v<.<^v>v><>^.>>.^>v>>^>>^>^><^^^<v^^^>v<^>^^<vvv<^v^<>.^vv<^>.^>^^<#
#<<vv^^^><<<v.<v>^>v>^^><v<<><<^<<<v>.<v^<<>><>^>>>><v<.^>>>><^<>>v^vv^<.<>.>>.^v>.v^>.>vvvv^v<><v^<<#
#>>v>>^<<v.^v.vvvv<>>><>^v<^<>><v<^vv<.v>v>^<v<>>^<>>>^.>^v<>>vv<vvv^<vv.<<.v<<>.>^^<>^<>^v^^^>>>^.^>#
#>><>vv>^>>v^>v>^^v.<<^v.<..>>>^^vvvv..^v>^>.<.v<^<<.><.^>.<v><<>.<v^vv><^<<>v^vv^>v<^.^^>^<<^.<<<>.<#
#<>v>>v<>>>.v<<v<^^v<>^v<^^<v.>^<^v>vv>^>v<vv><v<v<^>>vv>>>v.<<<><.<><>.<>>^><<^vvvvv^<<<v<vv>>.<<^<.#
#><<.>^v<>^.vv^>^><><.<^>>vv^vvv><v><.>^^^v^..><><.vv<^>v.v<vvv><^^v.<>v<.^v<^>>>v<v^<>^>v<v^v>^v><>>#
#><v>.>^<<v>>.<<<<vv^<<^v^>vv<^^v><>><<v<^>vv>^^>v^^^<<v.vv<><^>>>>>>>^>^^.>>^.<>^<^<v.^.<v^^>.>>v^<<#
#>><<.<^<.<<>vv<>>v<.<><^^>^<>v^<<^^^>^^<<^<>^<<v<^^^.v>v<^v>.<v<.vv>^>><.>^<.>.>>v^><<v<^<^.><.^.^v<#
#>v^^v>v><^><<^^^<<vv>>.v>^<>^^>v>^.v>>v^<^v<v^^>vv^v><>^>><^<v.v>v><<<<>v.<.^>^<v.<<<<v^<<<<>>^>v^<>#
#<^^v<<^>v.<<>^vv^^<^<v>>vvv^^<>>^v^v..v^v>v.^<^.<<v<>v><.<^<^v<>^>v<vv>v><<.vv^.>^>v..>><<.v<^v^>>^.#
#>v^v.v^v><>vv<^v^<v^v<>v<v<<>>..^.<vv^v>v.>^<vv>><^>v>>^^v^vv<^<^>>v^v>^^^><v.>>^^.v.^>><<><.vv.^>>>#
#.^>>.<^v.>vvv<v>>^<.v<v<<v^v>v.>.>v<^.<^.v.<.>vvv^vv><.^^v>>>v>^>^vv<<.<^<>>vv.^>vvvvv^><><v^<^v^>v.#
#<>v^^^.>^>>>^>v.<^.<<^^<>>v>vv.v.^.><v^<v^v<^>^>><vv>^.^.<^^<<<<v>^.>.<<.>.>^><v.v^.^<><^>^v><.vv^<<#
#>>vv^^<v<<v<.>v>^...>vv..^v^>^<>v^^^<<<.>^v>>>>.>^<.v><v><^^^vv>.v^>v.>v^>>><^v<>vv>v>v.^><^v<^^<vv>#
#>^<><<.>.>>v>>v<<^^v^.v^>.>>vv^.><<v^<v^>>>vvv<v<.<>^>>>>v>^^^.v^<.v><<v><.<v^<<<^>v^v^^^.>>>^>>v<><#
#<^v<^<<^<v^>^^<.<..vvv^^v^^><<.>^v<<vv<<>v<>><<>>v^.<v><>.<^vv<<>>>>^><v<<^v^vv.v.<vv^>^>><<^<<<v^^>#
#<v>^><><^^v>><<^>>^>><.>>v<^v>^v.<<v^>^<v>vv^^<<v><vvv>^.<v^v<^v^.^<<^<v>v^v>v.>v<>><v.v.><<^vvv^>.<#
#>><.<><>>>v...v<><v>v<^>><vv^<^^<v<v^<v>^.<^v><>>v<v^v>v^>>v<^>v<>.vv<<^^^v<>v<<^><^<v^.<^<^.>v^..><#
#><<>^vv.v<<v<<^v.><>^.<.<<<^^.v^<v^<vvv^v^>^>><^<>^>>^>^vv.^>vvvv<^<v.>^<.^vvv<><.^^>>^..v<^^<><<>><#
#<.><v<><^.><<.^<^^v^v><>^>.<^>.<v^^^>><^vv^vv<<>v.vv<^.^>^>.>>.<<^v>>^^.vv>vvv<vv>^>>>v^<>v.>.>v<>>.#
#<v>>>>^><^v^>^^vvv^<<v<v<<^^><^<vv><v>>v<>v^^>v>.<>v>^>v>>v.>.>>>^^^vv<<<>^><^<><v<^^^^^.<^vvv^<<<.<#
#.<v^<>>vv<^v^<v>>v<><.>.^^>^<v^>>v<<.<>v>^^v^v<>vv^^v>v>vvvvv>v^^<<^<><^v<v>>^<<v>>^.^v<^<<<<^v<.<><#
#<.^v>^vv^>^v<>>^^v.v<vvv.v<<^.>v><^vv>><.^<><v>..><>>.vv>>>.>v<v><v^..<v<<<^^><v<v<.v^..<v.^v<>>><^>#
#>vv.<..>^vv<^><>v>^vv<^.>^.<v^<v>vvv>>><<^v<>^<^v>^v.^v^v^><^><^<v.^vv<>^v>^<<^v^^>^^>^.v<>.<>v>>.^>#
#<v^^v<.<<vv.<>v^<^>^.<^<v<v^<<v<v.<^^>^>^v>>.<v.>^v.^v.^><<^>v<v.^vv^.^^>>>^<<>>^^<vv>v.<>^.v>^v.>v>#
#<>v>>^^<<>^^>><^vvv^^<<><><vv<vv>v>>>^><^.<v<^.>>v<<<vv.^<<^^><v><^.<><<v>^v^<^><>v..><<...<^.v.^v.>#
#>.>^>v><..^<^^^v^v<v><<^.^>.^v^v<^>>v><<.>v^<<^<<>^<.>>>v<.>>v>^^.<<>>^><v..v<vvvvv^v.<<<v..^^>.<^<<#
#<v>>.^<..>><>v^^>^^>.^^v^vv<>.<<v>><^<^<.^>^^>^<<.v^<<v^.^>v^^>>>.v><>^^<<><^<vv>^v.<^<v<<vv^v.<<<v<#
#.^^^<<v>v^vv^vv^>v^<v<^.v<^^>v^.^^^^>^<<^^>.>^^>^v<.vv>><v^v<vvv^>^>^<^^<v<>.v>^<v.<v^>.<v^.^>v^vv<>#
####################################################################################################.#"""


@mark.parametrize(
    ("input_string", "num_steps", "expected_output"),
    [
        (
            EXAMPLE_INPUT,
            1,
            """#.#####
#.....#
#.>...#
#.....#
#.....#
#...v.#
#####.#""",
        )
    ],
)
def test_move_blizzards(input_string: str, num_steps: int, expected_output: str) -> None:
    assert move_blizzards(parse_input(input_string), num_steps) == parse_input(expected_output)


@mark.parametrize(
    ("input_string", "expected_output"),
    [
        (EXAMPLE_INPUT2, 18),
        (PUZZLE_INPUT, 247),
    ],
)
def test_blizzard_basin(input_string: str, expected_output: int) -> None:
    grid = parse_input(input_string)
    height = len(grid)
    width = len(grid[0])

    start = Coord(x=1, y=0)
    goal = Coord(x=width - 2, y=height - 1)

    assert blizzard_basin(grid, 0, start, goal) == expected_output


@mark.parametrize(
    ("input_string", "expected_output"),
    [
        (EXAMPLE_INPUT2, 54),
        (PUZZLE_INPUT, 728),
    ],
)
def test_blizzard_basin_with_backtrack(input_string: str, expected_output: int) -> None:
    grid = parse_input(input_string)
    height = len(grid)
    width = len(grid[0])

    start = Coord(x=1, y=0)
    goal = Coord(x=width - 2, y=height - 1)

    time_so_far = blizzard_basin(grid, 0, start, goal)
    time_so_far = blizzard_basin(grid, time_so_far, goal, start)
    time_so_far = blizzard_basin(grid, time_so_far, start, goal)

    assert time_so_far == expected_output

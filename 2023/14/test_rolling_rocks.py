from enum import IntEnum

from pytest import mark


class RockType(IntEnum):
    EMPTY = 0
    ROUND = 1
    CUBE = 2


Grid = list[list[RockType]]


def rolling_rocks(input_string: str) -> int:
    grid = _parse_input(input_string)
    _roll_north(grid)
    return _summarise_grid(grid)


def rolling_rock_cycles(input_string: str, num_cycles: int) -> int:
    grid = _parse_input(input_string)
    lookup = dict[str, int]()
    n = 0

    while n != num_cycles:
        _roll_cycle(grid)

        cycle_length = _compute_cycle_length(lookup, grid, n)

        if cycle_length is not None:
            break

        n += 1

    assert cycle_length is not None
    n += cycle_length * ((num_cycles - n) // cycle_length) + 1

    while n != num_cycles:
        _roll_cycle(grid)
        n += 1

    return _summarise_grid(grid)


def _summarise_grid(grid: Grid) -> int:
    height = len(grid)
    return sum(height - y for y, row in enumerate(grid) for x, rock in enumerate(row) if rock == RockType.ROUND)


PRINT_LOOKUP = {RockType.EMPTY: ".", RockType.ROUND: "O", RockType.CUBE: "#"}


def _compute_cycle_length(lookup: dict[str, int], grid: Grid, current_cycle: int) -> int | None:
    as_string = "\n".join("".join(PRINT_LOOKUP[value] for value in row) for row in grid)
    looked_up = lookup.get(as_string)
    if looked_up is None:
        lookup[as_string] = current_cycle
        return None

    return current_cycle - looked_up


def _parse_input(input_string: str) -> Grid:
    return [_parse_line(line) for line in input_string.splitlines()]


def _parse_line(line: str) -> list[RockType]:
    LOOKUP = {".": RockType.EMPTY, "O": RockType.ROUND, "#": RockType.CUBE}
    return [LOOKUP[char] for char in line]


def _roll_cycle(grid: Grid) -> None:
    _roll_north(grid)
    _roll_west(grid)
    _roll_south(grid)
    _roll_east(grid)


def _roll_east(grid: Grid) -> None:
    for x in range(len(grid[0]) - 1, -1, -1):
        for y in range(len(grid)):
            if grid[y][x] != RockType.ROUND:
                continue

            temp_x = x
            while temp_x < len(grid[y]) - 1 and grid[y][temp_x + 1] == RockType.EMPTY:
                grid[y][temp_x], grid[y][temp_x + 1] = grid[y][temp_x + 1], grid[y][temp_x]
                temp_x += 1


def _roll_north(grid: Grid) -> None:
    for y in range(1, len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] != RockType.ROUND:
                continue

            temp_y = y
            while temp_y > 0 and grid[temp_y - 1][x] == RockType.EMPTY:
                grid[temp_y][x], grid[temp_y - 1][x] = grid[temp_y - 1][x], grid[temp_y][x]
                temp_y -= 1


def _roll_south(grid: Grid) -> None:
    for y in range(len(grid) - 1, -1, -1):
        for x in range(len(grid[y])):
            if grid[y][x] != RockType.ROUND:
                continue

            temp_y = y
            while temp_y < len(grid) - 1 and grid[temp_y + 1][x] == RockType.EMPTY:
                grid[temp_y][x], grid[temp_y + 1][x] = grid[temp_y + 1][x], grid[temp_y][x]
                temp_y += 1


def _roll_west(grid: Grid) -> None:
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            if grid[y][x] != RockType.ROUND:
                continue

            temp_x = x
            while temp_x > 0 and grid[y][temp_x - 1] == RockType.EMPTY:
                grid[y][temp_x], grid[y][temp_x - 1] = grid[y][temp_x - 1], grid[y][temp_x]
                temp_x -= 1


EXAMPLE_INPUT = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
PUZZLE_INPUT = """O...#.O......#...##....O#.#.OO...O.#OO#.....#O.O.....#......#.OO...O...O..O#O#....#...O..O...O.....O
.OO......O.OO.O.#.#O.O...#.##OO.....#.#O#...OOOOO..##O#O..O#O.##O...#O....O#.#.OO....#.........O.O.O
......O.O.O.....O.#.#.#OO#O#.O...O.#.......#O....#.O.#....OOO...#....O#O.......#......O...O##...O...
O...##O..#....OO.OO....O...O...O#..##.OOO..O..#OO....###....OO.O.O...........O...O..O.....#.#..O.O#.
............#.#.##O.O.#.#OO#........O..O.O..##....O.#..#O..O...O#.#.#.........O...........OO......O.
#.OO........#..#O.#......#....#....#......OO..OO...O#...#...#..##..O#.O......#.#..O..#O#...#..#.O#.O
O.O.##...........O...O..O...O.OO.......##....#...O.....##...#.....OO...O.O#...OO..........O...O..#O.
.O##....#.O#O....O.O.#.#O.O#..OO..##..#OO.#...#......#.#O#.....O...O#.O...#..O.#.#......#.##.O....O.
.........#..#.O..O..O.O...#.#.O...#.OOO.##..#.O.....OO#....O...OOO#.O#....##O..#.O.O.....O.O.O.O..O.
......#O.....OOO###.O..O####O.#.O...............#..O......##O...#.#..###...O....#O...OO.OO.O......O.
#.O....#.O..#O...#...#...O....OOO.#O.#.#..#.....#.#..OO..#OO.......#OO.OOO....O.#O.#.O......####..O.
OOOO...#.OO.#....O...O.O...##....#OO...O.##.O.....###..O........OO..O.O.......#.#...O..#..O.#..O....
OOO..##....O...O.....O#..O.O.#..O..#.#.#..O........O..#OOO.....#....O#OO.#.#.....O..#..O...O..O.#OO#
...##.#.##.#O....O#..O..O.........#.#.#O...O.......O...O#..OOOO....O...O.OO#.O.##...#....O..O.......
....##.###OOO.O...#.......OO....OOO....O.OO#..O.#..OO....OO......O..OO...OOO.OO#...#..OOO..O.###O...
O###O.....O.O.#O#.O.O#O.O###.....O..O........#....#..O#..#.#..O...........#......#OO........O..O####
.#.#.OOO.O.......#O..O.#..O.OO.OO.O..O.#.#...O.O.OO..##..O...#...#O#..O.........O.O..O.O#....O..#O..
.#..#O.#O..#.O.O.O...#OO....#...O....O..O.O...#..#.##O.O..O..#O.....OO##...O#.......O#O.#..........#
#O...#.#OO.O...#O...O...#.#.O#..#.O#.###.#......O..O....#..#.OO..#....O..O.O....#.O.O.O.#..O..OOO..O
O.....#...#.#OOO.OOOO..#O.O.#...O.##..OO..#O...#.....OO#..#.#...O##OO...O.....O..#...#...........O.O
.##.O#.O..#O#.O##.O.#.........##.O......#OO...OO.......#...#O.O#...O..#.#...O..#...#O...O.#....OO.OO
.O#OO.O..#...#..O..O...##.O....###O.....O...#.#OOO...OO...O.......#.#.#.OO....#OO.#..O..........OO..
.....#OO.O..O.O.O...O.O#.#.O...O..#...O##.......#......#O...#.#.#....#..O.O..#..........O..#.#..#O..
...O.O.O.OO...O#..O..OO..O#.#.O.#OO..O.O..OO..O#...#.O#...O.......#..#..O..##..O..#O......O.OO...O.O
#.O....O.O.#...O.....O.....O#......#.#..OO...#.....O.#.#.O...#.#....#....O#.O.#......#OOO.O...O#....
...OOO......#..O..O#.......#....O#OO..#O.#.#...#...O.O..OO..#.O...O..#.....OO..O..#...#.O...O#..O.OO
#OO.OO#.OOO...##............O....O.O..#.##.#.O.........##...#O.O..#................#..O.O.O#O.O#..##
.O.O.O##..#O.O#O...##.#OO#...#.OO#..O...O#...O....O#..OO....O....#...O...#OO.OO#O....#..O..#OO....O.
.OO.#.......#...O...OO..#..OO.O.O.OO#O.O.O...O....O#..#.O.........O..#.O...#.#...O.O......O........O
.O....##..#....#.....O.#...O.O.#....#....OOOO...O.O###.O........O.....O.O..#.##OOO.O.......#.#.O..O.
.#.....O...#.O...#........#...#....#OO.O...O#O........OOO...#.O....OOO#.O.....OO....#.#...#..OO..#..
OO.OO...O..#..#O....O.O....OOOOO.#O.#O.O...#.O....O#.O.O.#O.#...#..O...O.#O.O.#..O....OOO......#.O#.
.O##..OO.....#.OO..#..O..#...#.#........O..OO...#O..O....#..O..O#.....O#..##O..O#.##.#...#.O..O.O.O.
..#...#O.....OO#.....O..#.#O.#.#..#..O.....#...OO.#.....O..O.O##.O.....OOOO.#O.....O.#..O........#.#
.#.#O..O.O..#..O##.....O.OO...##.........O...####..O..O....#O..O.....##........O.#..#.#OO.#..O.##.O#
#...#.O....OO......#O...#O..O#..#O#O.#..#.....OO....OO#..#O....O.O..#.O.#.....O#.O.OO..O#.O.O..O.O#.
OO....OO......#O........#O...#.#..O##....O#..#.#O.O.#....O..O..O.O....O.......#..OOO#.........O....O
O.....#O.OO##......#O##..O..O...##..O..........O..OO.O..#O....O..OOO#OO.##..#....O#..#...O.O.O...O..
.............#.#.#.O...#.#..#......O.#.O..#....#..##....#.##.##.#.O...O.O..#.#.#...OO....O..#O..#..O
.O.#.....O.O..O..##O...OO.#.O....#..#.#...O.O#...#O.O.OO...O..#..OO...O...O...O.....#.O..O#..#.#..OO
.....O..OO......#.#.#.O.##.OO...O..O.#..#...#OO....OOO......O.OO.#.O..O#O...O.#......OO##O.O.#O..O..
O##O.#.#..#..OO.O.........#O.#..O.#.##.O#..OOOO..#....O...O.........O..O..###...O...O.#.....O..##.O.
..O...#O#O.O...O.#..#O.......OO...........#...#..##.O......#..O.O.#OO.OO.#O....#.O.....O..#..#.#..#.
O#..O..##O#....O..OOO..OO...#O..O.O...O#O...OO.O##.O#O..#......OO##O.##...OOO.O..#....O##O..#......#
..#O...O..O.O...#..O.O...#O.....O.O......##OO#..O......#..O.#.O......OO.#O........O.....OO...O...O.O
........OO.#.OO..O......#...#...#..OOOO.OO.#....O.OO...O.##.....O.O....#O.#.OO..##.##..#.#O#.OO...O#
....#......#O.OO.....OOO....OO..O.O.O....##..O..O.O#.O....O.#O.#O.....O..O........#O.....O.O.....O#.
#.O#.O#......##.....O.#O...###...##....#O#.#.#....OO...O..#.O....O..#..#..O..........O......#.O.O...
.O.#..O#.OO....O.#...#O....#....OO......#O.O..#O..........O.#..#...#OOO........#.#.........O.#..O...
#OO.OO..O..O.O.#O.O.....O.##..#.O#..#.O....#........#.OOO#.#.....#.#.......O#..##..#.OO....O#O#.....
.......#O.O....#.OOO..OO...O...#....O..#.#....OO..O....O.#.O.#O#..O#.#.O..O......##...OO..#....O.#..
.O..O#.#OO.O.O.O.##...O..O.O..O.##O...#.O..O..O..O..O.....O...#..OO#O..O###...#...#....O##.OO...#...
#O....#...##..O..#...#OO.O.O.#......O...O.#.#O..O...O....OOO..O.O..O...O.OO...O...#..O....O#.###....
....#..O.....##.O.......##.##..OOO.O.#.#.....#....O..#..O....#....O...#.O..O#..O##...#.##....O.#OO##
O....O...OO.O........#..O...#..#.....O......O.O.OO.OO..#....O..O.............##.O.....##O#.OOO......
........#.O.####O.OO.#.O..O.O.#.#....OO#.......O..#....##.OOO..O.O.O..#.O.#...O.O.O..O.##O..O#....O.
...#....#.....O....O.O.O##.O..#O.OO...#.##.O..###OO##.O......#..##.OO...O.......O.......#..O.#.O..O.
.O.O...O......OO.#....#O..O.O.O..OO.O..O##O...O....O..OO.#..O....O..#.O..OO.OO....O#O..#.O..#O...#.#
..O#O.#O..#...##..#.O...OO..O#.......#..O........#.OO#..O#.#.#O....##...O.........O......OO#.....O.#
....OO.......###..O#.....O##..#O..#..#.O.....##.......##..O#O....#....#O.O..#..#..O.###O..#.O#......
O..##..O...#..O...O#OOO....#.O##O.#........#.O..O.#..#.OO.#O.#.....##.O..O.O....#..#..OO....#..#..##
.#...O.OO#O.O..O.##O..O#...##...O....OO.O#....#...#O.O#....O..........#....#............##.......#..
.O.#........##O...#O..O..O....OO#O....#.O..OO.##..O..OO#.###OO.....#..#.......O.#.....OO........OO.#
.OO...O.#..##.....OO..O.O.O.#.###.##.O.#..O..#..O..O...##.#......O....O.O.........O..#.O.O#O.#O...#.
#..#.#..O...##.....OO#O.OOO.....#...#.....##.#...O....O....#..OO#.#.OO....#.....O.O...O#.#..#..O#O.O
.O#.O.#..O..O#...OO...O...O#...O..O..#.O..#...O#.#....O......O#...O...OO.O##.#O....O....#OO....#O...
OO..OOO.O......OO...OO#O...#.#.#O.OOO#....#.OO#.#.O.#......O.O.OO#..O..#..O.O#.O#.O....O..O...O.....
...OO....O...#OO#..#..O.#O#....O.....OO.O.#.OO##.....#..O#.OO..#.#.O#..#..O.#..O....#....O.#O...OO#O
..#.......OO..##.O#...O#....O.#.O..##..#O.......#O#......O..O.........O#..#OO..O..#O.#.#.O.O#.#OO#.O
...#O#...O...OO...OO..OO...#OO...O...##.O....##.#O##.O....#..O#..O.....O.......###.#.OO#...O......#.
.O.OO#O##O##...#..#....#..#O...O#..O.O##......#........#O.........#.O....O..#..O.....O..#......O.#.#
..#....#.O.O.O..O.....O.O#O.O..#......O............O.........O#.O....#.O#..O..O.#OO.....#......O...#
OO...#..O..O##.#.#O.O.#.#....O....O...O.#..O##...O...#.O...#.O.OO...#........O#O..O.O.O..O.....#.O..
.OOO....#...O..O.....O..O...O...O..O...O#...#O....O.O...#..OO##.O.#..O..........O#..#..#..OO#.....#.
O..#..O#....#O..##O..#.#.......OO..O..#...O....O.#....O..O.##........O...O..OO...#....OO#..O.#.#.#..
O#O.O.O#.#OO#..OO.O.#......#.....#.......##.O..#.O..#..OO..O.#.#.O.O.O#.#......O....####OO#.#O#OO.#.
.#.....O#..O#O#..OO...#.O.#....#.#..##....O##....#.........##OO...##...O......#.OO...#O....O.O.O#O..
O......#.O....O...O.....OO.#....#O.##....#.O.O...O..#...O....#.O....O.O....#.OO.#.......#...#..#...O
...#OO..#......#..OO.O.O.##.O....O.##O##.OO#O.O.O..O.#O#O.OO...........O...###.#......O..#..#O#..OOO
O..O.#..O.OO.O...OO.OO..OOOO....O...#....##.OO.O.....#.......O.O........O.#.......#.......#..#.O..O.
.OO.##...#O..O#....O....#..O#....#.....O...O#.....OOO#.....................#..#..#..#O.......O.#OO..
.#OO..O....O..#.....#O...OO.#....#.#.O...O.#........O...O..O..OO#..#.....#.......OOOOO.OO....O....O.
.O#...#.......O.O...O.O.O#...OO.O#...O#O.O.#......#......O..O##.##.....O.....##...........O#...O....
.#.O.O#.....O.#..OO......#O.#..O..O.O.O..#.#...O##.#O..OOO......#...#..OO...O.#.....#O.OOO...#.O..##
.........O..##OO.#OOOO.O.O..OOO...OO.#.....#...O.#O##..O#..#.#..#...#..O.O...#OO.O...O...#O...#..#..
.#.#O.#...#OO.O.........O#..O...OO#.....O....OOOO#.....O.O....#...O...........O#.#.O..O.#.O.#.O.#.#.
......O.#...O.....O.O..O#...O.#........#.O...O.O....#..O#....O.#.O.O....O...#OO...#........OO..O.O.O
....O.O..OO.....#...OOOO.O#............O#OO....OOOOOO..#..#O#..#.#.O.OO.#O.....O.#......##..O#..#O..
..#......#...#O.#..#.#....OOO#...O.#....O..#O.....O.....O.O......O.......O.O..O..O.OO.O.#OO..O#...#.
.O.#.O.OO..O#.O#OO..........O.......O..#..#.#..O...#...##.....####...#........##O.......#....#...O##
........#.#.O.#O.......#O...O...#.#O..#OOO..#O..###...O.#.#O...O.O#..O..O...O.O....###.OO.#OO..O.#.O
..#O....#..O..####.O#...O....O.#O.##.O....O.O......O#O...OO###...O..#........#.#O.O#OO.......#.....O
....O.....#.#.O.#..O.#O.#.#O.#.......OO.....OOO...O.O..#.#....#..O.O..#.OO.O..O..OO##.....#.O..OO#O.
O#O..OO.O....OO.#O......O......#...#.....O.#OO.#.....OO..O#.O..O.O...#....O.O..OO.O....#....OO..O...
...O.....##....#....#....#......O#O..OO.....OO#O.OO......#OO.......O.#..###OO...#.O..OO.#.O.O#OO..#.
.O.#.O..#O.....#.#O....##OO.#O..##..##.##...#OO.O.#O#..O..O.O..O..##O.O.....O.OOO..#..#O..O#..OO...O
..##O#O.O.#.........O....O.OO#O#O.....O.....O#O.OO.O......O.O.OO......#.....O.O.O.O.O.....#.O.......
.....#OO.#O........O#....O.#OO.OO........#.O....O.OOOOOO.#.#O......O.#...O#.O.O..OO.....O.OO...#.O.#
.....#................OO..OOOO..#.....O.###O.O...O..#O..........OO.#...OO.O#...O......O..OOOO.#..###
O.....O...#O.#..........#O......O..OOO#....O.OOOO....O..#..#O....O.....O#..O..#.O.O....#OO.#....#O.."""


@mark.parametrize(("input_string", "expected_output"), [(EXAMPLE_INPUT, 136), (PUZZLE_INPUT, 113525)])
def test_rolling_rocks(input_string: str, expected_output: int) -> None:
    assert rolling_rocks(input_string) == expected_output


@mark.parametrize(
    ("input_string", "num_cycles", "expected_output"),
    [(EXAMPLE_INPUT, 1000000000, 64), (PUZZLE_INPUT, 1000000000, 101292)],
)
def test_rolling_rock_cycles(input_string: str, num_cycles: int, expected_output: int) -> None:
    assert rolling_rock_cycles(input_string, num_cycles) == expected_output

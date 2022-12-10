from collections.abc import Iterable
from dataclasses import dataclass

from pytest import mark


@dataclass
class Instruction:
    pass


@dataclass
class NoOp(Instruction):
    pass


@dataclass
class AddX(Instruction):
    operand: int


def signal_strength(input_string: str) -> int:
    instructions = _parse_input(input_string)
    cycle_values = _interpret_instructions(instructions)
    output = 0

    for pc, x in enumerate(cycle_values):
        if pc in {19, 59, 99, 139, 179, 219}:
            output += (pc + 1) * x

    return output


def crt_output(input_string: str) -> str:
    instructions = _parse_input(input_string)
    cycle_values = _interpret_instructions(instructions)

    crt = [[False] * 40 for _ in range(6)]

    for pc, x_register in enumerate(cycle_values):
        x_beam = pc % 40
        y_beam = pc // 40

        if x_register - 1 <= x_beam <= x_register + 1:
            crt[y_beam][x_beam] = True

    return "\n".join("".join("#" if cell else "." for cell in row) for row in crt)


def _interpret_instructions(instructions: Iterable[Instruction]) -> Iterable[int]:
    x = 1

    for instruction in instructions:
        match (instruction):
            case AddX(_):
                yield x
                yield x
                x += instruction.operand
            case NoOp():
                yield x


def _parse_input(input_string: str) -> Iterable[Instruction]:
    for line in input_string.split("\n"):
        yield _parse_line(line)


def _parse_line(line: str) -> Instruction:
    tokens = line.split(" ")

    if tokens[0] == "noop":
        return NoOp()
    elif tokens[0] == "addx":
        return AddX(int(tokens[1]))

    raise RuntimeError(f"Unexpected {line=}")


EXAMPLE_INPUT = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""


EXAMPLE_OUTPUT = """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""


PUZZLE_INPUT = """noop
noop
noop
addx 6
addx -1
noop
addx 5
noop
noop
addx -12
addx 19
addx -1
noop
addx 4
addx -11
addx 16
noop
noop
addx 5
addx 3
addx -2
addx 4
noop
noop
noop
addx -37
noop
addx 3
addx 2
addx 5
addx 2
addx 10
addx -9
noop
addx 1
addx 4
addx 2
noop
addx 3
addx 2
addx 5
addx 2
addx 3
addx -2
addx 2
addx 5
addx -40
addx 25
addx -22
addx 2
addx 5
addx 2
addx 3
addx -2
noop
addx 23
addx -18
addx 2
noop
noop
addx 7
noop
noop
addx 5
noop
noop
noop
addx 1
addx 2
addx 5
addx -40
addx 3
addx 8
addx -4
addx 1
addx 4
noop
noop
noop
addx -8
noop
addx 16
addx 2
addx 4
addx 1
noop
addx -17
addx 18
addx 2
addx 5
addx 2
addx 1
addx -11
addx -27
addx 17
addx -10
addx 3
addx -2
addx 2
addx 7
noop
addx -2
noop
addx 3
addx 2
noop
addx 3
addx 2
noop
addx 3
addx 2
addx 5
addx 2
addx -5
addx -2
addx -30
addx 14
addx -7
addx 22
addx -21
addx 2
addx 6
addx 2
addx -1
noop
addx 8
addx -3
noop
addx 5
addx 1
addx 4
noop
addx 3
addx -2
addx 2
addx -11
noop
noop
noop"""

PUZZLE_OUTPUT = """###...##..###....##..##..###..#..#.###..
#..#.#..#.#..#....#.#..#.#..#.#..#.#..#.
#..#.#..#.#..#....#.#....###..####.#..#.
###..####.###.....#.#....#..#.#..#.###..
#....#..#.#....#..#.#..#.#..#.#..#.#....
#....#..#.#.....##...##..###..#..#.#...."""


@mark.parametrize(("input_string", "expected_output"), [(EXAMPLE_INPUT, 13140), (PUZZLE_INPUT, 14340)])
def test_signal_strength(input_string: str, expected_output: int) -> None:
    assert signal_strength(input_string) == expected_output


@mark.parametrize(("input_string", "expected_output"), [(EXAMPLE_INPUT, EXAMPLE_OUTPUT), (PUZZLE_INPUT, PUZZLE_OUTPUT)])
def test_crt_output(input_string: str, expected_output: str) -> None:
    assert crt_output(input_string) == expected_output

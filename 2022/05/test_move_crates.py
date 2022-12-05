from collections.abc import Callable
from dataclasses import dataclass

from pytest import mark


@dataclass
class Instruction:
    count: int
    old_col: int
    new_col: int


CrateMover = Callable[[list[str], Instruction], None]


def move_crates(crates_string: str, instructions_string: str, crate_mover: CrateMover) -> str:
    crates = _parse_crates(crates_string)
    instructions = _parse_instructions(instructions_string)
    _apply_instructions(crates, instructions, crate_mover)
    top_crates = [stack[-1] for stack in crates]
    return "".join(top_crates)


def _apply_instructions(crates: list[str], instructions: list[Instruction], crate_mover: CrateMover) -> None:
    for instruction in instructions:
        crate_mover(crates, instruction)


def _move_crates_one_by_one(crates: list[str], instruction: Instruction) -> None:
    for _ in range(instruction.count):
        assert crates[instruction.old_col - 1]
        char = crates[instruction.old_col - 1][-1]
        crates[instruction.old_col - 1] = crates[instruction.old_col - 1][:-1]
        prev = crates[instruction.new_col - 1]
        crates[instruction.new_col - 1] = f"{prev}{char}"


def _move_crates_together(crates: list[str], instruction: Instruction) -> None:
    crates_to_be_moved = crates[instruction.old_col - 1][-instruction.count :]
    crates[instruction.old_col - 1] = crates[instruction.old_col - 1][: -instruction.count]
    prev = crates[instruction.new_col - 1]
    crates[instruction.new_col - 1] = f"{prev}{crates_to_be_moved}"


def _parse_crates(crates_string: str) -> list[str]:
    output = list[str]()

    for line in crates_string.split("\n"):
        for col in range(1, len(line), 4):
            output_col = (col - 1) // 4

            while len(output) <= output_col:
                output.append("")

            char = line[col]

            if char == " ":
                continue

            prev = output[output_col]
            output[output_col] = f"{char}{prev}"

    return output


def _parse_instructions(instructions_string: str) -> list[Instruction]:
    return [_parse_instruction(line) for line in instructions_string.split("\n")]


def _parse_instruction(line: str) -> Instruction:
    tokens = line.split(" ")
    return Instruction(count=int(tokens[1]), old_col=int(tokens[3]), new_col=int(tokens[5]))


EXAMPLE_CRATES = """    [D]
[N] [C]
[Z] [M] [P]"""

EXAMPLE_INSTRUCTIONS = """move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

PUZZLE_CRATES = """    [C]         [Q]         [V]
    [D]         [D] [S]     [M] [Z]
    [G]     [P] [W] [M]     [C] [G]
    [F]     [Z] [C] [D] [P] [S] [W]
[P] [L]     [C] [V] [W] [W] [H] [L]
[G] [B] [V] [R] [L] [N] [G] [P] [F]
[R] [T] [S] [S] [S] [T] [D] [L] [P]
[N] [J] [M] [L] [P] [C] [H] [Z] [R]"""

PUZZLE_INSTRUCTIONS = """move 2 from 4 to 6
move 4 from 5 to 3
move 6 from 6 to 1
move 4 from 1 to 4
move 4 from 9 to 4
move 7 from 2 to 4
move 1 from 9 to 3
move 1 from 2 to 6
move 2 from 9 to 5
move 2 from 6 to 8
move 5 from 8 to 1
move 2 from 6 to 9
move 5 from 8 to 3
move 1 from 5 to 4
move 3 from 7 to 2
move 10 from 4 to 7
move 7 from 4 to 3
move 1 from 4 to 7
move 1 from 7 to 9
move 1 from 2 to 3
move 11 from 1 to 7
move 12 from 3 to 7
move 8 from 3 to 8
move 29 from 7 to 2
move 3 from 7 to 3
move 3 from 9 to 2
move 4 from 5 to 3
move 7 from 3 to 5
move 28 from 2 to 3
move 1 from 7 to 5
move 2 from 8 to 5
move 2 from 4 to 1
move 2 from 1 to 4
move 1 from 7 to 6
move 1 from 7 to 1
move 3 from 2 to 8
move 1 from 1 to 7
move 9 from 5 to 3
move 12 from 3 to 1
move 1 from 4 to 3
move 1 from 6 to 4
move 3 from 2 to 9
move 16 from 3 to 7
move 2 from 9 to 6
move 5 from 7 to 2
move 1 from 9 to 7
move 1 from 4 to 2
move 13 from 7 to 2
move 13 from 2 to 7
move 12 from 7 to 8
move 2 from 6 to 4
move 16 from 8 to 1
move 4 from 3 to 1
move 3 from 3 to 2
move 1 from 5 to 7
move 1 from 5 to 3
move 3 from 4 to 6
move 19 from 1 to 3
move 5 from 8 to 4
move 6 from 3 to 2
move 5 from 4 to 2
move 1 from 7 to 4
move 1 from 4 to 9
move 3 from 6 to 7
move 1 from 9 to 2
move 16 from 2 to 4
move 9 from 1 to 8
move 10 from 4 to 2
move 2 from 7 to 5
move 5 from 8 to 4
move 12 from 2 to 9
move 2 from 7 to 4
move 12 from 9 to 5
move 11 from 5 to 6
move 3 from 1 to 9
move 1 from 5 to 7
move 2 from 9 to 2
move 10 from 3 to 2
move 1 from 9 to 2
move 2 from 8 to 9
move 1 from 7 to 8
move 1 from 8 to 4
move 7 from 2 to 6
move 1 from 1 to 5
move 5 from 3 to 1
move 1 from 5 to 1
move 2 from 3 to 9
move 2 from 1 to 6
move 3 from 9 to 8
move 14 from 6 to 1
move 1 from 3 to 5
move 5 from 4 to 6
move 1 from 9 to 6
move 7 from 6 to 9
move 1 from 6 to 2
move 8 from 1 to 4
move 7 from 1 to 7
move 10 from 2 to 1
move 4 from 7 to 6
move 10 from 4 to 6
move 5 from 8 to 2
move 1 from 5 to 9
move 2 from 2 to 6
move 2 from 4 to 7
move 1 from 2 to 7
move 5 from 9 to 2
move 1 from 2 to 9
move 14 from 6 to 8
move 2 from 8 to 4
move 1 from 2 to 6
move 4 from 9 to 3
move 2 from 6 to 8
move 5 from 4 to 5
move 5 from 8 to 3
move 1 from 2 to 4
move 3 from 7 to 1
move 2 from 2 to 7
move 1 from 4 to 7
move 1 from 4 to 5
move 1 from 2 to 8
move 1 from 4 to 9
move 8 from 8 to 2
move 3 from 1 to 5
move 7 from 2 to 9
move 8 from 1 to 6
move 6 from 7 to 2
move 2 from 2 to 8
move 5 from 1 to 8
move 3 from 6 to 8
move 4 from 3 to 6
move 3 from 6 to 2
move 8 from 9 to 2
move 11 from 5 to 7
move 12 from 2 to 6
move 2 from 3 to 7
move 12 from 7 to 2
move 10 from 6 to 9
move 1 from 7 to 1
move 12 from 8 to 7
move 2 from 3 to 2
move 8 from 9 to 7
move 6 from 2 to 5
move 1 from 1 to 6
move 3 from 2 to 6
move 1 from 3 to 7
move 5 from 5 to 3
move 10 from 7 to 2
move 2 from 3 to 7
move 8 from 7 to 6
move 20 from 2 to 8
move 5 from 8 to 1
move 5 from 8 to 6
move 1 from 5 to 7
move 1 from 1 to 4
move 4 from 1 to 2
move 1 from 9 to 6
move 3 from 3 to 1
move 4 from 7 to 5
move 1 from 9 to 8
move 11 from 8 to 7
move 1 from 4 to 9
move 2 from 7 to 5
move 31 from 6 to 9
move 4 from 2 to 3
move 6 from 5 to 1
move 4 from 1 to 2
move 7 from 7 to 8
move 1 from 7 to 6
move 1 from 1 to 7
move 24 from 9 to 4
move 2 from 7 to 8
move 2 from 9 to 2
move 2 from 7 to 5
move 2 from 5 to 9
move 3 from 4 to 1
move 20 from 4 to 2
move 1 from 6 to 1
move 16 from 2 to 1
move 4 from 3 to 1
move 1 from 4 to 8
move 5 from 8 to 5
move 5 from 8 to 1
move 1 from 5 to 2
move 3 from 5 to 6
move 33 from 1 to 6
move 6 from 9 to 4
move 15 from 6 to 7
move 6 from 4 to 3
move 1 from 5 to 3
move 7 from 3 to 9
move 11 from 7 to 5
move 10 from 5 to 8
move 2 from 7 to 3
move 5 from 8 to 9
move 1 from 7 to 5
move 1 from 5 to 8
move 1 from 5 to 7
move 2 from 3 to 8
move 2 from 7 to 5
move 2 from 8 to 7
move 1 from 5 to 9
move 1 from 7 to 6
move 3 from 8 to 6
move 22 from 6 to 9
move 1 from 7 to 6
move 27 from 9 to 4
move 18 from 4 to 8
move 5 from 4 to 1
move 1 from 5 to 1
move 3 from 6 to 3
move 2 from 3 to 5
move 2 from 5 to 2
move 1 from 2 to 6
move 1 from 6 to 3
move 9 from 8 to 6
move 3 from 9 to 8
move 9 from 6 to 5
move 1 from 6 to 9
move 15 from 8 to 5
move 1 from 3 to 4
move 6 from 1 to 8
move 1 from 3 to 7
move 8 from 5 to 8
move 2 from 5 to 6
move 3 from 4 to 6
move 1 from 7 to 6
move 2 from 5 to 3
move 5 from 5 to 1
move 2 from 3 to 7
move 1 from 8 to 1
move 10 from 2 to 9
move 5 from 6 to 3
move 7 from 8 to 5
move 4 from 3 to 5
move 1 from 2 to 1
move 2 from 7 to 6
move 5 from 1 to 5
move 1 from 3 to 7
move 1 from 7 to 6
move 3 from 8 to 5
move 4 from 6 to 4
move 1 from 2 to 9
move 5 from 4 to 6
move 21 from 5 to 3
move 2 from 8 to 4
move 3 from 4 to 1
move 1 from 8 to 4
move 18 from 3 to 5
move 2 from 3 to 6
move 2 from 6 to 9
move 2 from 6 to 2
move 1 from 2 to 9
move 19 from 9 to 4
move 3 from 6 to 3
move 2 from 9 to 4
move 1 from 1 to 2
move 1 from 3 to 7
move 16 from 5 to 2
move 4 from 1 to 9
move 3 from 3 to 4
move 4 from 9 to 8
move 3 from 5 to 1
move 22 from 4 to 5
move 1 from 7 to 2
move 22 from 5 to 9
move 2 from 5 to 2
move 2 from 4 to 6
move 10 from 9 to 5
move 1 from 8 to 3
move 13 from 9 to 2
move 1 from 6 to 3
move 19 from 2 to 7
move 2 from 7 to 4
move 1 from 8 to 4
move 1 from 8 to 2
move 11 from 5 to 7
move 3 from 1 to 7
move 8 from 7 to 8
move 1 from 3 to 5
move 1 from 8 to 3
move 1 from 5 to 3
move 6 from 2 to 3
move 1 from 8 to 7
move 1 from 6 to 1
move 1 from 1 to 8
move 4 from 8 to 1
move 1 from 4 to 6
move 8 from 3 to 9
move 2 from 2 to 3
move 3 from 8 to 5
move 1 from 8 to 2
move 4 from 2 to 7
move 5 from 9 to 7
move 1 from 6 to 3
move 4 from 2 to 4
move 23 from 7 to 5
move 4 from 1 to 2
move 3 from 9 to 6
move 2 from 4 to 8
move 2 from 8 to 3
move 2 from 6 to 1
move 1 from 6 to 8
move 8 from 5 to 3
move 5 from 2 to 6
move 5 from 6 to 3
move 1 from 8 to 3
move 4 from 4 to 7
move 15 from 5 to 2
move 1 from 1 to 9
move 2 from 5 to 1
move 4 from 3 to 7
move 1 from 4 to 9
move 4 from 7 to 1
move 2 from 5 to 6
move 7 from 1 to 2
move 6 from 2 to 3
move 16 from 2 to 5
move 1 from 6 to 3
move 1 from 6 to 3
move 9 from 7 to 4
move 6 from 4 to 6
move 1 from 9 to 8
move 23 from 3 to 9
move 1 from 3 to 4
move 3 from 4 to 5
move 9 from 5 to 2
move 6 from 9 to 7
move 7 from 7 to 5
move 5 from 5 to 3
move 1 from 4 to 6
move 3 from 3 to 8
move 6 from 2 to 1
move 3 from 5 to 6
move 4 from 7 to 1
move 2 from 3 to 9
move 5 from 6 to 8
move 19 from 9 to 6
move 1 from 9 to 2
move 9 from 5 to 9
move 4 from 8 to 3
move 5 from 6 to 1
move 4 from 6 to 1
move 2 from 3 to 8
move 17 from 1 to 7
move 2 from 1 to 2
move 6 from 6 to 9
move 4 from 8 to 5
move 3 from 8 to 2
move 3 from 5 to 6
move 4 from 6 to 8
move 2 from 6 to 9
move 4 from 8 to 7
move 9 from 9 to 5
move 5 from 9 to 4
move 7 from 2 to 8
move 1 from 2 to 1
move 3 from 6 to 5
move 6 from 8 to 5
move 1 from 3 to 4
move 1 from 3 to 1
move 12 from 7 to 2
move 5 from 2 to 7
move 8 from 7 to 5
move 1 from 9 to 3
move 5 from 2 to 8
move 3 from 6 to 3
move 2 from 2 to 3
move 1 from 2 to 4
move 2 from 3 to 4
move 1 from 1 to 6
move 14 from 5 to 6
move 1 from 8 to 6
move 3 from 3 to 7
move 4 from 7 to 1
move 9 from 4 to 3
move 3 from 1 to 4
move 1 from 1 to 2
move 1 from 8 to 4
move 8 from 3 to 1
move 1 from 3 to 2
move 5 from 7 to 6
move 3 from 1 to 6
move 2 from 2 to 8
move 13 from 5 to 3
move 5 from 1 to 3
move 3 from 4 to 5
move 1 from 9 to 2
move 4 from 3 to 9
move 1 from 1 to 7
move 2 from 5 to 8
move 1 from 7 to 5
move 2 from 5 to 4
move 1 from 2 to 6
move 1 from 4 to 5
move 7 from 3 to 6
move 31 from 6 to 1
move 25 from 1 to 7
move 2 from 3 to 2
move 13 from 7 to 9
move 1 from 1 to 6
move 1 from 4 to 1
move 2 from 2 to 9
move 1 from 4 to 6
move 3 from 7 to 1
move 7 from 8 to 3
move 1 from 8 to 2
move 1 from 2 to 8
move 4 from 3 to 4
move 1 from 8 to 7
move 3 from 6 to 9
move 5 from 7 to 6
move 1 from 4 to 7
move 5 from 7 to 9
move 5 from 3 to 6
move 3 from 4 to 7
move 1 from 5 to 4
move 4 from 7 to 9
move 32 from 9 to 1
move 1 from 6 to 5
move 1 from 5 to 9
move 4 from 3 to 8
move 5 from 1 to 4
move 4 from 4 to 9
move 6 from 1 to 7
move 4 from 9 to 8
move 4 from 7 to 8
move 1 from 7 to 1
move 1 from 7 to 6
move 7 from 6 to 3
move 1 from 9 to 5
move 2 from 4 to 7
move 25 from 1 to 6
move 1 from 7 to 1
move 1 from 3 to 4
move 18 from 6 to 8
move 1 from 5 to 1
move 3 from 1 to 6
move 21 from 8 to 3
move 1 from 8 to 4
move 2 from 4 to 2
move 1 from 8 to 1
move 1 from 7 to 6
move 5 from 6 to 3
move 30 from 3 to 1
move 4 from 8 to 6
move 1 from 2 to 9
move 1 from 8 to 5
move 9 from 6 to 5
move 2 from 8 to 7
move 3 from 5 to 9
move 2 from 3 to 4
move 1 from 2 to 1
move 1 from 5 to 8
move 1 from 8 to 3
move 2 from 4 to 6
move 1 from 3 to 1
move 1 from 5 to 6
move 5 from 5 to 7
move 4 from 6 to 8
move 3 from 8 to 2
move 1 from 1 to 5
move 1 from 8 to 7
move 4 from 9 to 6
move 1 from 5 to 1
move 4 from 6 to 8
move 6 from 7 to 3
move 4 from 3 to 9
move 2 from 2 to 7
move 1 from 3 to 5
move 3 from 7 to 6
move 2 from 9 to 8
move 1 from 2 to 4
move 1 from 3 to 4
move 5 from 8 to 4
move 1 from 9 to 2
move 1 from 7 to 5
move 3 from 4 to 5
move 1 from 9 to 1
move 1 from 2 to 7
move 1 from 7 to 1
move 5 from 5 to 4
move 4 from 1 to 4
move 19 from 1 to 9
move 6 from 6 to 2
move 12 from 9 to 1
move 1 from 8 to 6
move 1 from 9 to 4
move 4 from 4 to 8
move 1 from 6 to 5
move 1 from 5 to 3
move 2 from 8 to 9
move 5 from 4 to 6
move 5 from 9 to 4
move 1 from 4 to 3
move 2 from 2 to 9
move 1 from 6 to 5
move 1 from 6 to 9
move 7 from 1 to 5
move 1 from 3 to 1
move 2 from 8 to 3
move 1 from 5 to 7
move 2 from 9 to 8"""


@mark.parametrize(
    ("crates", "instructions", "expected_output"),
    [(EXAMPLE_CRATES, EXAMPLE_INSTRUCTIONS, "CMZ"), (PUZZLE_CRATES, PUZZLE_INSTRUCTIONS, "VPCDMSLWJ")],
)
def test_crate_moving_one_by_one(crates: str, instructions: str, expected_output: str) -> None:
    assert move_crates(crates, instructions, _move_crates_one_by_one) == expected_output


@mark.parametrize(
    ("crates", "instructions", "expected_output"),
    [(EXAMPLE_CRATES, EXAMPLE_INSTRUCTIONS, "MCD"), (PUZZLE_CRATES, PUZZLE_INSTRUCTIONS, "TPWCGNCCG")],
)
def test_crate_moving_together(crates: str, instructions: str, expected_output: str) -> None:
    assert move_crates(crates, instructions, _move_crates_together) == expected_output

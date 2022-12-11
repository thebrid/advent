from collections.abc import Callable
from dataclasses import dataclass
from functools import reduce
from operator import add, mul

from pytest import mark


@dataclass
class Monkey:
    items: list[int]
    operator: Callable[[int, int], int]
    lhs_operand: int | None
    rhs_operand: int | None
    test_divisor: int
    true_monkey: int
    false_monkey: int
    inspected: int = 0


def monkey_inspection(monkeys: list[Monkey], number_of_rounds: int, worry_level_update: Callable[[int], int]) -> int:
    for _ in range(number_of_rounds):
        _run_inspection_round(monkeys, worry_level_update)

    counts = [monkey.inspected for monkey in monkeys]
    sorted_counts = sorted(counts)

    return sorted_counts[-1] * sorted_counts[-2]


def _parse_input(input_string: str) -> list[Monkey]:
    lines = input_string.split("\n")

    return [_parse_monkey(lines[index : index + 6]) for index, line in enumerate(lines) if line[:6] == "Monkey"]


OPERATOR_MAP = {"+": add, "*": mul}


def _parse_monkey(lines: list[str]) -> Monkey:
    items_line = lines[1]
    assert "Starting items" in items_line
    parts = items_line.split(": ")
    assert len(parts) == 2
    starting_items = [int(token) for token in parts[1].split(", ")]

    operation_line = lines[2]
    assert "Operation: " in operation_line
    parts = operation_line.split(" = ")
    tokens = parts[1].split(" ")
    assert len(tokens) == 3
    operator_token = tokens[1]
    operator = OPERATOR_MAP[operator_token]
    lhs_operand = None if tokens[0] == "old" else int(tokens[0])
    rhs_operand = None if tokens[2] == "old" else int(tokens[2])

    test_line = lines[3]
    tokens = test_line.split(" ")
    test_divisor = int(tokens[-1])

    true_line = lines[4]
    tokens = true_line.split(" ")
    true_monkey = int(tokens[-1])

    false_line = lines[5]
    tokens = false_line.split(" ")
    false_monkey = int(tokens[-1])

    return Monkey(
        items=starting_items,
        operator=operator,
        lhs_operand=lhs_operand,
        rhs_operand=rhs_operand,
        test_divisor=test_divisor,
        true_monkey=true_monkey,
        false_monkey=false_monkey,
    )


def _run_inspection_round(monkeys: list[Monkey], worry_level_update: Callable[[int], int]) -> None:
    for monkey in monkeys:
        while monkey.items:
            worry_level = monkey.items.pop(0)
            lhs = worry_level if monkey.lhs_operand is None else monkey.lhs_operand
            rhs = worry_level if monkey.rhs_operand is None else monkey.rhs_operand
            worry_level = worry_level_update(monkey.operator(lhs, rhs))
            next_monkey = monkey.true_monkey if worry_level % monkey.test_divisor == 0 else monkey.false_monkey
            monkeys[next_monkey].items.append(worry_level)
            monkey.inspected += 1

    """
    for index, monkey in enumerate(monkeys):
        formatted_worry_levels = ", ".join(str(worry_level) for worry_level in monkey.items)
        print(f"Monkey {index}: {formatted_worry_levels}")
    print("\n")
    """


EXAMPLE_INPUT = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


PUZZLE_INPUT = """Monkey 0:
  Starting items: 83, 62, 93
  Operation: new = old * 17
  Test: divisible by 2
    If true: throw to monkey 1
    If false: throw to monkey 6

Monkey 1:
  Starting items: 90, 55
  Operation: new = old + 1
  Test: divisible by 17
    If true: throw to monkey 6
    If false: throw to monkey 3

Monkey 2:
  Starting items: 91, 78, 80, 97, 79, 88
  Operation: new = old + 3
  Test: divisible by 19
    If true: throw to monkey 7
    If false: throw to monkey 5

Monkey 3:
  Starting items: 64, 80, 83, 89, 59
  Operation: new = old + 5
  Test: divisible by 3
    If true: throw to monkey 7
    If false: throw to monkey 2

Monkey 4:
  Starting items: 98, 92, 99, 51
  Operation: new = old * old
  Test: divisible by 5
    If true: throw to monkey 0
    If false: throw to monkey 1

Monkey 5:
  Starting items: 68, 57, 95, 85, 98, 75, 98, 75
  Operation: new = old + 2
  Test: divisible by 13
    If true: throw to monkey 4
    If false: throw to monkey 0

Monkey 6:
  Starting items: 74
  Operation: new = old + 4
  Test: divisible by 7
    If true: throw to monkey 3
    If false: throw to monkey 2

Monkey 7:
  Starting items: 68, 64, 60, 68, 87, 80, 82
  Operation: new = old * 19
  Test: divisible by 11
    If true: throw to monkey 4
    If false: throw to monkey 5"""


@mark.parametrize(("input_string", "expected_output"), [(EXAMPLE_INPUT, 10605), (PUZZLE_INPUT, 112815)])
def test_monkey_inspection_with_division_update(input_string: str, expected_output: int) -> None:
    monkeys = _parse_input(input_string)
    assert monkey_inspection(monkeys, 20, lambda worry_level: worry_level // 3) == expected_output


@mark.parametrize(("input_string", "expected_output"), [(EXAMPLE_INPUT, 2713310158), (PUZZLE_INPUT, 25738411485)])
def test_monkey_inspection_with_mod_update(input_string: str, expected_output: int) -> None:
    monkeys = _parse_input(input_string)
    all_divisors = [monkey.test_divisor for monkey in monkeys]
    product = reduce(mul, all_divisors)
    assert monkey_inspection(monkeys, 10000, lambda worry_level: worry_level % product) == expected_output

from collections.abc import MutableMapping
from dataclasses import dataclass
from os.path import dirname, join

from pytest import mark

Circuit = MutableMapping[str, "Expression"]


@dataclass
class AndExpression:
    lhs: "Expression"
    rhs: "Expression"

    def evaluate(self, circuit: Circuit) -> int:
        return self.lhs.evaluate(circuit) & self.rhs.evaluate(circuit)


@dataclass
class ConstantExpression:
    value: int

    def evaluate(self, circuit: Circuit) -> int:
        return self.value


@dataclass
class LeftShiftExpression:
    variable: "Expression"
    shift: "Expression"

    def evaluate(self, circuit: Circuit) -> int:
        return self.variable.evaluate(circuit) << self.shift.evaluate(circuit)


@dataclass
class NotExpression:
    underlying: "Expression"

    def evaluate(self, circuit: Circuit) -> int:
        return 0xFFFF - self.underlying.evaluate(circuit)


@dataclass
class OrExpression:
    lhs: "Expression"
    rhs: "Expression"

    def evaluate(self, circuit: Circuit) -> int:
        return self.lhs.evaluate(circuit) | self.rhs.evaluate(circuit)


@dataclass
class RightShiftExpression:
    variable: "Expression"
    shift: "Expression"

    def evaluate(self, circuit: Circuit) -> int:
        return self.variable.evaluate(circuit) >> self.shift.evaluate(circuit)


@dataclass
class VariableExpression:
    underlying: str
    evaluation_result: int | None = None

    def evaluate(self, circuit: Circuit) -> int:
        if self.evaluation_result is None:
            self.evaluation_result = circuit[self.underlying].evaluate(circuit)

        return self.evaluation_result


Expression = (
    AndExpression
    | ConstantExpression
    | LeftShiftExpression
    | NotExpression
    | OrExpression
    | RightShiftExpression
    | VariableExpression
)


def logic_gates(circuit: Circuit, variable: str) -> int:
    return circuit[variable].evaluate(circuit)


def parse_input(raw_input: str) -> Circuit:
    output = {}

    for line in raw_input.splitlines():
        tokens = line.split(" -> ")
        expression = tokens[0]
        variable = tokens[1]
        output[variable] = parse_expression(expression)

    return output


def parse_expression(expression: str) -> Expression:
    if " AND " in expression:
        tokens = expression.split(" AND ")
        return AndExpression(parse_expression(tokens[0]), parse_expression(tokens[1]))
    elif " LSHIFT " in expression:
        tokens = expression.split(" LSHIFT ")
        return LeftShiftExpression(parse_expression(tokens[0]), parse_expression(tokens[1]))
    elif " OR " in expression:
        tokens = expression.split(" OR ")
        return OrExpression(parse_expression(tokens[0]), parse_expression(tokens[1]))
    elif expression.startswith("NOT "):
        return NotExpression(parse_expression(expression[4:]))
    elif " RSHIFT " in expression:
        tokens = expression.split(" RSHIFT ")
        return RightShiftExpression(parse_expression(tokens[0]), parse_expression(tokens[1]))

    try:
        return ConstantExpression(int(expression))
    except ValueError:
        return VariableExpression(expression)


EXAMPLE_INPUT = """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h"""

PUZZLE_INPUT = open(join(dirname(__file__), "puzzle_input.txt")).read()


@mark.parametrize(
    ("raw_input", "variable", "expected_value"),
    [
        (EXAMPLE_INPUT, "x", 123),
        (EXAMPLE_INPUT, "y", 456),
        (EXAMPLE_INPUT, "d", 72),
        (EXAMPLE_INPUT, "e", 507),
        (EXAMPLE_INPUT, "f", 492),
        (EXAMPLE_INPUT, "g", 114),
        (EXAMPLE_INPUT, "h", 65412),
        (PUZZLE_INPUT, "a", 3176),
    ],
)
def test_logic_gates(raw_input: str, variable: str, expected_value: int) -> None:
    circuit = parse_input(raw_input)
    assert logic_gates(circuit, variable) == expected_value


def test_logic_gates_with_overriden_b() -> None:
    circuit = parse_input(PUZZLE_INPUT)
    circuit["b"] = ConstantExpression(3176)
    assert logic_gates(circuit, "a") == 14710

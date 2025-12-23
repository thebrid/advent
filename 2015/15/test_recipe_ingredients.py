from collections.abc import Iterable
from dataclasses import dataclass
from re import compile

from pytest import mark


@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavour: int
    texture: int
    calories: int

    def __mul__(self, other: object) -> Ingredient:
        if type(other) is not int:
            return NotImplemented

        return Ingredient(
            name=self.name,
            capacity=self.capacity * other,
            durability=self.durability * other,
            flavour=self.flavour * other,
            texture=self.texture * other,
            calories=self.calories * other,
        )

    def __iadd__(self, other: object) -> Ingredient:
        if type(other) is not Ingredient:
            return NotImplemented

        self.name = ""
        self.capacity += other.capacity
        self.durability += other.durability
        self.flavour += other.flavour
        self.texture += other.texture
        self.calories += other.calories

        return self


Ingredients = list[Ingredient]
Quantities = list[int]


def get_best_recipe_score(raw_input: str, target_calories=None) -> int | None:
    ingredients = parse_input(raw_input)
    max_score = None

    for quantities in generate_quantities(100, len(ingredients)):
        total = sum_ingredients(ingredients, quantities)
        score = score_recipe(total)
        # print(f"{quantities=}\t{score=}")
        if (max_score is None or score > max_score) and (target_calories is None or total.calories == target_calories):
            max_score = score

    return max_score


def generate_quantities(amount_needed: int, num_ingredients: int) -> Iterable[Quantities]:
    if num_ingredients == 1:
        yield [amount_needed]
        return

    for current_amount in range(0, amount_needed + 1):
        for remaining_quantities in generate_quantities(amount_needed - current_amount, num_ingredients - 1):
            yield [current_amount] + remaining_quantities


def parse_input(raw_input: str) -> list[Ingredient]:
    return [parse_input_line(line) for line in raw_input.splitlines()]


def score_recipe(total: Ingredient) -> int:
    return max(total.capacity, 0) * max(total.durability, 0) * max(total.flavour, 0) * max(total.texture, 0)


def sum_ingredients(ingredients: Ingredients, quantities: Quantities) -> Ingredient:
    total = Ingredient(name="", capacity=0, durability=0, flavour=0, texture=0, calories=0)

    for index, ingredient in enumerate(ingredients):
        total += ingredient * quantities[index]

    return total


PATTERN = (
    "([A-z]+): capacity (\\-?[0-9]+), durability (\\-?[0-9]+), "
    "flavor (\\-?[0-9]+), texture (\\-?[0-9]+), calories (\\-?[0-9]+)"
)
REGEX = compile(PATTERN)


def parse_input_line(line: str) -> Ingredient:
    match = REGEX.match(line)

    if not match:
        raise RuntimeError(f"{line=} did not match {PATTERN=}")

    return Ingredient(
        name=match.group(1),
        capacity=int(match.group(2)),
        durability=int(match.group(3)),
        flavour=int(match.group(4)),
        texture=int(match.group(5)),
        calories=int(match.group(6)),
    )


EXAMPLE_INPUT = """Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"""

PUZZLE_INPUT = """Sprinkles: capacity 2, durability 0, flavor -2, texture 0, calories 3
Butterscotch: capacity 0, durability 5, flavor -3, texture 0, calories 3
Chocolate: capacity 0, durability 0, flavor 5, texture -1, calories 8
Candy: capacity 0, durability -1, flavor 0, texture 5, calories 8"""


@mark.parametrize(("raw_input", "expected_output"), [(EXAMPLE_INPUT, 62842880), (PUZZLE_INPUT, 21367368)])
def test_get_best_recipe_score(raw_input: str, expected_output: str) -> None:
    assert get_best_recipe_score(raw_input, None) == expected_output


@mark.parametrize(("raw_input", "expected_output"), [(EXAMPLE_INPUT, 57600000), (PUZZLE_INPUT, 1766400)])
def test_get_best_recipe_score_with_target_calories(raw_input: str, expected_output: str) -> None:
    assert get_best_recipe_score(raw_input, 500) == expected_output

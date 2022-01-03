from dataclasses import dataclass
from os.path import dirname, join
from typing import Callable

AttributeDict = dict[str, int]


@dataclass
class Aunt:
    number: int
    attributes: AttributeDict


AttributeMatcher = Callable[[Aunt, AttributeDict], bool]


def identify_aunt(
    actual_attributes: AttributeDict, aunts: list[Aunt], attribute_matcher: AttributeMatcher
) -> int | None:
    matching_aunt = next(aunt for aunt in aunts if attribute_matcher(aunt, actual_attributes))

    if matching_aunt:
        return matching_aunt.number

    return None


def simple_attribute_match(aunt: Aunt, actual_attributes: AttributeDict) -> bool:
    for attribute, value in actual_attributes.items():
        if attribute in aunt.attributes and value != aunt.attributes[attribute]:
            return False

    return True


def attribute_match_with_ranges(aunt: Aunt, actual_attributes: AttributeDict) -> bool:
    for attribute, value in actual_attributes.items():
        if attribute not in aunt.attributes:
            continue

        if attribute in {"cats", "trees"}:
            if aunt.attributes[attribute] <= value:
                return False
        elif attribute in {"goldfish", "pomeranians"}:
            if aunt.attributes[attribute] >= value:
                return False
        elif value != aunt.attributes[attribute]:
            return False

    return True


def parse_aunts(raw_input: str) -> list[Aunt]:
    return [parse_aunt(line) for line in raw_input.splitlines()]


def parse_aunt(line: str) -> Aunt:
    first_colon = line.index(":")
    initial_tokens = line[:first_colon].split(" ")
    attribute_tokens = line[first_colon + 2 :].split(", ")
    number = int(initial_tokens[1])
    attributes = {}

    for attribute_token in attribute_tokens:
        value_tokens = attribute_token.split(": ")
        attribute_name = value_tokens[0]
        attribute_value = int(value_tokens[1])
        attributes[attribute_name] = attribute_value

    return Aunt(number=number, attributes=attributes)


ACTUAL_ATTRIBUTES = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}
REMEMBERED_ATTRIBUTES = open(join(dirname(__file__), "puzzle_input.txt")).read()


def test_identify_aunt():
    aunts = parse_aunts(REMEMBERED_ATTRIBUTES)
    assert identify_aunt(ACTUAL_ATTRIBUTES, aunts, simple_attribute_match) == 103


def test_identify_aunt_with_ranges():
    aunts = parse_aunts(REMEMBERED_ATTRIBUTES)
    assert identify_aunt(ACTUAL_ATTRIBUTES, aunts, attribute_match_with_ranges) == 405

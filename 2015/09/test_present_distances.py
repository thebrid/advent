from collections import defaultdict
from collections.abc import Mapping, MutableMapping
from dataclasses import dataclass
from heapq import heapify, heappop, heappush

from pytest import mark

Distances = Mapping[str, Mapping[str, int]]
MutableDistances = MutableMapping[str, MutableMapping[str, int]]


@dataclass(frozen=True, order=True)
class QueueItem:
    distance: int
    path: tuple[str, ...]


def get_distance(raw_input: str, longest: bool) -> int | None:
    distances = parse_input(raw_input)
    return find_distance(distances, longest)


def find_distance(distances: Distances, longest: bool) -> int | None:
    all_cities = set(distances.keys())
    queue = [QueueItem(distance=0, path=(start_city,)) for start_city in all_cities]
    heapify(queue)

    while queue:
        queue_item = heappop(queue)

        visited = set(queue_item.path)

        if visited == all_cities:
            return -queue_item.distance if longest else queue_item.distance

        current_distance = queue_item.distance
        current_city = queue_item.path[-1]
        reachable_cities = distances[current_city]

        for reachable_city, leg_distance in reachable_cities.items():
            if reachable_city in visited:
                continue

            new_distance = current_distance - leg_distance if longest else current_distance + leg_distance

            heappush(queue, QueueItem(new_distance, queue_item.path + (reachable_city,)))

    return None


def parse_input(raw_input: str) -> Distances:
    output: MutableDistances = defaultdict(lambda: defaultdict(int))

    for line in raw_input.splitlines():
        tokens = line.split(" ")
        place1 = tokens[0]
        place2 = tokens[2]
        distance = int(tokens[4])
        output[place1][place2] = distance
        output[place2][place1] = distance

    return output


EXAMPLE_INPUT = """London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141"""

PUZZLE_INPUT = """AlphaCentauri to Snowdin = 66
AlphaCentauri to Tambi = 28
AlphaCentauri to Faerun = 60
AlphaCentauri to Norrath = 34
AlphaCentauri to Straylight = 34
AlphaCentauri to Tristram = 3
AlphaCentauri to Arbre = 108
Snowdin to Tambi = 22
Snowdin to Faerun = 12
Snowdin to Norrath = 91
Snowdin to Straylight = 121
Snowdin to Tristram = 111
Snowdin to Arbre = 71
Tambi to Faerun = 39
Tambi to Norrath = 113
Tambi to Straylight = 130
Tambi to Tristram = 35
Tambi to Arbre = 40
Faerun to Norrath = 63
Faerun to Straylight = 21
Faerun to Tristram = 57
Faerun to Arbre = 83
Norrath to Straylight = 9
Norrath to Tristram = 50
Norrath to Arbre = 60
Straylight to Tristram = 27
Straylight to Arbre = 81
Tristram to Arbre = 90"""


@mark.parametrize(("raw_input", "expected_output"), [(EXAMPLE_INPUT, 605), (PUZZLE_INPUT, 141)])
def test_get_shortest_distance(raw_input: str, expected_output: int) -> None:
    assert get_distance(raw_input, longest=False) == expected_output


@mark.parametrize(("raw_input", "expected_output"), [(EXAMPLE_INPUT, 982), (PUZZLE_INPUT, 736)])
def test_get_longest_distance(raw_input: str, expected_output: int) -> None:
    assert get_distance(raw_input, longest=True) == expected_output

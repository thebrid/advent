from pytest import mark


def count_container_combinations(containers: list[int], amount: int) -> int:
    return len(container_combinations(containers, amount))


def count_smallest_container_combinations(containers: list[int], amount: int) -> int:
    smallest_size = None
    smallest_count = 0

    for combination in container_combinations(containers, amount):
        if smallest_size is None or len(combination) < smallest_size:
            smallest_size = len(combination)
            smallest_count = 1
        elif len(combination) == smallest_size:
            smallest_count += 1

    return smallest_count


def container_combinations(containers: list[int], amount: int) -> list[list[int]]:
    if amount == 0:
        return [[]]

    if not containers:
        return []

    output = []

    if amount >= containers[0]:
        remaining_combinations = container_combinations(containers[1:], amount - containers[0])
        for remaining_combination in remaining_combinations:
            output.append([containers[0]] + remaining_combination)

    output.extend(container_combinations(containers[1:], amount))

    return output


EXAMPLE_INPUT = [20, 15, 10, 5, 5]
PUZZLE_INPUT = [11, 30, 47, 31, 32, 36, 3, 1, 5, 3, 32, 36, 15, 11, 46, 26, 28, 1, 19, 3]


@mark.parametrize(("containers", "amount", "expected_output"), [(EXAMPLE_INPUT, 25, 4), (PUZZLE_INPUT, 150, 4372)])
def test_eggnog_containers(containers: list[int], amount: int, expected_output: int) -> None:
    assert count_container_combinations(containers, amount) == expected_output


@mark.parametrize(("containers", "amount", "expected_output"), [(EXAMPLE_INPUT, 25, 3), (PUZZLE_INPUT, 150, 4)])
def test_count_smallest_container_combinations(containers: list[int], amount: int, expected_output: int) -> None:
    assert count_smallest_container_combinations(containers, amount) == expected_output

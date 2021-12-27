from hashlib import md5

from pytest import mark


def get_advent_coin(secret_key: str, num_leading_zeros: int) -> int:
    number_to_check = 1
    required_prefix = "0" * num_leading_zeros

    while True:
        hash_input = f"{secret_key}{number_to_check}"
        hash = md5(hash_input.encode("ascii"))

        if hash.hexdigest().startswith(required_prefix):
            return number_to_check

        number_to_check += 1


@mark.parametrize(
    ("secret_key", "num_leading_zeros", "expected_output"),
    [("abcdef", 5, 609043), ("pqrstuv", 5, 1048970), ("yzbqklnj", 5, 282749), ("yzbqklnj", 6, 9962624)],
)
def test_advent_coin(secret_key: str, num_leading_zeros: int, expected_output: int) -> None:
    assert get_advent_coin(secret_key, num_leading_zeros) == expected_output

from pytest import mark


def snafu_sum(input_string: str) -> str:
    total = 0

    for line in input_string.split("\n"):
        total += snafu_to_int(line)

    return int_to_snafu(total)


INT_TO_SNAFU = {-2: "=", -1: "-", 0: "0", 1: "1", 2: "2"}


def int_to_snafu(input_int: int) -> str:
    digits = list[str]()

    while input_int != 0:
        mod = input_int % 5

        if mod < 3:
            digits.insert(0, INT_TO_SNAFU[mod])
            input_int -= mod
        else:
            digits.insert(0, INT_TO_SNAFU[mod - 5])
            input_int -= mod - 5

        input_int //= 5

    return "".join(digits)


SNAFU_TO_INT = {value: key for key, value in INT_TO_SNAFU.items()}


def snafu_to_int(snafu: str) -> int:
    output = 0

    for char in snafu:
        output *= 5
        output += SNAFU_TO_INT[char]

    return output


TEST_INT_SNAFU_MAP = {
    1: "1",
    2: "2",
    3: "1=",
    4: "1-",
    5: "10",
    6: "11",
    7: "12",
    8: "2=",
    9: "2-",
    10: "20",
    11: "21",
    12: "22",
    13: "1==",
    14: "1=-",
    15: "1=0",
    16: "1=1",
    17: "1=2",
    18: "1-=",
    19: "1--",
    20: "1-0",
    21: "1-1",
    22: "1-2",
    23: "10=",
    24: "10-",
    25: "100",
    26: "101",
    27: "102",
    28: "11=",
    29: "11-",
    30: "110",
    31: "111",
    32: "112",
    2022: "1=11-2",
    12345: "1-0---0",
    314159265: "1121-1110-1=0",
}


@mark.parametrize(("input_int", "expected_snafu"), TEST_INT_SNAFU_MAP.items())
def test_int_to_snafu(input_int: int, expected_snafu: str) -> None:
    assert int_to_snafu(input_int) == expected_snafu


@mark.parametrize(("input_snafu", "expected_int"), [(snafu, integer) for integer, snafu in TEST_INT_SNAFU_MAP.items()])
def test_snafu_to_int(input_snafu: str, expected_int: int) -> None:
    assert snafu_to_int(input_snafu) == expected_int


EXAMPLE_INPUT = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""

PUZZLE_INPUT = """20=2=00=022-02
1=-=2--12==000=00-
1201-
2=-0==
1=1-=0-0001--2102=
1=0
1=101-
21022110=1=0=1=1=1
2002-=0
12-=1==1
1-121001
1==11
11-==
102202
2--0==
1-112-22
1-=2
21=00
120011=1====2
111-1012012=0=0112
2-2--1101
1-1=
1--1-002
2--221-1-212
22
1=--20=
1=2=--1-1
1=121--2==1
10
21==121
1110-2=10=0-=1=-=2
20==02=02-2111
12-1-122=--=2=-
12--0010=20
1=-0-2121120=-0=002
1===
1--22=22010=01011
22=20=02=-20
1-=1112=-0-
1---1-0-1021==01
11=0
1===-0=-0===021-=1
21=
210020-=20
1-11021=2=1
1--
1-10
2-01-00=2=
1--=-212-0
222011
1=1-=2100020
1202=2=-
2=-0
1=-02=2-===-==-002=
1===--=-1=2-1=0=
2-02
10-=-=2=20=1=-=-
20--210=2=020=2
1=12=2---=22--120-0=
1=-00=
1=2--1--=1=212
2=1
1-02-==-=01=
12=-121=11=21=1-1
2=21=2-=-22222=2
2-2
1-020
101-120--12=2002
1--1==-0=021
20121===11
2-
1=--2=-2==2=21
2-0200021--1
2=020=
1=12
1=2==10=12
1=11=1=-==101020=
111=00-
1==01
102=02--2
2-21
100=1=
11=-120=0
200-12-2=00101012-=
10=202
1011100=-12==1=2-00
21
1-=-202=-22102=0
1=-=21=-
1=2-1=1202-=
20-1121122=-=1201
10---=0==0-
112--2=
10=2211=1--=2---=0
1=0-01-01
2=2-2-121=01-1
1==-110
201=-0=-00==-21
2==11=11=1=
1=1-21=22--=2
2==2102-=-
2
22=--1===00221-
1--01221--21
2-2101=
10-1==22=21
1112-22====
11=0--1==211-001
1-2
112020
2=-000-=111=0
2===-2-=-0==
1--===21=1=1-101-
2=0111-=
102=1=1
1=10220212-=-2
1-10-=01
220-1
101-2
112"""


@mark.parametrize(
    ("input_string", "expected_snafu"),
    [
        (EXAMPLE_INPUT, "2=-1=0"),
        (PUZZLE_INPUT, "2-10==12-122-=1-1-22"),
    ],
)
def test_snafu_sum(input_string: str, expected_snafu: str) -> None:
    assert snafu_sum(input_string) == expected_snafu

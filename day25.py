"""Day 25: SNAFU"""

from pathlib import Path

DECODES = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}


ENCODES = "012=-"

TEST_INPUT = """1=-0-2
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
122""".splitlines()


def decode_snafu(snafu: str) -> str:
    result = 0
    for power, value in enumerate(reversed(snafu)):
        # print(f'{power=}, {value=}, {result=}')
        result += DECODES[value] * (5**power)
        # print(f'{result=}')
    return result


def encode_snafu(decimal_value: int) -> str:
    digits = []
    # print('encoding', decimal_value)
    while decimal_value:
        # print(f'{decimal_value=}')
        ones_digit = decimal_value % 5
        decimal_value //= 5
        digits.append(ENCODES[ones_digit])
        if ones_digit >= 3:
            decimal_value += 1
        # print(ones_digit, decimal_value, digits)

    # print(''.join(reversed(digits)).lstrip('0'))
    return "".join(reversed(digits)).lstrip("0")


def run_tests():
    for base_10, snafu in [
        (1, "1"),
        (2, "2"),
        (3, "1="),
        (4, "1-"),
        (5, "10"),
        (6, "11"),
        (7, "12"),
        (8, "2="),
        (9, "2-"),
        (10, "20"),
        (15, "1=0"),
        (20, "1-0"),
        (2022, "1=11-2"),
        (12345, "1-0---0"),
        (314159265, "1121-1110-1=0"),
    ]:
        assert decode_snafu(snafu=snafu) == base_10, (
            snafu,
            base_10,
            decode_snafu(snafu=snafu),
        )
        assert encode_snafu(decimal_value=base_10) == snafu, (
            snafu,
            base_10,
            encode_snafu(decimal_value=base_10),
        )


def part_one(puzzle: list[str]) -> str:
    value = 0
    for line in puzzle:
        value += decode_snafu(line)
    print("got value", value)
    return encode_snafu(value)


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == "2=-1=0", part_one_result
    puzzle = Path("day25.txt").read_text().splitlines()
    print(part_one(puzzle))


if __name__ == "__main__":
    run_tests()
    main()

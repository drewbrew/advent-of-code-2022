from pathlib import Path
from itertools import zip_longest

TEST_INPUT = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


PACKET_TYPE = int | list["PACKET_TYPE"]


def parse_input(puzzle: str) -> list[PACKET_TYPE]:
    pairs = []
    for pair in puzzle.split("\n\n"):
        left, right = (eval(i) for i in pair.splitlines())
        pairs.append([left, right])
    return pairs


def compare(left: PACKET_TYPE, right: PACKET_TYPE) -> int:
    match (left, right):
        case int(), int():
            return right - left
        case int(), list():
            return compare([left], right)
        case list(), int():
            return compare(left, [right])
        case list(), list():
            for left_value, right_value in zip(left, right):
                if (retval := compare(left_value, right_value)) != 0:
                    return retval
            return len(right) - len(left)
        case _:
            raise TypeError(f"Unknown types {type(left)} and {type(right)}")


def part_one(puzzle: str) -> int:
    pairs = parse_input(puzzle)
    score = 0
    for index, (left, right) in enumerate(pairs, start=1):
        if compare(left, right) > 0:
            score += index
    return score


def part_two(puzzle: str) -> int:
    """Figure out where [[2]] and [[6]] would slide in to the sorted list"""
    pairs = parse_input(puzzle)
    two_index = 1  # one-based counting
    six_index = 2  # and [[6]] has to come after [[2]]
    # we don't actually have to worry about sorting the entire list,
    # only figuring out where the two bonus packets would slide into
    # place

    # we can start counting at 1 and place [[2]], [[6]] in that order
    # which gives us the start values of 1 and 2 above
    for left, right in pairs:
        two_index += 1 if compare(left, [[2]]) > 0 else 0
        two_index += 1 if compare(right, [[2]]) > 0 else 0
        six_index += 1 if compare(left, [[6]]) > 0 else 0
        six_index += 1 if compare(right, [[6]]) > 0 else 0
    return two_index * six_index


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 13, part_one_result
    real_puzzle = Path("day13.txt").read_text()
    print(part_one(real_puzzle))
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 140, part_two_result
    print(part_two(real_puzzle))


if __name__ == "__main__":
    main()

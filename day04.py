"""Day 4: cleanup on aisle 4"""

from pathlib import Path

TEST_INPUT = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8""".splitlines()


def parse_input(puzzle: list[str]) -> list[tuple[int, int, int, int]]:
    parsed = []
    for line in puzzle:
        range1, range2 = line.split(",")
        start1, end1 = (int(i) for i in range1.split("-"))
        start2, end2 = (int(i) for i in range2.split("-"))
        parsed.append((start1, end1, start2, end2))
    return parsed


def part_one(puzzle: list[tuple[int, int, int, int]]):
    supersets = 0
    for start1, end1, start2, end2 in puzzle:
        if (start1 >= start2 and end1 <= end2) or (start1 <= start2 and end1 >= end2):
            supersets += 1
    return supersets


def part_two(puzzle: list[tuple[int, int, int, int]]):
    overlaps = 0
    for start1, end1, start2, end2 in puzzle:
        set1 = set(range(start1, end1 + 1))
        set2 = set(range(start2, end2 + 1))
        if set1.intersection(set2):
            overlaps += 1
    return overlaps


def main():
    real_input = Path("day04.txt").read_text().splitlines()
    test_puzzle = parse_input(TEST_INPUT)
    real_puzzle = parse_input(real_input)
    assert part_one(test_puzzle) == 2, part_one(test_puzzle)
    print(part_one(real_puzzle))
    assert part_two(test_puzzle) == 4, part_two(test_puzzle)
    print(part_two(real_puzzle))


if __name__ == "__main__":
    main()

"""Day 1: how many snacks are these elves packing?"""
from pathlib import Path


TEST_INPUT = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000""".splitlines()


def parse_input(lines: list[str]) -> list[int]:
    elves = []
    interim = 0
    for line in lines:
        line = line.strip()
        if not line:
            elves.append(interim)
            interim = 0
        else:
            interim += int(line)
    elves.append(interim)
    return elves


def part_one(puzzle_input: list[str]) -> int:
    elves = parse_input(puzzle_input)
    return max(elves)


def part_two(puzzle_input: list[str]) -> int:
    elves = parse_input(puzzle_input)
    elves = sorted(elves, reverse=True)
    return sum(elves[:3])


def main():
    assert part_one(TEST_INPUT) == 24000, part_one(TEST_INPUT)
    puzzle_file = Path("day01.txt")
    puzzle_data = puzzle_file.read_text().splitlines()
    print(part_one(puzzle_data))
    assert part_two(TEST_INPUT) == 45000, part_two(TEST_INPUT)
    print(part_two(puzzle_data))


if __name__ == "__main__":
    main()

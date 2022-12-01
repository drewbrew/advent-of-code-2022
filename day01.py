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
    reindeer = []
    interim = 0
    for line in lines:
        line = line.strip()
        if not line:
            reindeer.append(interim)
            interim = 0
        else:
            interim += int(line)
    reindeer.append(interim)
    return reindeer


def part_one(puzzle_input: list[str]) -> int:
    reindeer = parse_input(puzzle_input)
    return max(reindeer)


def part_two(puzzle_input: list[str]) -> int:
    reindeer = parse_input(puzzle_input)
    reindeer = sorted(reindeer, reverse=True)
    return sum(reindeer[:3])


def main():
    assert part_one(TEST_INPUT) == 24000, part_one(TEST_INPUT)
    puzzle_file = Path("day01.txt")
    puzzle_data = puzzle_file.read_text().splitlines()
    print(part_one(puzzle_data))
    assert part_two(TEST_INPUT) == 45000, part_two(TEST_INPUT)
    print(part_two(puzzle_data))


if __name__ == "__main__":
    main()

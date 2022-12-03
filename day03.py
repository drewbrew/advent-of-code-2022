"""Day 3: rucksack reorg"""

from pathlib import Path
from collections.abc import Generator


TEST_INPUT = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""".splitlines()


def rucksack_priority(rucksack: str) -> int:
    split = len(rucksack) // 2
    assert len(rucksack) / 2 == split
    pack1 = rucksack[:split]
    pack2 = rucksack[split:]
    union = set(pack1) & set(pack2)
    assert len(union) == 1, union
    commonality = union.pop()
    if commonality.lower() == commonality:
        return ord(commonality) - ord("a") + 1
    return ord(commonality) - ord("A") + 27


def part_one(puzzle: list[str]) -> int:
    return sum(rucksack_priority(sack) for sack in puzzle)


def chunks(lst: list[int], n: int) -> Generator[str, None, None]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def part_two(puzzle: list[str]) -> int:
    total = 0
    for sack1, sack2, sack3 in chunks(puzzle, 3):
        union = set(sack1) & set(sack2) & set(sack3)
        assert len(union) == 1, union
        commonality = union.pop()
        if commonality.lower() == commonality:
            total += ord(commonality) - ord("a") + 1
        else:
            total += ord(commonality) - ord("A") + 27
    return total


def main():
    assert part_one(TEST_INPUT) == 157, part_one(TEST_INPUT)
    real_input = Path("day03.txt").read_text().splitlines()
    print(part_one(real_input))
    assert part_two(TEST_INPUT) == 70, part_two(TEST_INPUT)
    print(part_two(real_input))


if __name__ == "__main__":
    main()

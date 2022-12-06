"""Day 6: tuning trouble"""

from pathlib import Path

TEST_INPUTS = {
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb": (7, 19),
    "bvwbjplbgvbhsrlpgdmjqwftvncz": (5,23),
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": (10, 29),
    "nppdvjthqldpwncqszvftbrmjlhg": (6, 23),
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": (11, 26),
}


def part_one(puzzle: str) -> int:
    """How many characters in do we have to get before getting 4 distinct chars?"""
    for index in range(4, len(puzzle) + 1):
        last_4 = puzzle[index - 4:index]
        assert len(last_4) == 4
        if len(set(last_4)) == 4:
            return index


def part_two(puzzle: str) -> int:
    """How many characters in do we have to get before getting 14 distinct chars?"""
    for index in range(14, len(puzzle) + 1):
        last_14 = puzzle[index - 14:index]
        assert len(last_14) == 14
        if len(set(last_14)) == 14:
            return index


def main():
    for puzzle, (answer, p2_answer) in TEST_INPUTS.items():
        assert part_one(puzzle) == answer, (puzzle, answer, part_one(puzzle))
        assert part_two(puzzle) == p2_answer, (puzzle, p2_answer, part_two(puzzle))
    real_puzzle = Path('day06.txt').read_text().strip()
    print(part_one(real_puzzle))
    print(part_two(real_puzzle))



if __name__ == '__main__':
    main()

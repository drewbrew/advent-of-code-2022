"""Day 6: tuning trouble"""

from pathlib import Path

TEST_INPUTS = {
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb": (7, 19),
    "bvwbjplbgvbhsrlpgdmjqwftvncz": (5,23),
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": (10, 29),
    "nppdvjthqldpwncqszvftbrmjlhg": (6, 23),
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": (11, 26),
}

def min_offset_before_distinct_chars(puzzle: str, min_distinct: int) -> int:
    for index in range(min_distinct, len(puzzle) + 1):
        most_recent = puzzle[index - min_distinct:index]
        assert len(most_recent) == min_distinct
        if len(set(most_recent)) == min_distinct:
            return index

def part_one(puzzle: str) -> int:
    """How many characters in do we have to get before getting 4 distinct chars?"""
    return min_offset_before_distinct_chars(puzzle, 4)

def part_two(puzzle: str) -> int:
    """How many characters in do we have to get before getting 14 distinct chars?"""
    return min_offset_before_distinct_chars(puzzle, 14)


def main():
    for puzzle, (answer, p2_answer) in TEST_INPUTS.items():
        assert part_one(puzzle) == answer, (puzzle, answer, part_one(puzzle))
        assert part_two(puzzle) == p2_answer, (puzzle, p2_answer, part_two(puzzle))
    real_puzzle = Path('day06.txt').read_text().strip()
    print(part_one(real_puzzle))
    print(part_two(real_puzzle))



if __name__ == '__main__':
    main()

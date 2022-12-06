"""Day 5: cranes"""

from string import ascii_uppercase
from pathlib import Path

TEST_INPUT = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2""".splitlines()


def crate_number(line_index: int) -> int:
    # 1 -> 1
    # 5 -> 2
    # 8 -> 3
    # ...
    return (line_index - 1) // 4 + 1


def parse_input(
    puzzle: list[str],
) -> tuple[list[list[str]], list[tuple[int, int, int]]]:
    # my test input has 1 through 9, so this is a cheat
    crates = [list() for _ in range(10)]
    instructions = []

    parsing_crates = True

    for line in puzzle:
        if not line:
            continue
        if line.startswith("move"):
            parsing_crates = False
        if parsing_crates:
            for index, char in enumerate(line):
                if char in ascii_uppercase:
                    # we have a crate
                    crate = crate_number(index)
                    crates[crate].append(char)
        else:
            words = line.split()
            instructions.append((int(words[1]), int(words[3]), int(words[5])))
    for crate in crates:
        # Here's the big key for the puzzle:
        # the lines you read are in reverse order
        # so you need to reverse each crate container
        crate.reverse()
    return crates, instructions


def move_crate(crates: list[list[str]], qty: int, source: int, target: int):
    assert source != target
    for _ in range(qty):
        crates[target].append(crates[source].pop())


def move_crate_p2(crates: list[list[str]], qty: int, source: int, target: int):
    assert source != target
    removed = crates[source][-qty:]
    del crates[source][-qty:]
    crates[target].extend(removed)


def part_one(crates: list[list[str]], instructions: list[tuple[int, int, int]]) -> str:
    for qty, source, target in instructions:
        move_crate(crates, qty, source, target)
    return "".join(crate[-1] for crate in crates if crate)


def part_two(crates: list[list[str]], instructions: list[tuple[int, int, int]]) -> str:
    for qty, source, target in instructions:
        move_crate_p2(crates, qty, source, target)
    return "".join(crate[-1] for crate in crates if crate)


def main():
    test_crates, test_instructions = parse_input(TEST_INPUT)
    part_one_result = part_one(test_crates, test_instructions)
    assert part_one_result == "CMZ"

    real_puzzle = Path("day05.txt").read_text().splitlines()
    real_crates, real_instructions = parse_input(real_puzzle)

    print(part_one(real_crates, real_instructions))
    test_crates, test_instructions = parse_input(TEST_INPUT)

    # simply slicing (e.g. test_crates[:]) is not enough to preserve
    # the original list because it'll still point to the same interior
    # lists
    part_two_result = part_two(test_crates, test_instructions)
    assert part_two_result == "MCD", part_two_result

    real_crates, real_instructions = parse_input(real_puzzle)
    print(part_two(real_crates, real_instructions))


if __name__ == "__main__":
    main()

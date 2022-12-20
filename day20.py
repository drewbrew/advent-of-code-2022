from pathlib import Path
from collections import deque


TEST_INPUT = """1
2
-3
3
-2
0
4""".splitlines()

DECRYPTION_KEY = 811589153


def mix(puzzle: deque[tuple[int, int]]) -> deque[tuple[int, int]]:

    output = puzzle
    for index in range(len(puzzle)):
        while index != output[0][0]:
            output.rotate(-1)
        index1, number = output.popleft()
        output.rotate(-number)
        output.appendleft((index1, number))
        output.rotate(number)
    return output


def part_one(puzzle: list[str]) -> int:
    # store a tuple of the instruction index and the value
    # this wasn't technically necessary for part 1, but
    # it made part two easier to reuse the same function
    instructions = deque((index, int(i)) for index, i in enumerate(puzzle))
    mixed = mix(instructions)
    score = 0
    while mixed[0][1] != 0:
        mixed.rotate(-1)
    assert mixed[0][1] == 0

    for _ in range(3):
        mixed.rotate(-1000)
        score += mixed[0][1]
    return score


def part_two(puzzle: list[str]) -> int:
    instructions = deque(
        (index, int(i) * DECRYPTION_KEY) for index, i in enumerate(puzzle)
    )
    for _ in range(10):
        instructions = mix(instructions)
    score = 0
    while instructions[0][1] != 0:
        instructions.rotate(-1)
    assert instructions[0][1] == 0

    for _ in range(3):
        instructions.rotate(-1000)
        score += instructions[0][1]
    return score


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 3, part_one_result
    puzzle = Path("day20.txt").read_text().splitlines()
    print(part_one(puzzle))
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 1623178306, part_two_result
    print(part_two(puzzle=puzzle))


if __name__ == "__main__":
    main()

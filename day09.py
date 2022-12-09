from pathlib import Path

TEST_INPUT = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""".splitlines()

PART_TWO_TEST_INPUT = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""".splitlines()


def parse_input(puzzle: list[str]) -> list[tuple[complex, int]]:
    output = []
    directions = {
        "R": 1 + 0j,
        "L": -1 + 0j,
        "U": 0 + 1j,
        "D": 0 - 1j,
    }
    for line in puzzle:
        base_direction, base_amount = line.strip().split()
        output.append((directions[base_direction], int(base_amount)))
    return output


def follow_head(head: complex, tail: complex) -> complex:
    """Return which direction the head must move to follow the tail"""
    if head == tail:
        return 0j
    if abs(int(head.imag - tail.imag)) <= 1 and abs(int(head.real - tail.real)) <= 1:
        # if we're within one space, no need to move
        return 0j
    if head.real == tail.real:
        if head.imag > tail.imag:
            # move up
            return 1j
        # move down
        return -1j
    elif head.imag == tail.imag:
        if head.real > tail.real:
            # move right
            return 1 + 0j
        # move left
        return -1 - 0j
    # now we need to move diagonally
    elif head.real > tail.real:
        # we need to move right
        if head.imag > tail.imag:
            # move right and up
            return 1 + 1j
        # move right and down
        return 1 - 1j
    else:
        assert head.real < tail.real
        # move left
        if head.imag > tail.imag:
            # move left and up
            return -1 + 1j
        # left and down
        return -1 - 1j


def part_one(puzzle: list[str]) -> int:
    steps = parse_input(puzzle=puzzle)
    head = 0j
    tail = 0j
    points_seen: set[complex] = {tail}
    for direction, number_of_steps in steps:
        while number_of_steps > 0:
            head += direction
            tail += follow_head(head, tail)
            number_of_steps -= 1

            points_seen.add(tail)

    return len(points_seen)


def part_two(puzzle: list[str]) -> int:
    steps = parse_input(puzzle=puzzle)
    head = 0j
    tail1 = 0j
    tail2 = 0j
    tail3 = 0j
    tail4 = 0j
    tail5 = 0j
    tail6 = 0j
    tail7 = 0j
    tail8 = 0j
    tail9 = 0j
    points_seen: set[complex] = {tail9}
    for direction, number_of_steps in steps:
        while number_of_steps > 0:
            head += direction
            tail1 += follow_head(head, tail1)
            tail2 += follow_head(tail1, tail2)
            tail3 += follow_head(tail2, tail3)
            tail4 += follow_head(tail3, tail4)
            tail5 += follow_head(tail4, tail5)
            tail6 += follow_head(tail5, tail6)
            tail7 += follow_head(tail6, tail7)
            tail8 += follow_head(tail7, tail8)
            tail9 += follow_head(tail8, tail9)
            number_of_steps -= 1

            points_seen.add(tail9)

            # print(head, tail1, tail2, tail3, tail4, tail5, tail6, tail7, tail8, tail9)

    return len(points_seen)


def main():
    part_one_result = part_one(TEST_INPUT)
    assert follow_head((4 + 1j), (3 + 0j)) == 0j, follow_head((4 + 1j), (3 + 0j))
    assert part_one_result == 13, part_one_result
    puzzle = Path("day09.txt").read_text().splitlines()
    print(part_one(puzzle=puzzle))
    part_two_result = part_two(PART_TWO_TEST_INPUT)
    assert part_two_result == 36, part_two_result
    print(part_two(puzzle=puzzle))


if __name__ == "__main__":
    main()

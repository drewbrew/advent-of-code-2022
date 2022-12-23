from pathlib import Path
from collections import deque, Counter
from typing import Callable


SMALL_INPUT = """.....
..##.
..#..
.....
..##.
.....""".splitlines()

TEST_INPUT = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..""".splitlines()


COORDINATE_TYPE = tuple[int, int]

GRID_TYPE = set[COORDINATE_TYPE]


def move_elf(
    grid: GRID_TYPE,
    elf: COORDINATE_TYPE,
    funcs: deque[Callable[[GRID_TYPE, COORDINATE_TYPE], None | COORDINATE_TYPE]],
) -> COORDINATE_TYPE:
    x, y = elf
    # 1. are all the spaces around them empty?
    if not any(
        neighbor in grid
        for neighbor in [
            (x + 1, y - 1),
            (x + 1, y),
            (x + 1, y + 1),
            (x, y + 1),
            (x, y - 1),
            (x - 1, y + 1),
            (x - 1, y),
            (x - 1, y - 1),
        ]
    ):
        # do nothing
        return elf
    for func in list(funcs):
        result = func(grid, elf)

        if result is not None:
            assert isinstance(result, tuple)
            return result
    return elf


def propose_north(grid: GRID_TYPE, elf: COORDINATE_TYPE) -> None | COORDINATE_TYPE:
    x, y = elf
    # 2. are all the northern neighbors open?
    if not any(
        neighbor in grid
        for neighbor in [
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
        ]
    ):
        # move up
        return x, y - 1


def propose_south(grid: GRID_TYPE, elf: COORDINATE_TYPE) -> None | COORDINATE_TYPE:
    x, y = elf

    # 3. are  all the southern neighbors open?
    if not any(
        neighbor in grid
        for neighbor in [
            (x - 1, y + 1),
            (x, y + 1),
            (x + 1, y + 1),
        ]
    ):
        # move down
        return x, y + 1


def propose_west(grid: GRID_TYPE, elf: COORDINATE_TYPE) -> None | COORDINATE_TYPE:
    x, y = elf

    # 4: are all the western neighbors open?
    if not any(
        neighbor in grid
        for neighbor in [
            (x - 1, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
        ]
    ):
        # move left
        return x - 1, y


def propose_east(grid: GRID_TYPE, elf: COORDINATE_TYPE) -> None | COORDINATE_TYPE:
    x, y = elf
    # 5. are all the eastern neighbors open?
    if not any(
        neighbor in grid
        for neighbor in [
            (x + 1, y - 1),
            (x + 1, y),
            (x + 1, y + 1),
        ]
    ):
        # move right
        return x + 1, y


def parse_input(puzzle: list[str]) -> GRID_TYPE:
    result = set()
    for y, row in enumerate(puzzle):
        for x, char in enumerate(row):
            if char == "#":
                result.add((x, y))
    return result


def part_one(puzzle: list[str], rounds: int = 10) -> int:
    grid = parse_input(puzzle)
    funcs = deque([propose_north, propose_south, propose_west, propose_east])
    for round in range(1, rounds + 1):
        if rounds != 10:
            print("new turn", round, end="\r")
        proposed_moves = [(elf, move_elf(grid, elf, funcs=funcs)) for elf in grid]
        destinations = Counter(coordinate for _, coordinate in proposed_moves)
        new_grid: GRID_TYPE = set()
        for elf, destination in proposed_moves:
            assert isinstance(destination, tuple), (elf, destination)
            if destinations[destination] == 1:
                new_grid.add(destination)
            else:
                # cancel the  move
                new_grid.add(elf)
        assert len(grid) == len(new_grid), new_grid
        if new_grid == grid:
            print("found a dead stop!")
            return round
        grid = new_grid
        funcs.rotate(-1)
        # display_grid(new_grid)

    return empty_tiles(grid)


def empty_tiles(grid: GRID_TYPE) -> int:
    x_values = sorted(x for x, _ in grid)
    y_values = sorted(y for _, y in grid)
    min_x = x_values[0]
    max_x = x_values[-1] + 1
    min_y = y_values[0]
    max_y = y_values[-1] + 1
    return sum(
        (x, y) not in grid for y in range(min_y, max_y) for x in range(min_x, max_x)
    )


def display_grid(grid: GRID_TYPE):
    x_values = sorted(x for x, _ in grid)
    y_values = sorted(y for _, y in grid)
    min_x = x_values[0]
    max_x = x_values[-1] + 1
    min_y = y_values[0]
    max_y = y_values[-1] + 1
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            if (x, y) in grid:
                print("#", end="")
            else:
                print(" ", end="")
        print("")


def main():
    part_one_result = part_one(puzzle=TEST_INPUT)
    assert part_one_result == 110, part_one_result
    puzzle = Path("day23.txt").read_text().splitlines()
    print(part_one(puzzle))
    part_two_result = part_one(puzzle=TEST_INPUT, rounds=50)
    assert part_two_result == 20, part_two_result
    print(part_one(puzzle, rounds=1000000))


if __name__ == "__main__":
    main()

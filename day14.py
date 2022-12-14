"""Day 14: Regolith Reservoir"""

import sys
from pathlib import Path
from time import sleep

TEST_INPUT = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9""".splitlines()


START = 500, 0
COORDINATE_TYPE = tuple[int, int]


def parse_input(puzzle: list[str]) -> set(COORDINATE_TYPE):
    last_coordinate = 0, 0
    coordinates = set()

    for line in puzzle:
        text_coords = line.strip().split(" -> ")
        for coord in text_coords:
            x, y = (int(i) for i in coord.split(","))
            if last_coordinate != (0, 0):
                last_x, last_y = last_coordinate
                if last_x == x:
                    # moving horizontally
                    y1, y2 = sorted([y, last_y])
                    coordinates |= {(x, dy) for dy in range(y1, y2 + 1)}
                else:
                    assert last_y == y, (x, y, last_x, last_y)
                    x1, x2 = sorted([x, last_x])
                    coordinates |= {(dx, y) for dx in range(x1, x2 + 1)}
            last_coordinate = x, y
        last_coordinate = 0, 0
    return coordinates


def drop_sand(
    grid: set(COORDINATE_TYPE), starting_coordinate: COORDINATE_TYPE = START
) -> COORDINATE_TYPE:
    """Drop a grain of sand"""
    the_bottom = max(y for _, y in grid) + 1
    x, y = starting_coordinate
    while y < the_bottom:
        if (x, y + 1) not in grid:
            # keep going until we hit something
            y += 1
            continue
        # ok, we've hit something
        if (x - 1, y + 1) not in grid:
            # can we move left?
            x -= 1
            y += 1
            continue
        # can we move right?
        if (x + 1, y + 1) not in grid:
            # yes
            x += 1
            y += 1
            continue
        # nope, can't move at all
        return x, y
    # AAAAAAAAAH!
    raise IntoTheAbyss()


def part_two(puzzle: list[str], visualize: bool = False) -> int:
    """Same as part one, only now there's an infinite floor two levels below our last scan"""
    grains = 0
    grid = parse_input(puzzle=puzzle)
    the_bottom = max(y for _, y in grid) + 2
    x_values = sorted(x for x, _ in grid)
    # if we spread out an extra 300 in each dimension from our widest point
    # that should more than cover it

    # I had tried 3 for the test input but that wasn't enough, then I tried
    # 30 and that was enough for the test input but not the real input
    # after running it, the grid only went out to about 330 on the left and 675
    # on the right
    min_x = x_values[0] - 175
    max_x = x_values[-1] + 175
    grid |= {(dx, the_bottom) for dx in range(min_x, max_x)}
    if visualize:
        visualized = {coordinate: "#" for coordinate in grid}
    while True:
        new_point = drop_sand(grid)
        grains += 1
        if new_point == START:
            # print('blocked!')
            if visualize:
                display_grid(visualized, START[0] - 175, START[0] + 175)
            return grains
        # print(f'drop number {grains} landed at {new_point}')
        grid.add(new_point)
        if visualize:
            visualized[new_point] = "o"
            if not grains % 100:
                display_grid(visualized, START[0] - 175, START[0] + 175)


def display_grid(grid: dict[COORDINATE_TYPE, str], min_x: int, max_x: int):
    min_y = 0
    max_y = max(i[1] for i in grid)
    # move to top left and clear screen
    print(chr(27) + "[2j")
    print("\033c")
    print("\x1bc")
    for y in range(min_y, max_y + 2):

        for x in range(min_x, max_x + 1):
            print(grid.get((x, y), " "), end="")
        print("")


def part_one(puzzle: list[str]) -> int:
    grains = 0
    grid = parse_input(puzzle=puzzle)
    try:
        while True:
            new_point = drop_sand(grid)
            grains += 1
            # print(f'drop number {grains} landed at {new_point}')
            grid.add(new_point)
    except IntoTheAbyss:
        return grains


class IntoTheAbyss(Exception):
    """The drop of sand will fall into the abyss"""


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 24, part_one_result
    puzzle = Path("day14.txt").read_text().splitlines()
    print(part_one(puzzle))
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 93, part_two_result
    print(part_two(puzzle=puzzle, visualize="--display" in sys.argv))


if __name__ == "__main__":
    main()

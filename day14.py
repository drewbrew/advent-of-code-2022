"""Day 14: Regolith Reservoir"""

from pathlib import Path

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


def part_two(puzzle: list[str]) -> int:
    """Same as part one, only now there's an infinite floor two levels below our last scan"""
    grains = 0
    grid = parse_input(puzzle=puzzle)
    the_bottom = max(y for _, y in grid) + 2
    x_values = sorted(x for x, _ in grid)
    # if we spread out an extra 300 in each dimension from our widest point
    # that should more than cover it

    # I had tried 3 for the test input but that wasn't enough, then I tried
    # 30 and that was enough for the test input but not the real input
    min_x = x_values[0] - 300
    max_x = x_values[-1] + 301
    grid |= {(dx, the_bottom) for dx in range(min_x, max_x)}

    while True:
        new_point = drop_sand(grid)
        grains += 1
        if new_point == START:
            # print('blocked!')
            return grains
        # print(f'drop number {grains} landed at {new_point}')
        grid.add(new_point)


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
    print(part_two(puzzle=puzzle))


if __name__ == "__main__":
    main()

from pathlib import Path

TEST_INPUT = """30373
25512
65332
33549
35390""".splitlines()

CoordinateType = complex
GridType = dict[CoordinateType, int]


def parse_input(puzzle: list[str]) -> GridType:
    grid = {}
    for y, row in enumerate(puzzle):
        for x, char in enumerate(row.strip()):
            grid[x + (y * 1j)] = int(char)
    return grid


def walk_coordinates(
    grid: GridType, coordinates: list[CoordinateType]
) -> set[CoordinateType]:
    """Given a list of coordinates (in order by direction coming from the edge),
    return a set of coordinates that are visible from that edge"""
    tallest_tree = max(grid.values())
    # coherence check: are our grids sorted?

    if len({i.real for i in coordinates}) == 1:
        imag_list = [int(i.imag) for i in coordinates]
        assert imag_list in (
            sorted(imag_list),
            sorted(imag_list, reverse=True),
        ), imag_list
    else:
        assert len({i.imag for i in coordinates}) == 1, coordinates
        real_list = [int(i.real) for i in coordinates]
        assert real_list in (sorted(real_list), sorted(real_list, reverse=True))
    tallest_tree_seen_yet = -1  # start with an impossible value
    retval: set[CoordinateType] = set()
    # now walk along that list...
    for coordinate in coordinates:
        # until we hit something that's taller than our last seen tallest tree
        if (height := grid[coordinate]) > tallest_tree_seen_yet:
            # save it and set our new
            retval.add(coordinate)
            tallest_tree_seen_yet = height
            if height == tallest_tree:
                # we can't go any further in this direction
                return retval
    return retval


def scenic_score(grid: GridType, coordinate: CoordinateType) -> int:
    # by rule, edges have a zero score
    if coordinate.real == 0 or coordinate.imag == 0:
        return 0
    max_y = max(int(i.imag) for i in grid)
    if coordinate.imag == max_y:
        return 0
    max_x = max(int(i.real) for i in grid)
    if coordinate.real == max_x:
        return 0
    score = 1
    height = grid[coordinate]
    # down, up, right, left (B, A, select, start?)
    directions = [1j, -1j, 1 + 0j, -1 + 0j]
    for direction in directions:
        direction_score = 0
        new_coordinate = coordinate + direction
        # keep walking until we fall off the edge...
        while (new_height := grid.get(new_coordinate)) is not None:
            direction_score += 1
            # or a tree that isn't shorter than the one we're looking at
            if new_height >= height:
                break
            # and keep walking
            new_coordinate += direction
        # then per the rules, multiply that to our existing score
        score *= direction_score
    return score


def part_one(puzzle: list[str]) -> int:
    grid = parse_input(puzzle=puzzle)
    visibles: set[CoordinateType] = set()
    max_y = max(int(i.imag) for i in grid)
    max_x = max(int(i.real) for i in grid)
    # we have to walk in from each edge going down, right, left, and up
    # for each value of x, y, y, and x, respectively
    # and since I used complex values for the lists, I can't just use ranges
    down_lists = [[x + (y * 1j) for y in range(max_y + 1)] for x in range(max_x + 1)]
    up_lists = [[x + (y * 1j) for y in range(max_y, -1, -1)] for x in range(max_x + 1)]
    left_lists = [
        [x + (y * 1j) for x in range(max_x, -1, -1)] for y in range(max_y + 1)
    ]
    right_lists = [[x + (y * 1j) for x in range(max_x + 1)] for y in range(max_y + 1)]
    # make sure no off-by-one errors in the ranges above
    assert len(down_lists) == len(puzzle), down_lists
    assert len(down_lists[0]) == len(puzzle)
    assert len(right_lists) == len(puzzle)
    assert len(left_lists) == len(puzzle)
    assert len(up_lists) == len(puzzle)
    for direction in [left_lists, up_lists, down_lists, right_lists]:
        for coordinate_list in direction:
            visibles |= walk_coordinates(grid, coordinate_list)
    return len(visibles)


def part_two(puzzle: list[str]) -> int:
    grid = parse_input(puzzle)
    # yeah, I could optimize this a little, but it runs in about 8 sec
    return max(scenic_score(grid, coordinate) for coordinate in grid)


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 21, part_one_result
    puzzle = Path("day08.txt").read_text().splitlines()
    print(part_one(puzzle=puzzle))
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 8, part_two_result
    print(part_two(puzzle))


if __name__ == "__main__":
    main()

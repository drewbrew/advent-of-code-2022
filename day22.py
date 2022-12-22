from pathlib import Path

TEST_INPUT = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

RIGHT = 1 + 0j
LEFT = -1 + 0j
UP = 1j
DOWN = -1j

COORDINATE_TYPE = complex
DIRECTION_SCORES = {
    RIGHT: 0,  # right
    DOWN: 1,  # down
    LEFT: 2,  # left
    UP: 3,  # up
}

DIRECTION_CHARS = {
    RIGHT: ">",
    LEFT: "<",
    UP: "^",
    DOWN: "v",
}


def parse_input(puzzle: str) -> tuple[str, dict[COORDINATE_TYPE, str]]:
    the_map, directions = puzzle.split("\n\n")
    grid: dict[COORDINATE_TYPE, str] = {}
    for y, row in enumerate(the_map.splitlines(), start=1):
        for x, char in enumerate(row, start=1):
            if char == " ":
                continue
            coordinate = x - (1j * y)
            grid[coordinate] = char
    return directions.strip(), grid


def turn(initial_direction: complex, turn_command: str) -> complex:
    if turn_command == "R":
        return initial_direction * -1j
    assert turn_command == "L", turn_command
    return initial_direction * 1j


def score(position: COORDINATE_TYPE, direction: complex) -> int:
    return (
        1000 * -int(position.imag)
        + 4 * int(position.real)
        + DIRECTION_SCORES[direction]
    )


def move(
    grid: dict[COORDINATE_TYPE, str],
    position: COORDINATE_TYPE,
    direction: complex,
    steps: int,
) -> COORDINATE_TYPE:
    for _ in range(steps):
        try:
            next_grid_spot = grid[position + direction]
        except KeyError:
            # need to loop
            match direction:
                case 1j:
                    # facing up, so need to get to the bottom
                    x = int(position.real)
                    y = min(int(coord.imag) for coord in grid if coord.real == x)
                    new_pos = x + 1j * y
                case -1j:
                    # facing down
                    x = int(position.real)
                    y = max(int(coord.imag) for coord in grid if coord.real == x)
                    new_pos = x + 1j * y
                case 1 + 0j:
                    # right
                    y = int(position.imag)
                    x = min(int(coord.real) for coord in grid if coord.imag == y)
                    new_pos = x + 1j * y
                case _:
                    # left
                    assert direction == LEFT, direction
                    y = int(position.imag)
                    x = max(int(coord.real) for coord in grid if coord.imag == y)
                    new_pos = x + 1j * y
            next_grid_spot = grid[new_pos]
        else:
            new_pos = position + direction
        if next_grid_spot == "#":
            # blocked!
            return position
        position = new_pos
    return position


def move_p2(
    grid: dict[COORDINATE_TYPE, str],
    position: COORDINATE_TYPE,
    direction: complex,
    steps: int,
    cube_size: int,
) -> tuple[COORDINATE_TYPE, complex]:
    assert position in grid
    for _ in range(steps):
        new_direction = direction
        try:
            next_grid_spot = grid[position + direction]
        except KeyError:

            # need to move to a different surface
            match direction:
                case 1j:
                    # currently facing up
                    if int(position.imag) == -1:
                        # at the very top
                        if int(position.real) <= 100:
                            # moving to the bottom left, facing right
                            new_direction = RIGHT
                            # 51 - 1j -> 1 - 151j
                            # 52 - 1j -> 1 - 152j
                            # ...
                            y = -100 - int(position.real)
                            x = 1
                            new_pos = x + 1j * y
                        else:
                            # moving to the bottom left but still facing up
                            x = int(position.real) - 100
                            y = -200
                            new_pos = x + 1j * y
                    else:
                        assert int(position.imag) == -101
                        # now in the middle of the center section, facing right
                        # 1 - 101j -> 51 - 51j
                        # 2 - 101j -> 51 - 52j
                        new_direction = RIGHT
                        x = 51
                        y = -50 - int(position.real)
                        new_pos = x + 1j * y
                case -1j:
                    # going down
                    # 3 cases to consider here:
                    # 1. bottom of the upper right section
                    if int(position.imag) == -50:
                        # now face left (stand in the place where you are!)
                        new_direction = LEFT
                        # 101 - 50j -> 100 - 51j
                        # 102 - 50j -> 100 - 52j
                        x = 100
                        y = -int(position.real) + 50
                        new_pos = x + 1j * y

                    # 2. bottom of the center section
                    elif int(position.imag) == -150:
                        # also facing left
                        new_direction = LEFT
                        # but now we're in the bottom-left section facing left
                        # 51 - 150j -> 50 - 151j
                        # 52 - 150j -> 50 - 152j
                        x = 50
                        y = -int(position.real) - 100
                        new_pos = x + 1j * y
                    # 3. bottom of the bottom-left section
                    else:
                        assert int(position.imag) == -200, position
                        # move to the top right but still facing down
                        x = int(position.real) + 100
                        y = -1
                        new_pos = x + 1j * y

                case 1 + 0j:
                    # right
                    # 4 cases to consider here:
                    # 1. right edge of upper right (moves to right edge of bottom of center section)
                    if int(position.imag) >= -50:
                        # 150 - 1j -> 100 - 150j
                        # 150 - 2j -> 100 - 149j
                        # 150 - 3j -> 100 - 148j
                        new_direction = LEFT
                        x = 100
                        y = -151 - int(position.imag)
                        new_pos = x + 1j * y

                    # 2. right edge of middle bit of center section (moves to lower edge of upper right)
                    elif int(position.imag) >= -100:
                        new_direction = UP
                        y = -50
                        # 100 - 51j -> 101 - 50j
                        # 100 - 52j -> 102 - 50j
                        x = 50 - int(position.imag)
                        new_pos = x + 1j * y

                    # 3. right edge  of lower bit of center section (moves to right edge of upper right section)
                    elif int(position.imag) >= -150:
                        new_direction = LEFT
                        # 100 - 101j -> 150 - 50j
                        # 100 - 102j -> 150 - 49j
                        # -103 -> -48
                        # ...
                        x = int(position.real) + 50
                        y = -50 - (int(position.imag) + 101)
                        new_pos = x + 1j * y

                    # 4. right edge of lower left section (moves to bottom of center section))
                    else:
                        assert position.real == 50
                        new_direction = UP
                        # 50 - 151j -> 51 - 150j
                        # 50 - 152j -> 52 - 150j
                        y = -150
                        x = -int(position.imag) - 100
                        new_pos = x + 1j * y

                case _:
                    # left
                    # also 4 cases
                    # 1. left edge of top center -> left edge of upper left, moving right
                    # 2. left edge of upper center -> top edge of upper left, moving down
                    # 3. left edge of upper left -> left edge of top center, moving right
                    # 4. left edge of bottom left -> top edge of top center, moving down
                    assert direction == LEFT, direction
                    if int(position.real) == 1:
                        # in the left sections (3 and 4 above)
                        if int(position.imag) >= -150:
                            # scenario 3
                            new_direction = RIGHT
                            # 1 - 101j -> 51 - 50j
                            # 1 - 102j -> 51 - 49j
                            # 103 -> 48
                            # 104 -> 47
                            x = 51
                            y = -151 - int(position.imag)
                            new_pos = x + 1j * y
                        else:
                            # scenario 4
                            new_direction = DOWN
                            # 1 - 151j -> 51 - 1j
                            # 1 - 152j -> 52 - 1j
                            y = -1
                            x = -int(position.imag) - 100
                            new_pos = x + 1j * y
                    else:

                        assert int(position.real) == 51
                        if int(position.imag) >= -50:

                            # scenario 1
                            # 50 - 1j -> 1 - 151j
                            # 50 - 2j  -> 1 - 150j
                            # ...
                            # 50 - 50j -> 1 - 101j
                            new_direction = RIGHT
                            x = 1
                            y = -150 + (-1 - int(position.imag))
                            new_pos = x + y * 1j
                        else:
                            # scenario 2
                            new_direction = DOWN
                            # 51 - 51j -> 1 - 101j
                            # 51 - 52j -> 2 - 101j
                            y = -101
                            x = -int(position.imag) - 50
                            new_pos = x + 1j * y

            next_grid_spot = grid[new_pos]
        else:
            new_pos = position + direction
        if next_grid_spot == "#":
            # blocked!
            return position, direction
        direction = new_direction
        grid[new_pos] = DIRECTION_CHARS[direction]
        position = new_pos
    return position, direction


def part_one(puzzle: str) -> int:
    directions, grid = parse_input(puzzle)
    top = max(int(coord.imag) for coord in grid)
    assert top == -1, top
    left = min(int(coord.real) for coord in grid if coord.imag == top)
    position = left + 1j * top
    steps = 0
    direction = RIGHT
    turns_taken = 0
    for char in directions:
        try:
            steps = 10 * steps + int(char)
        except ValueError:
            assert char in "RL"
            position = move(grid, position, direction, steps)

            steps = 0
            direction = turn(direction, char)
            grid[position] = DIRECTION_CHARS[direction]

            turns_taken += 1

    if steps:
        position = move(grid, position, direction, steps)
    return score(position, direction)


def move_and_assert(
    grid: dict[COORDINATE_TYPE, str],
    start_pos: COORDINATE_TYPE,
    start_dir: complex,
    end_pos: COORDINATE_TYPE,
    end_dir: complex,
):
    new_pos, new_direction = move_p2(grid, start_pos, start_dir, 2, 50)
    assert new_direction == end_dir, (new_pos, new_direction)
    assert new_pos == end_pos, (new_pos, new_direction)


def run_tests(grid: dict[COORDINATE_TYPE, str]):
    assert move_p2(grid, 148 - 33j, RIGHT, 36, 50) == (96 - 118j, LEFT), move_p2(
        grid, 148 - 33j, RIGHT, 36, 50
    )
    assert move_p2(grid, 4 - 126j, LEFT, 37, 50) == (1 - 126j, LEFT), move_p2(
        grid, 4 - 126j, LEFT, 37, 50
    )
    assert move_p2(grid, 67 - 8j, LEFT, 36, 50) == (4 - 143j, RIGHT), move_p2(
        grid, 67 - 8j, LEFT, 36, 50
    )
    for args in [
        # 1. leaving upper center, going left
        (51 - 53j, LEFT, 3 - 102j, DOWN),
        # 2. the inverse: leaving upper left, going up
        (4 - 101j, UP, 52 - 54j, RIGHT),
        # 3. leaving lower left, going left
        (1 - 190j, LEFT, 90 - 2j, DOWN),
        # 4. leaving top center, going up
        (89 - 1j, UP, 2 - 189j, RIGHT),
        # 5. leaving upper center,  going left
        (51 - 57j, LEFT, 7 - 102j, DOWN),
        # 6. leaving upper left, going up
        (3 - 101j, UP, 52 - 53j, RIGHT),
        # 7. leaving top right, going up
        (130 - 1j, UP, 30 - 199j, UP),
        # 8. leaving bottom left, going down
        (30 - 200j, DOWN, 130 - 2j, DOWN),
        # 9. leaving top right, going right
        (150 - 3j, RIGHT, 99 - 148j, LEFT),
        # 10. leaving lower center, going right
        (100 - 103j, RIGHT, 150 - 48j, LEFT),
        # 11. leaving upper right going down
        (106 - 50j, DOWN, 99 - 56j, LEFT),
        # 12. Leaving middle center, going right
        (100 - 56j, RIGHT, 106 - 49j, UP),
        # 13. leaving lower left, going right
        (50 - 154j, RIGHT, 54 - 149j, UP),
        # 14 (finally): leaving bottom center, going down
        (52 - 150j, DOWN, 49 - 152j, LEFT),
        # this is where things went awry for me
    ]:
        try:
            move_and_assert(grid, *args)
        except AssertionError:
            print(args)
            raise


def part_two(puzzle: str) -> int:
    directions, grid = parse_input(puzzle)
    top = max(int(coord.imag) for coord in grid)
    assert top == -1, top
    left = min(int(coord.real) for coord in grid if coord.imag == top)
    position = left + 1j * top
    steps = 0
    direction = RIGHT
    turns_taken = 0
    run_tests(grid)
    for char in directions:
        try:
            steps = 10 * steps + int(char)
        except ValueError:
            assert char in "RL"
            try:
                position, direction = move_p2(grid, position, direction, steps, 50)
            except KeyError:
                print(position, direction, steps)
                display_grid(grid)
                raise
            steps = 0
            direction = turn(direction, char)
            grid[position] = DIRECTION_CHARS[direction]

            turns_taken += 1
    if steps:
        position = move(grid, position, direction, steps)
    return score(position, direction)


def display_grid(grid: COORDINATE_TYPE):
    y_values = sorted(int(coord.imag) for coord in grid)
    x_values = sorted(int(coord.real) for coord in grid)
    top = y_values[-1]
    bottom = y_values[0]
    left = x_values[0]
    right = x_values[-1]
    for y in range(top, bottom - 1, -1):
        for x in range(left, right + 1):
            print(grid.get(x + 1j * y, " "), end="")
        print("")


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 6032, part_one_result
    puzzle = Path("day22.txt").read_text()
    print(part_one(puzzle))
    print(part_two(puzzle=puzzle))


if __name__ == "__main__":
    main()

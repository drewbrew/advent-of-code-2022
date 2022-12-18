"""Day 17: don't call it Tetris"""
from pathlib import Path
from typing import Literal, Iterable
from itertools import cycle

ROCK_SHAPES = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##""".split(
    "\n\n"
)

WIDTH = 7

TEST_INPUT = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

START_X = 2
START_Y = 4

# how many rows to preserve in cycle detection
# in my testing, I had a piece fall 40 during part 1
CEILING_HEIGHT = 45  


CoordinateType = tuple[int, int]
InstructionType = Iterable[Literal[1] | Literal[-1]]
RoofType = dict[str, tuple[int, int, int]]


def parse_input(puzzle: str) -> InstructionType:
    return cycle(1 if char == ">" else -1 for char in puzzle)


def place_new_piece(
    chamber: dict[CoordinateType], current_piece: str, instructions: InstructionType
):
    lines = current_piece.splitlines()
    height = len(lines)
    bottom_row = [index for index, char in enumerate(lines[-1]) if char == "#"]
    x = START_X
    initial_y = y = START_Y + max(i[1] for i in chamber)
    while True:

        next_instr = next(instructions)
        for index, row in enumerate(reversed(lines)):
            dy = y + index
            active_x_values = set(ddx for ddx, ddy in chamber if dy == ddy)
            active_x_values |= {-1, WIDTH}
            for x_index, char in enumerate(row):
                if char != "#":
                    continue
                dx = x + x_index + next_instr
                if dx in active_x_values:
                    break
            else:
                continue
            break
        else:
            x += next_instr
        # can it fall?
        for index in bottom_row:
            dx = x + index
            if (dx, y - 1) in chamber:
                # print('found collision', dx, y - 1)
                # display_grid(chamber)
                # nope. comes to rest.
                for index, line in enumerate(lines):
                    dy = y + height - index - 1
                    for x_index, char in enumerate(line):
                        if char == "#":
                            # print('placing', x+ x_index, dy)
                            assert x + x_index < WIDTH, (x, current_piece)
                            assert (x + x_index, dy) not in chamber, (
                                current_piece,
                                (x + x_index, dy),
                            )
                            chamber[x + x_index, dy] = char
                if initial_y - y > CEILING_HEIGHT:
                    raise ValueError(f'Too big of a fall: {initial_y - y}')
                return
            # is it a + shape?
            if current_piece == ROCK_SHAPES[1]:
                # need to check the middle row
                if (x, y) in chamber or (x + 2, y) in chamber:
                    # nope. comes to rest.
                    for index, line in enumerate(lines):
                        dy = y + height - index - 1
                        for x_index, char in enumerate(line):
                            if char == "#":
                                assert (x + x_index, dy) not in chamber
                                chamber[x + x_index, dy] = char
                    if initial_y - y > CEILING_HEIGHT:
                        raise ValueError(f'Too big of a fall: {initial_y - y}')
                    return
        # yes it can fall
        y -= 1
        if y < 0:
            raise ValueError("huh?")


def display_grid(chamber: dict[CoordinateType, str]):
    y_values = sorted(i[1] for i in chamber)
    max_y = y_values[-1]
    min_y = y_values[0]
    for y in range(max_y, min_y - 1, -1):
        print(f"{abs(y) % 10}", end="")
        for x in range(WIDTH):
            print(chamber.get((x, y), " "), end="")
        print("|")


<<<<<<< Updated upstream
def get_roof(
    chamber: dict[CoordinateType, str]
) -> tuple[int, int, int, int, int, int, int]:
    heights = tuple(
        max(y for x1, y in chamber if x1 == x) for x in [0, 1, 2, 3, 4, 5, 6]
    )
    max_y = max(heights)
    return tuple(y - max_y for y in heights)
=======
def get_roof(chamber: dict[CoordinateType, str]) -> str:
    max_y = max(y for _, y in chamber)
    roof = []
    # 100 is acting on faith that there's no way a piece can drop more than 100
    # on a single turn
    for y in range(max_y, max(-1, max_y - CEILING_HEIGHT), -1):
        level = ''.join('#' if (x, y) in chamber else "." for x in range(WIDTH))
        roof.append(level)
    return '\n'.join(roof)
>>>>>>> Stashed changes


def part_one(puzzle: str, turns=2022) -> int:
    instructions = parse_input(puzzle=puzzle)
    chamber = {(x, 0): "-" for x in range(WIDTH)}
    pieces = cycle(ROCK_SHAPES)
    roofs: dict[str, RoofType] = {shape: {} for shape in ROCK_SHAPES}
    repeat_interval = len(ROCK_SHAPES) * len(puzzle)
    height = 0
    repeat_found = False
    turn = 0
    print("repeat interval", repeat_interval)
    while turn < turns:
        next_piece = next(pieces)
        place_new_piece(chamber, next_piece, instructions=instructions)

        if turn <= 5 and turns == 2022:
            display_grid(chamber)
            print(next_piece, "===NEW PIECE===", turn)
        roof = get_roof(chamber=chamber)

        if not repeat_found:
            if old_info := roofs.get(next_piece, {}).get(roof):
                old_turn, old_height, old_index = old_info
                new_index = turn % len(puzzle)
                if new_index == old_index:
                    interval = turn - old_turn
                    delta_y = max(y for _, y in chamber) - old_height
                    print("repeats every", turn - old_turn, delta_y, old_height)
                    while turn + interval < turns:
                        height += delta_y
                        turn += interval
                    print("done ", height, turn)
                    repeat_found = True
            else:
                roofs[next_piece][roof] = (
                    turn,
                    max(y for _, y in chamber),
                    turn % len(puzzle),
                )
        turn += 1
        if turns > 10000 and turn and not turn % 1000:
            print(turn, end="\r")

    print(turn, height)
    return max(y for _, y in chamber) + height


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 3068, part_one_result
    puzzle = Path("day17.txt").read_text().strip()
    print(part_one(puzzle))
    part_two_result = part_one(TEST_INPUT, 1000000000000)
    assert part_two_result == 1514285714288, part_two_result

    print(part_one(puzzle, 1000000000000))


if __name__ == "__main__":
    main()

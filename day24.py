import heapq
from pathlib import Path


TEST_INPUT = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#""".splitlines()

COORDINATE_TYPE = tuple[int, int]
GRID_TYPE = dict[COORDINATE_TYPE, str]

DIRECTIONS = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, -1),
    "v": (0, 1),
}


def parse_input(
    puzzle: list[str],
) -> tuple[GRID_TYPE, COORDINATE_TYPE, COORDINATE_TYPE]:
    start = None
    end = None
    grid: GRID_TYPE = {}
    for y, row in enumerate(puzzle):
        for x, char in enumerate(row):
            if y == 0 and not start:
                if char == ".":
                    start = (x, y)

            if y == len(puzzle) - 1 and not end:
                if char == ".":
                    end = (x, y)
            grid[x, y] = char

    return grid, start, end


def make_move(
    grid: GRID_TYPE, person: COORDINATE_TYPE, width: int, height: int
) -> list[tuple[GRID_TYPE, COORDINATE_TYPE]]:
    assert grid[person] == ".", (grid, person)
    results = []
    new_grid: GRID_TYPE = {}
    for (x, y), chars in grid.items():
        if chars == ".":
            # nothing leaves this place
            continue
        elif chars == "#":
            new_grid[x, y] = chars
            continue
        for char in chars:
            dx, dy = DIRECTIONS[char]
            if grid[x + dx, y + dy] == "#":
                # warp!
                if dx == -1:
                    # left wall
                    save_to_grid(new_grid, width - 2, y, char)
                elif dx == 1:
                    # right wall
                    save_to_grid(new_grid, 1, y, char)
                elif dy == -1:
                    # top wall
                    save_to_grid(new_grid, x, height - 2, char)
                else:
                    assert dy == 1, (dx, dy)
                    save_to_grid(new_grid, x, 1, char)
            else:
                save_to_grid(new_grid, x + dx, y + dy, char)
    # print(new_grid)
    # now let's put our dots in
    for x in range(width):
        for y in range(height):
            if (x, y) not in new_grid:
                new_grid[x, y] = "."
    if new_grid[person] == ".":
        # not moving is valid
        # print(f'not moving from {person} is valid')
        results.append((new_grid.copy(), person))
    x, y = person
    for dx, dy in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        if (dx, dy) not in grid:
            continue
        if new_grid[dx, dy] != ".":
            continue
        # print(f'moving from {person} to {(dx, dy)} is valid')
        # this move is valid
        results.append((new_grid.copy(), (dx, dy)))
    return results


def save_to_grid(grid: GRID_TYPE, x: int, y: int, char: str):
    assert len(char) == 1
    try:
        grid[x, y] += char
    except KeyError:
        grid[x, y] = char


def part_one(puzzle: list[str]) -> int:
    best_turns = 750
    grid, start, end = parse_input(puzzle)
    width = len(puzzle[0])
    height = len(puzzle)
    queue = [(0, start, grid)]
    heapq.heapify(queue)
    iterations = 0
    # states_seen = set(
    #     (
    #         start,
    #         frozenset(grid.items()),
    #     )
    # )
    # print('trying to get to ', end)
    states_seen: set[tuple[int, COORDINATE_TYPE]] = set()
    while queue:
        try:
            turns, position, new_grid = heapq.heappop(queue)
        except IndexError:
            return best_turns
        if position == end:
            # print(f'\n\nmade it to the end in {turns} moves')
            best_turns = min(best_turns, turns)
            continue
        if turns >= best_turns:
            continue
        set_key = (turns, position)
        if set_key in states_seen:
            continue
        states_seen.add(set_key)
        for newer_grid, new_position in make_move(
            new_grid, position, width=width, height=height
        ):
            # print(f"moved from {position} to {new_position}")
            # display_grid(newer_grid, position)
            heapq.heappush(queue, (turns + 1, new_position, newer_grid))
        iterations += 1
        print(f"{iterations}\t{len(queue)}\t{turns}\t{best_turns}", end="\r")
    print("")
    return best_turns


def part_two(puzzle: list[str], part_one_score: int) -> int:
    best_turns = 750
    grid, end, start = parse_input(puzzle)
    width = len(puzzle[0])
    height = len(puzzle)
    queue = [(part_one_score, start, grid)]
    heapq.heapify(queue)
    iterations = 0
    # states_seen = set(
    #     (
    #         start,
    #         frozenset(grid.items()),
    #     )
    # )
    # print('trying to get to ', end)
    states_seen: set[tuple[int, COORDINATE_TYPE]] = set()
    while queue:
        try:
            turns, position, new_grid = heapq.heappop(queue)
        except IndexError:
            return best_turns
        if position == end:
            # print(f'\n\nmade it to the end in {turns} moves')
            best_turns = min(best_turns, turns)
            continue
        if turns >= best_turns:
            continue
        set_key = (turns, position)
        if set_key in states_seen:
            continue
        states_seen.add(set_key)
        for newer_grid, new_position in make_move(
            new_grid, position, width=width, height=height
        ):
            # print(f"moved from {position} to {new_position}")
            # display_grid(newer_grid, position)
            heapq.heappush(queue, (turns + 1, new_position, newer_grid))
        iterations += 1
        print(f"{iterations}\t{len(queue)}\t{turns}\t{best_turns}", end="\r")
    print("")
    return best_turns


def display_grid(grid: GRID_TYPE, person: COORDINATE_TYPE):
    max_x = max(x for x, _ in grid)
    max_y = max(y for _, y in grid)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) == person:
                print("P", end="")

            elif (length := len(grid[x, y])) > 1:
                print(length, end="")
            else:
                print(grid[x, y], end="")
        print("")


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 18, part_one_result
    print("main puzzle: go")
    puzzle = Path("day24.txt").read_text().splitlines()
    part_one_result = part_one(puzzle=puzzle)
    print(part_one_result)
    print("here goes part two")
    print(part_two(puzzle, part_one_result))


if __name__ == "__main__":
    main()

"""Day 12: mountain climbing"""

from pathlib import Path
from collections import defaultdict

import networkx
from networkx.exception import NetworkXNoPath


TEST_INPUT = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""".splitlines()

COORDINATE_TYPE = tuple[int, int]


class Colors:
    """ANSI escape sequences to format text with colors"""

    reset = "\033[0m"
    bold = "\033[01m"
    disable = "\033[02m"
    underline = "\033[04m"
    reverse = "\033[07m"
    strikethrough = "\033[09m"
    invisible = "\033[08m"

    class Foreground:
        black = "\033[30m"
        red = "\033[31m"
        green = "\033[32m"
        orange = "\033[33m"
        blue = "\033[34m"
        purple = "\033[35m"
        cyan = "\033[36m"
        lightgrey = "\033[37m"
        darkgrey = "\033[90m"
        lightred = "\033[91m"
        lightgreen = "\033[92m"
        yellow = "\033[93m"
        lightblue = "\033[94m"
        pink = "\033[95m"
        lightcyan = "\033[96m"

    class Background:
        black = "\033[40m"
        red = "\033[41m"
        green = "\033[42m"
        orange = "\033[43m"
        blue = "\033[44m"
        purple = "\033[45m"
        cyan = "\033[46m"
        lightgrey = "\033[47m"


def parse_input(
    puzzle: list[str],
) -> tuple[
    networkx.DiGraph, COORDINATE_TYPE, COORDINATE_TYPE, dict[COORDINATE_TYPE, int]
]:
    graph = networkx.DiGraph()

    coordinates: dict[COORDINATE_TYPE, int] = {}

    for y, row in enumerate(puzzle):
        for x, char in enumerate(row.strip()):
            if char == "S":
                start = (x, y)
                char = "a"
            elif char == "E":
                end = (x, y)
                char = "z"
            elev = ord(char) - ord("a")
            coordinates[x, y] = elev
            graph.add_node((x, y))

    for (x, y), elev in coordinates.items():
        for (dx, dy) in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if coordinates.get((dx, dy), 100000000) <= elev + 1:
                # print(f'adding step from {x, y} to {dx, dy}')
                graph.add_edge((x, y), (dx, dy))
    return graph, start, end, coordinates


def part_one(puzzle: list[str]) -> int:
    graph, start, end, _ = parse_input(puzzle=puzzle)
    return networkx.shortest_path_length(graph, start, end)


def part_two(puzzle: list[str]) -> int:
    graph, _, end, coordinates = parse_input(puzzle=puzzle)
    minimum = 100000
    for start, elev in coordinates.items():
        if elev == 0:
            try:
                new_min = networkx.shortest_path_length(graph, start, end)
            except NetworkXNoPath:
                continue
            minimum = min(new_min, minimum)
    return minimum


def visualize_part_two(puzzle: list[str]) -> None:
    graph, _, end, coordinates = parse_input(puzzle=puzzle)
    points_seen: defaultdict[COORDINATE_TYPE, int] = defaultdict(int)
    for start, elev in coordinates.items():
        if elev == 0:
            try:
                path_to_end: list[COORDINATE_TYPE] = networkx.shortest_path(
                    graph, start, end
                )
            except NetworkXNoPath:
                continue
            for point in path_to_end:
                points_seen[point] += 1
    colors = {
        242: Colors.Foreground.lightgrey + Colors.bold,
        220: Colors.Foreground.lightgrey,
        211: Colors.Foreground.lightgreen,
        210: Colors.Foreground.lightblue,
        209: Colors.Foreground.lightred,
        208: Colors.Foreground.lightcyan,
        188: Colors.Foreground.green,
        144: Colors.Foreground.green,
        136: Colors.Foreground.green,
        129: Colors.Foreground.green,
        0: Colors.Foreground.black,
    }
    for i in range(50, 66):
        colors[i] = Colors.Foreground.blue
    for i in range(20, 50):
        colors[i] = Colors.Foreground.red
    for i in range(10, 20):
        colors[i] = Colors.Foreground.cyan
    for i in range(1, 10):
        colors[i] = Colors.Foreground.darkgrey
    max_x = max(i[0] for i in coordinates)
    max_y = max(i[1] for i in coordinates)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(
                f"{colors[points_seen[x, y]]}{chr(ord('a') + coordinates[x, y]) if (x, y) != end else 'E'}"
                f"{Colors.reset}",
                end="",
            )
        print("")


def main():
    part_one_result = part_one(puzzle=TEST_INPUT)
    assert part_one_result == 31, part_one_result
    puzzle = Path("day12.txt").read_text().splitlines()
    print(part_one(puzzle=puzzle))
    part_two_result = part_two(puzzle=TEST_INPUT)
    assert part_two_result == 29, part_two_result
    print(part_two(puzzle=puzzle))
    visualize_part_two(puzzle)


if __name__ == "__main__":
    main()

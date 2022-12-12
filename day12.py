"""Day 12: mountain climbing"""

from pathlib import Path

import networkx
from networkx.exception import NetworkXNoPath


TEST_INPUT = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""".splitlines()

COORDINATE_TYPE = tuple[int, int]


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


def main():
    part_one_result = part_one(puzzle=TEST_INPUT)
    assert part_one_result == 31, part_one_result
    puzzle = Path("day12.txt").read_text().splitlines()
    print(part_one(puzzle=puzzle))
    part_two_result = part_two(puzzle=TEST_INPUT)
    assert part_two_result == 29, part_two_result
    print(part_two(puzzle=puzzle))


if __name__ == "__main__":
    main()

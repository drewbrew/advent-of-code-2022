"""Day 18: 3D cubes"""

from pathlib import Path

import networkx
from networkx.exception import NetworkXNoPath

COORDINATE_TYPE = tuple[int, int, int]

SMALL_INPUT = """1,1,1
2,1,1""".splitlines()

TEST_INPUT = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5""".splitlines()


def parse_input(puzzle: list[str]) -> list[COORDINATE_TYPE]:
    grid = []
    for line in puzzle:
        grid.append(tuple(int(i) for i in line.split(",")))
    assert all(len(i) == 3 for i in grid), grid
    return grid


def unconnected_sides(nodes: list[COORDINATE_TYPE]) -> int:
    nodes = set(nodes)
    score = 0
    for x, y, z in sorted(nodes):
        base_score = 6
        for neighbor in (
            (x + 1, y, z),
            (x - 1, y, z),
            (x, y + 1, z),
            (x, y - 1, z),
            (x, y, z + 1),
            (x, y, z - 1),
        ):
            if neighbor in nodes:
                base_score -= 1
        score += base_score

    return score


def part_one(puzzle: list[str]) -> int:
    grid = parse_input(puzzle)

    return unconnected_sides(grid)


def part_two(puzzle: list[str]) -> int:
    grid = set(parse_input(puzzle))
    # abuse networkx here:
    # find all nodes which aren't in the graph and aren't reachable
    # from the outside world
    graph = networkx.Graph()
    max_x = max(i[0] for i in grid) + 1
    max_y = max(i[1] for i in grid) + 1
    max_z = max(i[2] for i in grid) + 1
    part_one_score = part_one(puzzle=puzzle)
    for x in range(-1, max_x):
        for y in range(-1, max_y):
            for z in range(-1, max_z):
                if (x, y, z) not in grid:
                    graph.add_node((x, y, z))
                    for neighbor in [
                        (x + 1, y, z),
                        (x - 1, y, z),
                        (x, y + 1, z),
                        (x, y - 1, z),
                        (x, y, z + 1),
                        (x, y, z - 1),
                    ]:
                        if neighbor not in grid:
                            graph.add_edge((x, y, z), neighbor)
    internal_disconnected_bits: set[COORDINATE_TYPE] = set()
    for x, y, z in graph.nodes:
        if (x, y, z) == (-1, -1, -1):
            continue
        try:
            networkx.shortest_path_length(graph, (x, y, z), (-1, -1, -1))
        except NetworkXNoPath:
            internal_disconnected_bits.add((x, y, z))
    # then pass that result into the same surface area function from part 1
    return part_one_score - unconnected_sides(internal_disconnected_bits)


def main():
    part_one_result = part_one(SMALL_INPUT)
    assert part_one_result == 10, part_one_result
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 64, part_one_result
    puzzle = Path("day18.txt").read_text().splitlines()
    print(part_one(puzzle))
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 58, part_two_result
    print(part_two(puzzle=puzzle))


if __name__ == "__main__":
    main()

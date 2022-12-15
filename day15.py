from pathlib import Path
from collections.abc import Generator

TEST_INPUT = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3""".splitlines()


COORDINATE_TYPE = tuple[int, int]
TEST_TARGET_ROW = 10
REAL_TARGET_ROW = 2_000_000


def parse_input(
    puzzle: list[str],
) -> tuple[dict[COORDINATE_TYPE, int], set[COORDINATE_TYPE]]:
    grid = {}
    beacons = set()
    for line in puzzle:
        words = line.split()
        s_x = int(words[2][2:-1])
        s_y = int(words[3][2:-1])
        b_x = int(words[-2][2:-1])
        b_y = int(words[-1][2:])
        beacons.add((b_x, b_y))
        grid[s_x, s_y] = manhattan((s_x, s_y), (b_x, b_y))

    return grid, beacons


def manhattan(point1: tuple[COORDINATE_TYPE], point2: tuple[COORDINATE_TYPE]) -> int:
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)


def part_one(puzzle: list[str], target_y: int) -> int:
    grid, beacons = parse_input(puzzle=puzzle)
    x_values = sorted(x for x, _ in grid)
    biggest_range = max(grid.values())
    score = 0
    for x in range(x_values[0] - biggest_range, x_values[-1] + biggest_range + 1):
        point = (x, target_y)
        if point in beacons:
            continue
        if point in grid:
            # print(point, 'in grid')
            score += 1
            continue
        for sensor, dist in grid.items():
            if manhattan(sensor, point) <= dist:
                # print(point, sensor, dist)
                score += 1
                break
    return score


def tuning_freq(point: COORDINATE_TYPE):
    x, y = point
    return y + 4000000 * x


def first_points_not_detected(
    sensor: COORDINATE_TYPE,
    distance: int,
    max_coordinate: int,
) -> Generator[COORDINATE_TYPE, None, None]:
    x, y = sensor
    dx = x + distance + 1
    dy = y
    while dx > x:
        # move up and to the left
        if dx >= 0 and dy >= 0 and dx <= max_coordinate and dy <= max_coordinate:
            yield dx, dy
        dx -= 1
        dy += 1
    assert dy == y + distance + 1
    while dy > y:
        # move down and to the left
        if dx >= 0 and dy >= 0 and dx <= max_coordinate and dy <= max_coordinate:
            yield dx, dy
        dx -= 1
        dy -= 1
    assert dx == x - distance - 1
    while dx < x:
        if dx >= 0 and dy >= 0 and dx <= max_coordinate and dy <= max_coordinate:
            yield dx, dy
        # move down and to the right
        dx += 1
        dy -= 1
    assert dy == y - distance - 1
    while dy < y:
        if dx >= 0 and dy >= 0 and dx <= max_coordinate and dy <= max_coordinate:
            yield dx, dy
        dx += 1
        dy += 1
    # and make sure we're back where we started
    assert dx == x + distance + 1


def part_two(puzzle: list[str], max_x: int, max_y: int) -> int:
    grid, beacons = parse_input(puzzle=puzzle)
    assert max_x == max_y
    for sensor, distance in grid.items():
        for neighbor in first_points_not_detected(
            sensor,
            distance=distance,
            max_coordinate=max_x,
        ):
            if neighbor in beacons:
                continue
            for other_sensor, other_dist in grid.items():
                if other_sensor == sensor:
                    continue
                if manhattan(other_sensor, neighbor) <= other_dist:
                    break
            else:
                freq = tuning_freq(neighbor)
                return freq
    raise ValueError("Destination not found?!?")


def main():
    part_one_result = part_one(TEST_INPUT, TEST_TARGET_ROW)
    assert part_one_result == 26, part_one_result
    puzzle = Path("day15.txt").read_text().splitlines()
    print(part_one(puzzle, REAL_TARGET_ROW))
    part_two_result = part_two(TEST_INPUT, 20, 20)
    assert part_two_result == 56000011, part_two_result
    print(part_two(puzzle, 4000000, 4000000))


if __name__ == "__main__":
    main()

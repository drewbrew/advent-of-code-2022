from dataclasses import dataclass
from pathlib import Path
from typing import Self
from collections import defaultdict
import heapq


TEST_INPUT = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""".splitlines()

BLUEPRINT_WORD = 1
ORE_ROBOT_COST_WORD = 6
CLAY_ROBOT_ORE_COST_WORD = ORE_ROBOT_COST_WORD + 6
OBSIDIAN_ROBOT_ORE_COST_WORD = CLAY_ROBOT_ORE_COST_WORD + 6
OBSIDIAN_ROBOT_CLAY_COST_WORD = OBSIDIAN_ROBOT_ORE_COST_WORD + 3
GEODE_ROBOT_ORE_COST_WORD = OBSIDIAN_ROBOT_CLAY_COST_WORD + 6
GEODE_ROBOT_OBSIDIAN_COST_WORD = GEODE_ROBOT_ORE_COST_WORD + 3


@dataclass
class Blueprint:
    number: int
    ore_robot_ore_cost: int
    clay_robot_ore_cost: int
    obsidian_robot_ore_cost: int
    obsidian_robot_clay_cost: int
    geode_robot_ore_cost: int
    geode_robot_obsidian_cost: int

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(number={self.number},"
            f" ore_robot_ore_cost={self.ore_robot_ore_cost},"
            f" clay_robot_ore_cost={self.clay_robot_ore_cost},"
            f" obsidian_robot_ore_cost={self.obsidian_robot_ore_cost},"
            f" obsidian_robot_clay_cost={self.obsidian_robot_clay_cost},"
            f" geode_robot_ore_cost={self.geode_robot_ore_cost},"
            f" geode_robot_obsidian_cost={self.geode_robot_obsidian_cost})"
        )

    @classmethod
    def from_puzzle_line(cls, line: str) -> Self:
        words = line.split()
        return cls(
            number=int(words[BLUEPRINT_WORD][:-1]),
            ore_robot_ore_cost=int(words[ORE_ROBOT_COST_WORD]),
            clay_robot_ore_cost=int(words[CLAY_ROBOT_ORE_COST_WORD]),
            obsidian_robot_ore_cost=int(words[OBSIDIAN_ROBOT_ORE_COST_WORD]),
            obsidian_robot_clay_cost=int(words[OBSIDIAN_ROBOT_CLAY_COST_WORD]),
            geode_robot_ore_cost=int(words[GEODE_ROBOT_ORE_COST_WORD]),
            geode_robot_obsidian_cost=int(words[GEODE_ROBOT_OBSIDIAN_COST_WORD]),
        )


def best_score_for_blueprint(blueprint: Blueprint, time: int = 24) -> int:
    """Run through the game for the blueprint, finding the most geodes possible"""
    max_materials_needed = [
        # never need more than any of the first 3:
        # ore
        max(
            blueprint.clay_robot_ore_cost,
            blueprint.geode_robot_ore_cost,
            blueprint.ore_robot_ore_cost,
            blueprint.obsidian_robot_clay_cost,
        ),
        # clay
        blueprint.obsidian_robot_clay_cost,
        # obsidian
        blueprint.geode_robot_obsidian_cost,
        1_000_000_000,  # want to maximize geodes
    ]
    queue: list[
        tuple[int, int, tuple[int, int, int, int], tuple[int, int, int, int]]
    ] = [
        (
            0,  # geode bots
            time,  # minutes to go
            (0, 0, 0, 0),  # materials on hand
            (1, 0, 0, 0),  # bots available
        )
    ]
    heapq.heapify(queue)
    result = 0
    counter = 0
    states = defaultdict(lambda: -100)
    while queue:
        _, time_left, materials, robots = heapq.heappop(queue)
        counter += 1
        if not counter % 100000:
            print(counter, time_left, materials, robots, len(queue), end="\r")
        # how many geodes can we make given the current state?
        result = max(result, materials[-1] + robots[-1] * time_left)
        # how many can we make if we make a geode bot for every remaining turn
        # regardless of materials?
        max_theoretical_limit = (
            ((time_left + robots[3]) * (time_left + robots[3] + 1)) // 2
            - (robots[3] * (robots[3] + 1)) // 2
            + materials[3]
        )
        if max_theoretical_limit <= result:
            # we've already done better
            continue

        # use the geodes produced as the cache value
        cache_key = time_left, materials[:-1], robots
        if states[cache_key] >= materials[-1]:
            # have we already found a better way?
            continue
        else:
            states[cache_key] = materials[-1]

        if not time_left:
            continue

        # do we want to wait for new materials?
        if any(
            material < max_material and robot
            for (material, max_material, robot) in zip(
                materials, max_materials_needed, robots
            )
        ):
            new_materials = tuple(
                material + robot for material, robot in zip(materials, robots)
            )
            new_robots = robots[:]
            heapq.heappush(
                queue,
                (
                    -new_robots[3],
                    time_left - 1,
                    new_materials,
                    new_robots,
                ),
            )

        # now build
        build_costs = {
            # ore bot
            0: (blueprint.ore_robot_ore_cost, 0, 0, 0),
            # clay bot
            1: (blueprint.clay_robot_ore_cost, 0, 0, 0),
            # obsidian bot
            2: (
                blueprint.obsidian_robot_ore_cost,
                blueprint.obsidian_robot_clay_cost,
                0,
                0,
            ),
            # geode bot
            3: (
                blueprint.geode_robot_ore_cost,
                0,
                blueprint.geode_robot_obsidian_cost,
                0,
            ),
        }
        for bot_index, costs in build_costs.items():
            # check whether we want and should build the robot
            if max_materials_needed[bot_index] > robots[bot_index] and all(
                material >= price for material, price in zip(materials, costs)
            ):
                # update the materials we will have in the next step
                new_materials = tuple(
                    material + robot - price
                    for material, robot, price in zip(materials, robots, costs)
                )

                # update the robots we will have
                new_robots = tuple(
                    robot + 1 if rx == bot_index else robot
                    for rx, robot in enumerate(robots)
                )

                # append to the queue
                heapq.heappush(
                    queue,
                    (
                        -new_robots[3],
                        time_left - 1,
                        new_materials,
                        new_robots,
                    ),
                )
    print("")
    return result


def part_one(puzzle: list[str]) -> int:
    blueprints = [Blueprint.from_puzzle_line(line) for line in puzzle]
    total = 0
    for blueprint in blueprints:
        blueprint_score = best_score_for_blueprint(blueprint=blueprint)
        print(
            f"Blueprint {blueprint.number} scored {blueprint.number * blueprint_score} from "
            f"{blueprint_score} geodes"
        )
        total += blueprint_score * blueprint.number
    return total


def part_two(puzzle: list[str]) -> int:
    blueprints = [Blueprint.from_puzzle_line(line) for line in puzzle][:3]
    total = 1
    for blueprint in blueprints:
        blueprint_score = best_score_for_blueprint(blueprint=blueprint, time=32)
        print(
            f"Blueprint {blueprint.number} scored {blueprint_score} from "
            f"{blueprint_score} geodes"
        )
        total *= blueprint_score
    return total


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 33, part_one_result
    puzzle = Path("day19.txt").read_text().splitlines()
    print(part_one(puzzle=puzzle))
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 62 * 56, part_two_result
    print(part_two(puzzle=puzzle))


if __name__ == "__main__":
    main()

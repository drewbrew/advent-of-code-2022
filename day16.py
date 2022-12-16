"""Day 16: I don't know where I'm a gonna go when the volcano blow"""

from dataclasses import dataclass
from pathlib import Path
from copy import deepcopy
from collections import deque
from typing import Self

import networkx

TURNS = 30

TEST_INPUT = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II""".splitlines()

START = "AA"
START_FLOW = 0


Valve = tuple[bool, int, list[str]]


def parse_input(puzzle: list[str]) -> tuple[dict[str, Valve], networkx.Graph]:
    graph = networkx.Graph()
    valves: dict[str, Valve] = {}
    for line in puzzle:
        words = line.split()
        name = words[1]
        flow_rate = int(words[4].split("=")[1][:-1])
        valve_neighbors = [word.split(",")[0] for word in words[9:]]
        for neighbor in valve_neighbors:
            graph.add_edge(name, neighbor)
        # HACK: if there's no flow, go ahead and mark it as open
        valves[name] = (flow_rate == 0, flow_rate, valve_neighbors)
    return valves, graph


def max_theoretical_flow(valves: dict[str, Valve], turns_remaining: int) -> int:
    """What's the best possible remaining flow we could get by turning things on
    regardless of distance"""
    value = 0
    for index, (state, rate, _) in enumerate(
        sorted([v for v in valves.values() if not v[0]], key=lambda k: -k[1]), start=1
    ):
        assert not state
        value += max((turns_remaining - index) * rate, 0)
    return value


def part_one(puzzle: list[str]) -> int:
    valves, graph = parse_input(puzzle)
    distances: dict[str, dict[str, int]] = {}
    valves_to_open = [
        name
        for name, (valve_open, rate, _) in valves.items()
        if rate and not valve_open
    ]
    for valve in valves:
        distances[valve] = {}
        for target in valves_to_open:
            if target == valve:
                continue
            distances[valve][target] = networkx.shortest_path_length(
                graph, valve, target
            )
    queue: deque[tuple[int, int, str, dict[str, Valve]]] = deque(
        [(0, TURNS, "AA", deepcopy(valves))]
    )
    # queue: total flow, turns remaining, current position, valves
    best_flow = 0
    while True:
        try:
            (
                total_flow,
                turns_remaining,
                current_position,
                current_valves,
            ) = queue.pop()
        except IndexError:
            return best_flow
        open_valves = []
        total_flow_this_turn = 0
        for name, (flow_open, flow_rate, _) in current_valves.items():
            if flow_open and flow_rate:
                open_valves.append(name)
                total_flow_this_turn += flow_rate

        if turns_remaining <= 0:
            best_flow = max(best_flow, total_flow)
            # end state
            continue
        if all(valve[0] for valve in current_valves.values()):
            # do nothing
            if total_flow > best_flow:
                best_flow = max(best_flow, total_flow)
            continue
        if (
            total_flow
            + (
                limit := max_theoretical_flow(
                    current_valves, turns_remaining=turns_remaining
                )
            )
            < best_flow
        ):
            # bail out if there's no way we could make it work
            continue
        # try turning on the valve
        current_valve = current_valves[current_position]
        valve_open, flow_rate, neighbors = current_valve
        if not valve_open:
            new_valves: dict[str, Valve] = {**current_valves}
            new_valves[current_position] = (True, flow_rate, neighbors)
            current_flow = flow_rate * (turns_remaining - 1)
            queue.append(
                (
                    total_flow + current_flow,
                    turns_remaining - 1,
                    current_position,
                    new_valves,
                )
            )
            continue
        # valve is already open (or opening wouldn't do any good)

        # Now let's hop to each closed valve and start another round
        for target, distance in distances[current_position].items():
            if not current_valves[target][0]:
                # move to that valve
                queue.append(
                    (total_flow, turns_remaining - distance, target, current_valves)
                )


def open_or_move(
    valves: dict[str, Valve],
    turns_remaining: int,
    current_position: str,
    distances: dict[str, dict[str, int]],
) -> list[tuple[dict[str, Valve], str, int, int]]:
    """Take an action, either turning on a valve or moving

    Returns a list of:
    - updated valve dict
    - new position of the actor
    - flow generated by the action
    - new turns_remaining
    """
    flow_open, flow_rate, neighbors = valves[current_position]
    if not flow_open:
        new_valves: dict[str, Valve] = {**valves}
        new_valves[current_position] = (True, flow_rate, neighbors)
        current_flow = flow_rate * (turns_remaining - 1)
        return [(new_valves, current_position, current_flow, turns_remaining - 1)]
    result = []
    for target, distance in distances[current_position].items():
        if not valves[target][0]:
            # move to that valve
            result.append((valves, target, 0, turns_remaining - distance))
    return result


@dataclass
class State:
    valves: dict[str, Valve]
    distances: dict[str, dict[str, int]]
    human_position: str
    elephant_position: str
    turns_remaining: int
    human_next_turn: int
    elephant_next_turn: int
    total_flow: int

    def take_action(self) -> list[Self]:
        new_states = []
        if self.turns_remaining == self.human_next_turn:
            # take the human action
            for (
                new_valves,
                new_human_position,
                new_human_flow,
                new_human_turns_remaining,
            ) in open_or_move(
                self.valves,
                turns_remaining=self.turns_remaining,
                current_position=self.human_position,
                distances=self.distances,
            ):
                if self.turns_remaining == self.elephant_next_turn:
                    for (
                        newer_valves,
                        new_elephant_position,
                        new_elephant_flow,
                        new_elephant_turns_remaining,
                    ) in open_or_move(
                        valves=new_valves,
                        turns_remaining=self.elephant_next_turn,
                        current_position=self.elephant_position,
                        distances=self.distances,
                    ):
                        new_states.append(
                            State(
                                valves=newer_valves,
                                distances=self.distances,
                                human_next_turn=new_human_turns_remaining,
                                elephant_next_turn=new_elephant_turns_remaining,
                                human_position=new_human_position,
                                turns_remaining=self.turns_remaining - 1,
                                elephant_position=new_elephant_position,
                                total_flow=self.total_flow
                                + new_human_flow
                                + new_elephant_flow,
                            )
                        )
                else:
                    # elephant can't move
                    new_states.append(
                        State(
                            valves=new_valves,
                            distances=self.distances,
                            human_next_turn=new_human_turns_remaining,
                            elephant_next_turn=self.elephant_next_turn,
                            human_position=new_human_position,
                            elephant_position=self.elephant_position,
                            total_flow=self.total_flow + new_human_flow,
                            turns_remaining=self.turns_remaining - 1,
                        )
                    )
        elif self.elephant_next_turn == self.turns_remaining:
            # human can't move, but elephant can
            for (
                newer_valves,
                new_elephant_position,
                new_elephant_flow,
                new_elephant_turns_remaining,
            ) in open_or_move(
                valves=self.valves,
                turns_remaining=self.elephant_next_turn,
                current_position=self.elephant_position,
                distances=self.distances,
            ):
                new_states.append(
                    State(
                        valves=newer_valves,
                        distances=self.distances,
                        human_next_turn=self.human_next_turn,
                        elephant_next_turn=new_elephant_turns_remaining,
                        human_position=self.human_position,
                        turns_remaining=self.turns_remaining - 1,
                        elephant_position=new_elephant_position,
                        total_flow=self.total_flow + new_elephant_flow,
                    )
                )
        else:
            # neither can move
            assert self.human_next_turn < self.turns_remaining
            assert self.elephant_next_turn < self.turns_remaining
            # count down until the next time either can move
            new_states.append(
                State(
                    valves=self.valves,
                    distances=self.distances,
                    human_next_turn=self.human_next_turn,
                    elephant_next_turn=self.elephant_next_turn,
                    human_position=self.human_position,
                    elephant_position=self.elephant_position,
                    turns_remaining=max(self.human_next_turn, self.elephant_next_turn),
                    total_flow=self.total_flow,
                )
            )
        return new_states


def part_two(puzzle: list[str]) -> int:
    valves, graph = parse_input(puzzle)
    distances: dict[str, dict[str, int]] = {}
    valves_to_open = [
        name
        for name, (valve_open, rate, _) in valves.items()
        if rate and not valve_open
    ]
    for valve in valves:
        distances[valve] = {}
        for target in valves_to_open:
            if target == valve:
                continue
            distances[valve][target] = networkx.shortest_path_length(
                graph, valve, target
            )
    queue: deque[State] = deque(
        [
            State(
                human_next_turn=26,
                turns_remaining=26,
                valves=valves,
                distances=distances,
                human_position="AA",
                elephant_position="AA",
                total_flow=0,
                elephant_next_turn=26,
            )
        ]
    )
    best_flow = 0
    turns = 0
    while True:
        try:
            # eliminate the late-stage games first in the hopes
            # of getting cutoffs faster
            state = queue.pop()
        except IndexError:
            if puzzle != TEST_INPUT:
                print("\n")
            return best_flow

        if state.turns_remaining <= 0:
            best_flow = max(best_flow, state.total_flow)
            # end state
            continue
        if all(valve[0] for valve in state.valves.values()):
            # do nothing
            if state.total_flow > best_flow:
                best_flow = max(best_flow, state.total_flow)
            continue
        if (
            state.total_flow
            + (
                limit := max_theoretical_flow(
                    state.valves, turns_remaining=state.turns_remaining
                )
            )
            < best_flow
        ):
            # bail out if there's no way we could make it work
            continue
        queue.extend(state.take_action())
        turns += 1

        if puzzle != TEST_INPUT and not turns % 10000:
            print(
                f"{turns=}\t{len(queue)=}\t{best_flow=}",
                end="\r",
            )


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 1651, part_one_result
    puzzle = Path("day16.txt").read_text().splitlines()
    print(part_one(puzzle))
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 1707, part_two_result
    print(part_two(puzzle))


if __name__ == "__main__":
    main()

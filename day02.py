"""Day 2: paper, rock, scissors"""
from pathlib import Path


SCORES = {
    "A": 1,  # ROCK
    "X": 1,
    "B": 2,  # PAPER
    "Y": 2,
    "C": 3,  # SCISSORS
    "Z": 3,
}

LOSS = 0
WIN = 6
DRAW = 3

TEST_INPUT = """A Y
B X
C Z""".splitlines()


def parse_input(puzzle: list[str]) -> list[tuple[str, str]]:
    return [line.strip().split() for line in puzzle]


def play_round(part_one: tuple[str, str]) -> int:
    opponent, me = part_one

    if (opponent, me) in [("A", "X"), ("B", "Y"), ("C", "Z")]:
        # draw
        return SCORES[me] + DRAW
    if (
        (opponent == "A" and me == "Y")  # paper beats rock
        or (opponent == "B" and me == "Z")  # scissors beats paper
        or (opponent == "C" and me == "X")  # rock beats scissors
    ):
        return SCORES[me] + WIN
    return SCORES[me] + LOSS


def play_round_part_2(turn: tuple[str, str]) -> int:
    opponent, result = turn
    if result == "X":  # lose
        losses = {
            "A": "Z",
            "B": "X",
            "C": "Y",
        }
        me = losses[opponent]
    elif result == "Y":  # draw
        draws = {
            "A": "X",
            "B": "Y",
            "C": "Z",
        }
        me = draws[opponent]
    else:
        wins = {
            "A": "Y",
            "B": "Z",
            "C": "X",
        }
        me = wins[opponent]
    return play_round((opponent, me))


def play_game(puzzle: list[str]) -> int:
    game = parse_input(puzzle)
    rounds = [play_round(turn) for turn in game]
    return sum(rounds)


def play_part_two(puzzle: list[str]) -> int:
    game = parse_input(puzzle)
    rounds = [play_round_part_2(turn) for turn in game]
    return sum(rounds)


def main():
    real_puzzle = Path("day02.txt").read_text().splitlines()
    assert play_game(TEST_INPUT) == 15, play_game(TEST_INPUT)
    print(play_game(real_puzzle))
    assert play_part_two(TEST_INPUT) == 12, play_part_two(TEST_INPUT)
    print(play_part_two(real_puzzle))


if __name__ == "__main__":
    main()

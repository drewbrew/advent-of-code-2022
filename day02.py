"""Day 2: paper, rock, scissors"""
from pathlib import Path

ME_ROCK = "X"
ME_PAPER = "Y"
ME_SCISSORS = "Z"
OPPONENT_ROCK = "A"
OPPONENT_PAPER = "B"
OPPONENT_SCISSORS = "C"

SCORES = {
    OPPONENT_ROCK: 1,  # ROCK
    ME_ROCK: 1,
    OPPONENT_PAPER: 2,  # PAPER
    ME_PAPER: 2,
    OPPONENT_SCISSORS: 3,  # SCISSORS
    ME_SCISSORS: 3,
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

    if (opponent, me) in [
        (OPPONENT_ROCK, ME_ROCK),
        (OPPONENT_PAPER, ME_PAPER),
        (OPPONENT_SCISSORS, ME_SCISSORS),
    ]:
        # draw
        return SCORES[me] + DRAW
    if (opponent, me) in [
        (OPPONENT_ROCK, ME_PAPER),
        (OPPONENT_PAPER, ME_SCISSORS),
        (OPPONENT_SCISSORS, ME_ROCK),
    ]:
        return SCORES[me] + WIN
    return SCORES[me] + LOSS


def play_round_part_2(turn: tuple[str, str]) -> int:
    opponent, result = turn
    if result == ME_ROCK:  # lose
        losses = {
            OPPONENT_ROCK: ME_SCISSORS,
            OPPONENT_PAPER: ME_ROCK,
            OPPONENT_SCISSORS: ME_PAPER,
        }
        me = losses[opponent]
    elif result == ME_PAPER:  # draw
        draws = {
            OPPONENT_ROCK: ME_ROCK,
            OPPONENT_PAPER: ME_PAPER,
            OPPONENT_SCISSORS: ME_SCISSORS,
        }
        me = draws[opponent]
    else:
        wins = {
            OPPONENT_ROCK: ME_PAPER,
            OPPONENT_PAPER: ME_SCISSORS,
            OPPONENT_SCISSORS: ME_ROCK,
        }
        me = wins[opponent]
    return play_round((opponent, me))


def play_game(puzzle: list[str]) -> int:
    game = parse_input(puzzle)
    return sum(play_round(turn) for turn in game)


def play_part_two(puzzle: list[str]) -> int:
    game = parse_input(puzzle)
    return sum(play_round_part_2(turn) for turn in game)


def main():
    real_puzzle = Path("day02.txt").read_text().splitlines()
    assert play_game(TEST_INPUT) == 15, play_game(TEST_INPUT)
    print(play_game(real_puzzle))
    assert play_part_two(TEST_INPUT) == 12, play_part_two(TEST_INPUT)
    print(play_part_two(real_puzzle))


if __name__ == "__main__":
    main()

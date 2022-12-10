"""Day 10: CRT"""

from pathlib import Path

TEST_INPUT = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop""".splitlines()


WIDTH = 40
HEIGHT = 6


class CPU:
    def __init__(self, instructions: list[str], part_two: bool = False):
        self.register = 1
        self.instructions = instructions
        self.cycles_completed = 0
        self.current_instr_cycles_remaining = 0
        self.signal_strengths: list[int] = []
        self.part_two = part_two
        self.reporting_thresholds = [20, 60, 100, 140, 180, 220]

    def addx(self, value: int):
        instructions = 2
        while instructions > 0:
            self.increment_and_report()
            instructions -= 1
        self.register += value

    def increment_and_report(self):
        if self.part_two:
            horizontal_position = self.cycles_completed % WIDTH
            if horizontal_position == 0:
                print("")  # new line
            if abs(horizontal_position - self.register) <= 1:
                print("#", end="")
            else:
                print(" ", end="")

        self.cycles_completed += 1
        if not self.part_two and self.cycles_completed in self.reporting_thresholds:
            self.signal_strengths.append(self.register)

    def run(self) -> int:
        for instruction in self.instructions:
            if instruction == "noop":
                self.increment_and_report()
            else:
                words = instruction.split()
                if words[0] == "addx":
                    self.addx(int(words[1]))
                else:
                    raise ValueError("unknown instruction" + instruction)
        if self.part_two:
            print("")
            return 0
        return sum(
            strength * cycle
            for strength, cycle in zip(self.signal_strengths, self.reporting_thresholds)
        )


def part_one(puzzle: list[str], part_two: bool = False) -> int:
    return CPU(puzzle, part_two=part_two).run()


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 13140, part_one_result
    puzzle = Path("day10.txt").read_text().splitlines()
    print(part_one(puzzle))
    part_one(puzzle, True)


if __name__ == "__main__":
    main()

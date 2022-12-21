from pathlib import Path
from collections import deque
from math import log10

TEST_INPUT = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32""".splitlines()


def parse_input(puzzle: list[str]) -> list[tuple[str, int] | tuple[str, str, str]]:
    output = []
    for line in puzzle:
        words = line.split()
        if len(words) == 2:
            output.append((words[0][:-1], int(words[1])))
        else:
            assert len(words) == 4
            output.append((words[0][:-1], words[1], words[2], words[3]))
    return output


def part_one(puzzle: list[str]) -> int:
    """Find what root will be"""
    instructions = parse_input(puzzle)
    results = {}
    while not results.get("root"):
        for line in instructions:
            if results.get(line[0]):
                continue
            if len(line) == 2:
                # yay a real assignment
                results[line[0]] = line[1]
            else:
                operation = line[2]
                operand1 = results.get(line[1])
                operand2 = results.get(line[3])
                if operand1 is None or operand2 is None:
                    results[line[0]] = None
                    continue
                if operation == "/":
                    results[line[0]] = operand1 // operand2
                elif operation == "+":
                    results[line[0]] = operand1 + operand2
                elif operation == "-":
                    results[line[0]] = operand1 - operand2
                elif operation == "*":
                    results[line[0]] = operand1 * operand2
                else:
                    raise ValueError(f"Unknown operation {operation}")
    return results["root"]


def substitute_value(variable: str, puzzle: list[str]) -> int | str:
    line = [i for i in puzzle if i.startswith(f"{variable}:")][0]
    value = line.split(":")[1].strip()
    if "humn" in value:
        print("found dependency on human")
        operands = value.split()
        if operands[0] == "humn":
            return (
                f"(humn {operands[1]} {substitute_value(operands[2], puzzle=puzzle)})"
            )
        return f"({substitute_value(operands[0], puzzle)} {operands[1]} humn)"
    try:
        return int(value)
    except ValueError:
        operands = value.split()
        internal = f"({substitute_value(operands[0], puzzle=puzzle)} {operands[1]} {substitute_value(operands[2], puzzle=puzzle)})"
        try:
            result = eval(internal.replace("/", "//"))
        except NameError:
            return internal
        return result


def part_two(puzzle: list[str]) -> int:
    """Find what humn needs to shout so that root's operands are equal"""
    target_line = [line for line in puzzle if line.startswith("root")][0]
    dependencies = target_line.split(":")[1].strip().split()
    operand1, _, operand2 = dependencies
    print(f"must make {operand1} equal to {operand2}")
    expr1 = substitute_value(operand1, puzzle)
    expr2 = substitute_value(operand2, puzzle)
    print(f"Solve this for humn: {expr1} = {expr2}")
    try:
        target = int(expr1)
    except ValueError:
        target = int(expr2)
        expr = expr1
    else:
        expr = expr2
    # just pick a really big number
    humn = 5_000_000_000_000
    turns = 0
    last_value = None
    last_values = deque([], maxlen=10)
    in_infinite_loop = False
    while True:
        real_value = eval(expr)
        try:
            real_value = int(real_value)
        except ValueError:
            pass
        else:
            if real_value == target:
                print("\n")
                return humn
        difference = target - real_value

        if difference > 0:
            if not in_infinite_loop and difference > 1_000_000_000_000:
                humn -= 1_000_000_000
            elif not in_infinite_loop and difference > 1_000_000_000:
                humn -= 1_000_000
            elif not in_infinite_loop and difference > 1_000_000:
                humn -= 1_000
            elif not in_infinite_loop and difference > 1000:
                humn -= 100
            else:
                humn -= 1
        else:
            if not in_infinite_loop and difference < -1_000_000_000_000:
                humn += 1_000_000_000
            elif not in_infinite_loop and difference < -1_000_000_000:
                humn += 1_000_00
            elif not in_infinite_loop and difference < -1_000_000:
                humn += 1_000
            elif not in_infinite_loop and difference < -1000:
                humn += 100
            else:
                humn += 1
        if last_value == real_value:
            repeats += 1
            if repeats > 10:
                raise ValueError(f"Found infinite loop at {last_value}")
        else:
            repeats = 0

        last_value = real_value
        last_values.appendleft(humn)
        turns += 1
        if turns > 500000 and len(set(last_values)) < 500000:
            if not in_infinite_loop:
                print(f"\ninfinite loop detected at {turns}")
            in_infinite_loop = True
        else:
            if in_infinite_loop:
                print(f"\nloop cleared at {turns}")
            in_infinite_loop = False
        if not turns % 1001:
            print(
                f"{turns=}\t{humn=}, {real_value=}, {last_value=}, {difference=}, {round(log10(abs(difference)))}, {last_values[0] - last_values[1]}, {in_infinite_loop=}",
                end="\r",
            )


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 152, part_one_result
    puzzle = Path("day21.txt").read_text().splitlines()
    print(part_one(puzzle=puzzle))
    print(part_two(puzzle=puzzle))


if __name__ == "__main__":
    main()

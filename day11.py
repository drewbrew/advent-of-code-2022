"""Day 11: monkey in the middle"""

from pathlib import Path
from collections import deque


TEST_INPUT = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1""".splitlines()


ITEM_TYPE = deque[int]


class Monkey:
    def __init__(
        self,
        monkey_number: int,
        starting_items: ITEM_TYPE,
        operation: str,
        modulus: int,
        part_one: bool = True,
    ) -> None:
        self.starting_items = starting_items
        self.monkey_number = monkey_number
        operands = operation.split()
        assert operands[:3] == ["new", "=", "old"], operands
        self.other_operand = operands[-1]

        if operands[-2] == "*":
            # print(f'    Worry level is multiplied by {value} to {item * value}')
            self.operation = self.multiply_by
        else:
            assert operands[-2] == "+"
            # print(f'    Worry level increases by {value} to {item + value}')
            self.operation = self.increase_by
        self.modulus = modulus
        self.true_destination: Monkey | None = None
        self.false_destination: Monkey | None = None
        self.items_inspected = 0
        if part_one:
            self.worry_divisor = 3
        else:
            self.worry_divisor = 1
        self.part_one = part_one
        self.destress: int | None = None

    def increase_by(self, item: int) -> int:
        if self.other_operand == "old":
            return item + item
        return item + int(self.other_operand)

    def multiply_by(self, item: int) -> int:
        if self.other_operand == "old":
            return item * item
        return item * int(self.other_operand)

    def inspect(self) -> int:
        item = self.starting_items.popleft()
        # print(f'  Monkey inspects an item with a worry level of {item}' )
        self.items_inspected += 1

        item = self.operation(item)

        item = item // self.worry_divisor
        # print(f'   Monkey gets bored with item. Worry level is divided by 3 to {item}')
        return item

    def throw(self) -> None:
        assert self.true_destination is not None
        assert self.false_destination is not None
        item_thrown = self.inspect()
        if item_thrown % self.modulus:
            # print(f'    Item is not divisible by {self.modulus}')
            # not divisible, so this is the false case
            self.false_destination.receive_item(item_thrown)
        else:
            # print(f'    Item is divisible by {self.modulus}')
            self.true_destination.receive_item(item_thrown)

    def receive_item(self, item: int):
        if not self.part_one:
            item %= self.destress
        self.starting_items.append(item)

    def __str__(self) -> str:
        return f"Monkey {self.monkey_number}"


def take_turn(monkeys: list[Monkey]):
    for index, monkey in enumerate(monkeys):
        # print(f'Monkey {index}:')
        while True:
            try:
                monkey.throw()
            except IndexError:
                # out of items
                break


def part_one(puzzle: list[str], num_turns: int = 20) -> int:
    monkeys = parse_input(puzzle, part_one=num_turns == 20)
    for _ in range(num_turns):
        take_turn(monkeys=monkeys)

    items_inspected = sorted(
        (monkey.items_inspected for monkey in monkeys), reverse=True
    )
    return items_inspected[0] * items_inspected[1]


def parse_input(puzzle: list[str], part_one: bool = True) -> list[Monkey]:
    monkeys: list[Monkey] = []
    true_destinations: dict[int, int] = {}
    false_destinations: dict[int, int] = {}
    monkey_number: int | None = None
    starting_items: ITEM_TYPE = deque()
    operation: str = ""
    modulus: int | None = None
    # because all the moduluses are prime numbers, we can take each thrown item mod their product
    # to act as a destressor
    destressor = 1

    for line in puzzle:
        if not line:
            assert all(
                i is not None
                for i in [
                    starting_items,
                    monkey_number,
                    operation,
                    modulus,
                ]
            )
            monkeys.append(
                Monkey(
                    monkey_number=monkey_number,
                    starting_items=starting_items,
                    operation=operation,
                    modulus=modulus,
                    part_one=part_one,
                )
            )
            assert len(monkeys) == monkey_number + 1
            starting_items = deque()
            operation = ""
            modulus = None
            monkey_number = None
        elif line.startswith("Monkey"):
            monkey_number = int(line.split()[-1][:-1])
        elif line.strip().startswith("Starting items:"):
            starting_items = deque(
                int(i.strip()) for i in line.split(":")[1].strip().split(",")
            )
        elif line.strip().startswith("Operation:"):
            operation = line.split(":")[1].strip()
        elif line.strip().startswith("Test:"):
            modulus = int(line.split()[-1])
            destressor *= modulus
        elif line.strip().startswith("If true:"):
            assert monkey_number is not None
            true_destinations[monkey_number] = int(line.split()[-1])
        elif line.strip().startswith("If false:"):
            assert monkey_number is not None
            false_destinations[monkey_number] = int(line.split()[-1])
        else:
            raise ValueError("Unknown instruction: " + line)

    # and the last monkey
    assert all(
        i is not None
        for i in [
            starting_items,
            monkey_number,
            operation,
            modulus,
        ]
    )
    monkeys.append(
        Monkey(
            monkey_number=monkey_number,
            starting_items=starting_items,
            operation=operation,
            modulus=modulus,
            part_one=part_one,
        )
    )
    assert len(monkeys) == monkey_number + 1

    for thrower, recipient in true_destinations.items():
        monkeys[thrower].true_destination = monkeys[recipient]

    for thrower, recipient in false_destinations.items():
        monkeys[thrower].false_destination = monkeys[recipient]

    for monkey in monkeys:
        monkey.destress = destressor

    return monkeys


def main():
    test_result = part_one(TEST_INPUT)
    assert test_result == 10605, test_result
    real_puzzle = Path("day11.txt").read_text().splitlines()
    print(part_one(real_puzzle))
    part_two_result = part_one(TEST_INPUT, 10000)
    assert part_two_result == 2713310158, part_two_result
    print(part_one(real_puzzle, 10000))


if __name__ == "__main__":
    main()

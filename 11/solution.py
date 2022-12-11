import sys

# requires python 3.9+
from math import lcm 

from typing import List

MAGIC_NUMBER = lcm(7,19,13,3,2,11,17,5)

class Monkey:

    false_throw = None
    true_throw = None

    def __init__(self, items: List[int], operation: callable, test: callable):
        self.items = items
        self.operation = operation
        self.test = test
        self.inspected = 0

    def turn(self, part):
        while len(self.items) > 0:
            item = self.items.pop(0)
            self.inspected += 1
            if part == 1:
                worry = self.operation(item) // 3
            if part == 2:
                # The worry spins out of control and destorys performance
                # So we have to mod by the LCM of all tests to preserve the relevant information
                # while keeping the number small
                #
                # This is the LCM of all monkey's test modulos
                worry = self.operation(item) % MAGIC_NUMBER
            if self.test(worry):
                self.true_throw.items.append(worry)
            else:
                self.false_throw.items.append(worry)

    def __repr__(self) -> str:
        return f"[{self.items}, {self.inspected} inspected"


def get_monkeys():

    # hardcoding inputs, TODO write a parser for this

    MONKEYS = [
        Monkey(
            [93,54,69,66,71],
            lambda x: x * 3,
            lambda x: x % 7 == 0
        ),
        Monkey(
            [89, 51, 80, 66],
            lambda x: x * 17,
            lambda x: x % 19 == 0
        ),
        Monkey(
            [90, 92, 63, 91, 96, 63, 64],
            lambda x: x + 1,
            lambda x: x % 13 == 0
        ),
        Monkey(
            [65, 77],
            lambda x: x + 2,
            lambda x: x % 3 == 0
        ),
        Monkey(
            [76, 68, 94],
            lambda x: x * x,
            lambda x: x % 2 == 0
        ),
        Monkey(
            [86, 65, 66, 97, 73, 83],
            lambda x: x + 8,
            lambda x: x % 11 == 0
        ),
        Monkey(
            [78],
            lambda x: x + 6,
            lambda x: x % 17 == 0
        ),
        Monkey(
            [89, 57, 59, 61, 87, 55, 55, 88],
            lambda x: x + 7,
            lambda x: x % 5 == 0
        ),
    ]

    # dependencies

    MONKEYS[0].true_throw = MONKEYS[7]
    MONKEYS[0].false_throw = MONKEYS[1]

    MONKEYS[1].true_throw = MONKEYS[5]
    MONKEYS[1].false_throw = MONKEYS[7]

    MONKEYS[2].true_throw = MONKEYS[4]
    MONKEYS[2].false_throw = MONKEYS[3]

    MONKEYS[3].true_throw = MONKEYS[4]
    MONKEYS[3].false_throw = MONKEYS[6]

    MONKEYS[4].true_throw = MONKEYS[0]
    MONKEYS[4].false_throw = MONKEYS[6]

    MONKEYS[5].true_throw = MONKEYS[2]
    MONKEYS[5].false_throw = MONKEYS[3]

    MONKEYS[6].true_throw = MONKEYS[0]
    MONKEYS[6].false_throw = MONKEYS[1]

    MONKEYS[7].true_throw = MONKEYS[2]
    MONKEYS[7].false_throw = MONKEYS[5]

    return MONKEYS


# Part 1

monkeys = get_monkeys()
for round in range(20):
    for i in range(len(monkeys)):
        monkeys[i].turn(part=1)

inspections = [m.inspected for m in monkeys]
inspections.sort(reverse=True)
solution = inspections[0] * inspections[1]
print(f"Part 1: {solution}")

# Part 2

monkeys = get_monkeys()
for round in range(10000):
    for i in range(len(monkeys)):
        monkeys[i].turn(part=2)

inspections = [m.inspected for m in monkeys]
inspections.sort(reverse=True)
solution = inspections[0] * inspections[1]

print(f"Part 2: {solution}")
import sys
from copy import copy
from typing import List, Tuple, Dict

if len(sys.argv) >= 2 and sys.argv[1] == "--test":
    print("Using test input")
    filepath = "test_input.txt"
else:
    filepath = "input.txt"

with open(filepath) as ifp:
    rows = ifp.read().splitlines()

# Part 1

equations: Dict[str, Tuple[str, str, str]] = {}
monkeys: Dict[str, int] = {}

for row in rows:
    if len(row.split(" ")) == 2:
        monkeys[row.split(":")[0]] = int(row.split(" ")[1])
    else:
         equations[row.split(":")[0]] = (
            row.split(" ")[1],
            row.split(" ")[2],
            row.split(" ")[3]
         )

# Now that we have dictionaries of resolved and unresolved monkeys
# We can iteravely resolve all of the unresolved monkeys

while True:

    for eq in list(equations):

        a, op, b = equations[eq]
        if a in monkeys and b in monkeys:
            match op:
                case "*":
                    monkeys[eq] = monkeys[a] * monkeys[b]
                case "-":
                    monkeys[eq] = monkeys[a] - monkeys[b]
                case "+":
                    monkeys[eq] = monkeys[a] + monkeys[b]
                case "/":
                    monkeys[eq] = monkeys[a] / monkeys[b]
            del equations[eq]

    if len(equations) == 0:
        break

print(f"Part 1 solution: {int(monkeys['root'])}")

# Part 2 was just done manually with a hacky variant of this and a binary-search like process
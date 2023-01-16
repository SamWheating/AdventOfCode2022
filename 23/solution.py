import sys
from collections import defaultdict
from typing import List, Tuple, Set
from copy import copy

if len(sys.argv) >= 2 and sys.argv[1] == "--test":
    print("Using test input")
    filepath = "test_input.txt"
else:
    filepath = "input.txt"

with open(filepath) as ifp:
    rows = ifp.read().splitlines()

elves = set()
for y in range(len(rows)):
    for x in range(len(rows[y])):
        if rows[y][x] == "#":
            elves.add((y,x))

def get_surrounding_tiles(t: Tuple[int, int]):
    return [
        (t[0]-1, t[1]-1),
        (t[0]-1, t[1]+1),
        (t[0]-1, t[1]),
        (t[0]+1, t[1]-1),
        (t[0]+1, t[1]+1),
        (t[0]+1, t[1]),
        (t[0], t[1]-1),
        (t[0], t[1]+1),
    ]

def get_intention(elf: Tuple[int, int], elves: Set[Tuple[int, int]], priority: List[str]):
    
    neighbours = set()
    for tile in get_surrounding_tiles(elf):
        if tile in elves:
            neighbours.add(tile)

    if len(neighbours) == 0:
        return None # stay where you are

    ns = {
        "N": (elf[0]-1, elf[1]),
        "NE": (elf[0]-1, elf[1]+1),
        "E": (elf[0], elf[1]+1),
        "SE": (elf[0]+1, elf[1]+1),
        "S": (elf[0]+1, elf[1]),
        "SW": (elf[0]+1, elf[1]-1),
        "W": (elf[0], elf[1]-1),
        "NW": (elf[0]-1, elf[1]-1)
    }

    elligible = []

    if ns["N"] not in neighbours and ns["NW"] not in neighbours and ns["NE"] not in neighbours:
        elligible.append("N")

    if ns["S"] not in neighbours and ns["SW"] not in neighbours and ns["SE"] not in neighbours:
        elligible.append("S")
    
    if ns["W"] not in neighbours and ns["SW"] not in neighbours and ns["NW"] not in neighbours:
        elligible.append("W")

    if ns["E"] not in neighbours and ns["SE"] not in neighbours and ns["NE"] not in neighbours:
        elligible.append("E")

    for c in priority:
        if c in elligible:
            return ns[c]

    return None

def part1(elves):

    ROUNDS = 10
    PRIORITY = ["N", "S", "W", "E"]
    
    for r in range(ROUNDS):
        proposals = defaultdict(list) # map of coord: [elves wanting to move there]
        next_elves = set()

        for elf in elves:
            intent = get_intention(elf, elves, PRIORITY)
            if intent is None:
                # This is an elf staying in place
                proposals[elf].append(elf) # prevents other elves from moving there
                next_elves.add(elf)
            else:
                proposals[intent].append(elf)

        # now reconcile all of the intents
        for p in proposals:
            if len(proposals[p]) == 1:
                next_elves.add(p)
            else:
                for elf in proposals[p]:
                    next_elves.add(elf) # all of the elves planning to move here just stay

        assert len(elves) == len(next_elves) # taking attendance
        
        elves = next_elves

        PRIORITY.append(PRIORITY.pop(0))

    max_x = max([e[1] for e in elves])
    min_x = min([e[1] for e in elves])
    max_y = max([e[0] for e in elves])
    min_y = min([e[0] for e in elves])

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    return width*height - len(elves)

def part2(elves):
    
    PRIORITY = ["N", "S", "W", "E"]

    round = 0
    while True:
        round += 1
        proposals = defaultdict(list) # map of coord: [elves wanting to move there]
        next_elves = set()

        for elf in elves:
            intent = get_intention(elf, elves, PRIORITY)
            if intent is None:
                # This is an elf staying in place
                proposals[elf].append(elf) # prevents other elves from moving there
                next_elves.add(elf)
            else:
                proposals[intent].append(elf)

        # now reconcile all of the intents
        for p in proposals:
            if len(proposals[p]) == 1:
                next_elves.add(p)
                moved = True
            else:
                for elf in proposals[p]:
                    next_elves.add(elf) # all of the elves planning to move here just stay

        assert len(elves) == len(next_elves) # taking attendance
        
        if len(elves.union(next_elves)) == len(next_elves):
            # no elves moved
            break
        
        elves = next_elves

        PRIORITY.append(PRIORITY.pop(0))

    return round

print(f"Part 1 Solution: {part1(elves)}")
print(f"Part 2 Solution: {part2(elves)}")
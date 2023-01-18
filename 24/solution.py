import sys
from collections import defaultdict
from typing import List, Tuple, Set, Dict
from copy import copy

if len(sys.argv) >= 2 and sys.argv[1] == "--test":
    print("Using test input")
    filepath = "test_input.txt"
else:
    filepath = "input.txt"

with open(filepath) as ifp:
    rows = ifp.read().splitlines()

storms = defaultdict(list) # map of (y, x): [character] representing each storm on the map
for y, row in enumerate(rows):
    for x, char in enumerate(row):
        if char not in ("#", "."):
            storms[(y, x)].append(char)

WIDTH = len(rows[0])
HEIGHT = len(rows)
START = (0, 1)
GOAL = (HEIGHT-1, WIDTH-2)
MAX_BOARDS = 1000

def advance_storms(storms: Dict[Tuple[int,int], List[str]]):
    
    new_storm = defaultdict(list)
    for coord in storms:
        y, x = coord
        for c in storms[coord]:
            if c == "<":
                if coord[1] == 1: # wrap
                    new_storm[(y,WIDTH-2)].append("<")
                else:
                    new_storm[(y,x-1)].append("<")
            elif c == ">":
                if coord[1] == WIDTH-2: # wrap
                    new_storm[(y,1)].append(">")
                else:
                    new_storm[(y,x+1)].append(">")
            elif c == "^":
                if coord[0] == 1: # wrap
                    new_storm[(HEIGHT-2,x)].append("^")
                else:
                    new_storm[(y-1,x)].append("^")
            elif c == "v":
                if coord[0] == HEIGHT-2: # wrap
                    new_storm[(1,x)].append("v")
                else:
                    new_storm[(y+1,x)].append("v")

    return new_storm

assert advance_storms({(1,1): [">"]}) == {(1,2): [">"]}
assert advance_storms({(1,1): [">"], (1,3): ["<"]}) == {(1,2): [">", "<"]}
assert advance_storms({(1,1): ["^"]}) == {(HEIGHT-2,1): ["^"]}

positions = defaultdict(set)
positions[0].add((0,1))

TRIP_ONE = False # have we made it to the end yet?
TRIP_TWO = False # have we made it back to the start to get a snack yet?
TRIP_THREE = False # have we made it to the end with a snack yet?

for step_num in range(1, 1000000):
    storms = advance_storms(storms)
    for start in positions[step_num-1]: # look at each position in move n-1
        

        possible_next_positions = [
            start,
            (start[0]-1, start[1]),
            (start[0]+1, start[1]),
            (start[0], start[1]-1),
            (start[0], start[1]+1)
        ]

        valid_next_positions = []
        for next_pos in possible_next_positions:
            
            # check for oob:
            if next_pos[0] < 0 or next_pos[0] > HEIGHT or next_pos[1] < 0 or next_pos[1] > WIDTH:
                continue

            # check for walls
            if next_pos[0] == 0 and next_pos[1] != 1:
                continue
            if next_pos[0] == HEIGHT-1 and next_pos[1] != WIDTH-2:
                continue
            if next_pos[1] == 0 or next_pos[1] == WIDTH-1:
                continue
            
            # check for storms:
            if next_pos in storms:
                continue

            positions[step_num].add(next_pos)

    # State tracking stuff to remember how many trips we've done:

    if GOAL in positions[step_num]:
        if not TRIP_ONE:
            print(f"Part 1 Solution: {step_num}")
            TRIP_ONE = True
            positions = defaultdict(set)
            positions[step_num] = {GOAL}

        if TRIP_ONE and TRIP_TWO:
            print(f"Part 2 Solution: {step_num}")
            break

    if START in positions[step_num]:
        if TRIP_ONE and not TRIP_TWO:
            TRIP_TWO = True
            positions = defaultdict(set)
            positions[step_num] = {START}

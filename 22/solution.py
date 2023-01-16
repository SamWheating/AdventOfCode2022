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

class MonkeyMap:

    directions = {
        0: (0, 1), # >
        1: (1, 0), # v
        2: (0,-1), # <
        3: (-1,0)  # ^
    }

    def __init__(self, rows):
        self.squares = set()
        self.walls = set()
        self.y = 0
        self.x = rows[0].index(".")
        self.direction = 0
        self.instructions = self.build_instructions(rows[-1])
        self.board = self.build_board(rows[:-2])
        print(self.instructions)

    def build_instructions(self, row):
        instructions = []
        current_num = ""
        for c in row:
            if c.isdigit():
                current_num += c
            else:
                if current_num != "":
                    instructions.append(int(current_num))
                    current_num = ""
                instructions.append(c)

        return instructions

    def build_board(self, rows):
        for y in range(len(rows)):
            for x in range(len(rows[y])):
                if rows[y][x] == ".":
                    self.squares.add((y,x))
                elif rows[y][x] == "#":
                    self.walls.add((y,x))

    def step(self):
        new_y = self.y + self.directions[self.direction][0]
        new_x = self.x + self.directions[self.direction][1]
        
        if (new_y, new_x) in self.squares:
            self.y = new_y
            self.x = new_x

        elif (new_y, new_x) not in self.walls:
            self.wrap()

    def wrap(self):
        # lazy wrapping implementation - just walk backwards and go through walls
        backwards = self.directions[(self.direction + 2) % 4]
        cursor = (self.y, self.x)
        while True:
            new_cursor = (cursor[0] + backwards[0], cursor[1] + backwards[1])
            if new_cursor in self.squares or new_cursor in self.walls:
                cursor = new_cursor
            else:
                break

        if cursor in self.walls:
            return

        if cursor in self.squares:
            self.y = cursor[0]
            self.x = cursor[1]

    def cubewrap(self):
        pass

    def rotate(self, direction):
        if direction == "L":
            self.direction -= 1
        elif direction == "R":
            self.direction += 1
        self.direction %= 4

    def run(self):
        for i in self.instructions:
            if isinstance(i, str):
                self.rotate(i)
            else:
                for _ in range(i):
                    self.step()

    def score(self):
        return ((self.y + 1) * 1000) + ((self.x + 1) * 4) + self.direction

# Part 1

mm = MonkeyMap(rows)
mm.run()
print(f"Part 1 Solution: {mm.score()}")
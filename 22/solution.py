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

    def __init__(self, rows, cubic=False):
        self.squares = set()
        self.walls = set()
        self.y = 0
        self.x = rows[0].index(".")
        self.direction = 0
        self.width = len(rows[0])//3
        self.instructions = self.build_instructions(rows[-1])
        self.build_board(rows[:-2])
        self.cubic = cubic
        self.edgemap = self.build_edge_map()

    def build_edge_map(self):
        """
        make a map which encodes all possible edge-wrapping

        the format being ((y,x), direction): ((y,x), direction)

        reference diagram:

                       w      2w     3w
                       |      |      |       
            0 _|        __A1__ __B1__      
                       |      |      |
                       E1     |      F1
            w __       |______|__D1__|
                       |      |
                       C1     D2   
            2w _ __C2__|______|           3    
                |      |      |           ^
                E2     |      F2      2 < + >  0
            3w _|______|__G1__|           v
                |      |                  1
                A2     G2 
                |__B2__|

        note: this implementaton is super hacky will only work for 1 of many possible cube nets.
        
        """
        map = {} # ((y,x), d): ((y,x), d)

        for i in range(self.width):
            # A1 -> A2
            map[((0, self.width+i), 3)] = ((3*self.width+i, 0), 0) # >
            # A2 -> A1
            map[((3*self.width+i, 0), 2)] = ((0, self.width+i), 1) # v
            # B1 -> B2
            map[((0, 2*self.width+i), 3)] = ((4*self.width-1, i), 3) # ^
            # B2 -> B1
            map[((4*self.width-1, i), 1)] = ((0, 2*self.width+i), 1) # v
            # C1 -> C2
            map[((self.width+i, self.width), 2)] = ((2*self.width, i), 1) # v
            # C2 -> C1
            map[((2*self.width, i), 3)] = ((self.width+i, self.width), 0) # >
            # D1 -> D2
            map[((self.width-1, 2*self.width+i), 1)] = ((self.width+i, 2*self.width-1), 2) # <
            # D2 -> D1
            map[((self.width+i, 2*self.width-1), 0)] = ((self.width-1, 2*self.width+i), 3) # ^
            # E1 -> E2
            map[((i, self.width), 2)] = ((3*self.width-1-i, 0), 0) # >
            # E2 -> E1
            map[((3*self.width-1-i, 0), 2)] = ((i, self.width), 0) # >
            # F1 -> F2
            map[((i, 3*self.width-1), 0)] = ((3*self.width-1-i, 2*self.width-1), 2) # <
            # F2 -> F1
            map[((3*self.width-1-i, 2*self.width-1), 0)] = ((i, 3*self.width-1), 2) # <
            # G1 -> G2
            map[((3*self.width-1, self.width+i), 1)] = ((3*self.width+i, self.width-1), 2) # <
            # G2 -> G1
            map[((3*self.width+i, self.width-1), 0)] = ((3*self.width-1, self.width+i), 3) # ^

        return map

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

        if current_num != "":
            instructions.append(int(current_num))

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
            if self.cubic:
                self.cubewrap()
            else:
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
        assert ((self.y, self.x), self.direction) in self.edgemap, f"({self.y}, {self.x}) not in edgemap"

        next = self.edgemap[((self.y, self.x), self.direction)]

        if next[0] in self.walls:
            return

        self.y, self.x = next[0]
        self.direction = next[1]

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

# Part 2
mm = MonkeyMap(rows, cubic=True)
mm.run()
print(f"Part 2 Solution: {mm.score()}")

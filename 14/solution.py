import sys
from typing import List, Union
from functools import cmp_to_key

if len(sys.argv) >= 2 and sys.argv[1] == "--test":
    print("Using test input")
    filepath = "test_input.txt"
else:
    filepath = "input.txt"

# ALL COORDS ARE Y,X
#
# y = 0 |
#       |
#       |
# y = 3 |_ _ _ _ _ _
#        ^         ^
#        x = 0     x = 6 

class Coord:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({x},{y})"

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __len__(self):
        return abs(self.x) + abs(self.y)

    def unit(self):
        return Coord(self.x//self.__len__(), self.y//self.__len__())


def between(start: Coord, end: Coord):
    # give a list of all of the coords between two coords (inclusive)
    direction = end - start
    unit = direction.unit()
    assert len(unit) == 1
    points = [start]
    cursor = start
    while True:
        cursor += unit
        points.append(cursor)
        if cursor == end:
            return points


with open(filepath) as ifp:
    rows = ifp.read().splitlines()
    lines = [] # List[List[Tuple[int,int]]]
    for row in rows:
        path = []
        for coord in row.split(" -> "):
            x = int(coord.split(",")[0])
            y = int(coord.split(",")[1])
            path.append(Coord(x,y))

        lines.append(path)

# LEGEND
# " " == air
# "#" == wall
# "X" == sand 
# initialize the board
board = [[" "]*600 for _ in range(600)]

# draw the lines:
for line in lines:
    for i in range(len(line)-1):
        start = line[i]
        end = line[i+1]
        for point in between(start, end):
            board[point.y][point.x] = "#"

# Part 1

grains = 0
try:
    while True: # keep making grains of sand
        assert board[0][500] == " " # ensure start point is clear
        cursor = Coord(x=500,y=0)
        done = False
        while True: # keep falling until it can't
            if board[cursor.y+1][cursor.x] == " ":
                cursor.y += 1
            elif board[cursor.y+1][cursor.x-1] == " ":
                cursor.y += 1
                cursor.x -= 1
            elif board[cursor.y+1][cursor.x+1] == " ":
                cursor.y += 1
                cursor.x += 1
            else:
                board[cursor.y][cursor.x] = "#"
                grains += 1
                break
except IndexError:
    print(f"Part 1: {grains}")

            

# Part 2

max_y = 0
for line in lines:
    for point in line:
        if point.y >= max_y:
            max_y = point.y

board = [[" "]*800 for _ in range(max_y+3)]
board[max_y + 2] = ["#"] * 800

# draw the lines:
for line in lines:
    for i in range(len(line)-1):
        start = line[i]
        end = line[i+1]
        for point in between(start, end):
            board[point.y][point.x] = "#"

grains = 0
while True: # keep making grains of sand
    if board[0][500] != " ":
        break
    cursor = Coord(x=500,y=0)
    done = False
    while True: # keep falling until it can't
        if board[cursor.y+1][cursor.x] == " ":
            cursor.y += 1
        elif board[cursor.y+1][cursor.x-1] == " ":
            cursor.y += 1
            cursor.x -= 1
        elif board[cursor.y+1][cursor.x+1] == " ":
            cursor.y += 1
            cursor.x += 1
        else:
            board[cursor.y][cursor.x] = "#"
            grains += 1
            break

print(f"Part 2: {grains}")

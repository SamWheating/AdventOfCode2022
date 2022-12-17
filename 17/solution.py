import sys
from copy import copy
from typing import List

if len(sys.argv) >= 2 and sys.argv[1] == "--test":
    print("Using test input")
    filepath = "test_input.txt"
else:
    filepath = "input.txt"

with open(filepath) as ifp:
    jets = list(ifp.read())

ROCKS = [
    [
        [".", ".", "@", "@", "@", "@", "."]
    ],
    [
        [".", ".", ".", "@", ".", ".", "."],
        [".", ".", "@", "@", "@", ".", "."],
        [".", ".", ".", "@", ".", ".", "."],
    ],
    [
        [".", ".", ".", ".", "@", ".", "."],
        [".", ".", ".", ".", "@", ".", "."],
        [".", ".", "@", "@", "@", ".", "."],   
    ],
    [
        [".", ".", "@", ".", ".", ".", "."],
        [".", ".", "@", ".", ".", ".", "."],
        [".", ".", "@", ".", ".", ".", "."],
        [".", ".", "@", ".", ".", ".", "."],
    ],
    [
        [".", ".", "@", "@", ".", ".", "."],
        [".", ".", "@", "@", ".", ".", "."],
    ]
]

# operate on a chunk-by-chunk basis, as only 4 rows are involved in a move at any time.

# Part 1:
BOARD = []

def left(chunk: List[List[str]]) -> List[str]:
    # for any @ in the List of List of string, shift them to the left
    # if any encounters an error, return the original
    new_chunk = []
    for row in chunk:
        new_row = [r for r in row]
        for i in range(len(new_row)):
            if new_row[i] == "@":
                if i == 0:
                    return chunk
                if new_row[i-1] != ".":
                    return chunk
                new_row[i-1] = "@"
                new_row[i] = "."
        new_chunk.append(new_row)
    return new_chunk

assert(left([["#", "@", "."],[".", "@", "."]])) == [["#", "@", "."],[".", "@", "."]]
assert(left([[".", "@", "."],[".", "@", "."]])) == [["@", ".", "."],["@", ".", "."]]
assert(left([["#", ".", "@"],[".", ".", "@"]])) == [["#", "@", "."],[".", "@", "."]]
assert(left([["#", ".", "@", "#"]])) == [["#", "@", ".", "#"]]

def right(chunk: List[List[str]]) -> List[str]:
    # for any # in the List of List of string, shift to the right
    # if any encounters an error, return the original chunk
    new_chunk = []
    for row in chunk:
        new_row = [r for r in row]
        for i in range(len(new_row)-1,-1,-1):
            if new_row[i] == "@":
                if i == len(new_row)-1:
                    return chunk
                if new_row[i+1] != ".":
                    return chunk
                new_row[i+1] = "@"
                new_row[i] = "."
        new_chunk.append(new_row)
    return new_chunk

assert(right([["#", "@", "."],[".", "@", "."]])) == [["#", ".", "@"],[".", ".", "@"]]
assert(right([[".", "@", "."],[".", "@", "#"]])) == [[".", "@", "."],[".", "@", "#"]]

def lock(chunk: List[List[str]]):
    # given a chunk, turn all "@" into "#"
    for row in chunk:
        for i in range(len(row)):
            if row[i] == "@":
                row[i] = "#"
    return chunk

assert lock([["#", "@", "."],[".", "@", "."]]) == [["#", "#", "."],[".", "#", "."]]

def down(chunk: List[List[str]]) -> List[str]:
    # given a chunk, move all of the "@" down a row,
    # if any hits an obstacle, return the original chunk
    new_chunk = [[r for r in row] for row in chunk]
    for i in range(len(chunk)-1,0,-1):
        for j in range(len(chunk[i])):
            if new_chunk[i-1][j] == "@":
                if new_chunk[i][j] != ".":
                    return lock(chunk), True
                new_chunk[i][j] = "@"
                new_chunk[i-1][j] = "."

    return new_chunk, False

assert down([["#", "@", "."],[".", ".", "."]])  == ([["#", ".", "."],[".", "@", "."]], False)
assert down([["@", "@", "."],["#", "@", "."]])  == ([["#", "#", "."],["#", "#", "."]], True)
assert down(
    [
        [".", "@", "."],
        [".", "@", "."],
        [".", ".", "."]
    ]) == ([
        [".", ".", "."],
        [".", "@", "."],
        [".", "@", "."]
        ], False
    )

# Part 1:

# initialize the board with the first rock on the floor (saves us from defining a floor mechanism)

def play_teris(moves, blocks):
    # returns the total height of the stack after n moves
    board = [["#", "#", "#", "#", "#", "#", "#"]]
    BL = 0
    for rock_idx in range(moves):

        # Add a new rock to the board
        addition = [copy(row) for row in blocks[rock_idx % len(blocks)]]
        addition.extend(["."]*7 for i in range(3))
        addition.extend(board)

        board = addition

        # establish a chunk
        ctop = 0
        cwidth = len(blocks[rock_idx % len(blocks)]) + 1

        # move it down:
        while True:
            chunk = board[ctop:ctop+cwidth]
            jet = jets.pop(0) # hacky circular list
            jets.append(jet)
            if jet == "<":
                chunk = left(chunk)
            elif jet == ">":
                chunk = right(chunk)
            chunk, stopped = down(chunk)
            board[ctop:ctop+cwidth] = chunk
            ctop += 1
            if stopped:
                break

        # trim the board to only keep the top 5000 rows in memory
        if len(board) > 20000:
            board = board[:-1000]
            BL += 1000

        # trim empty rows off the top of the board
        i = 0
        for i in range(len(board)):
            if board[i] != ["."]*7:
                board = board[i:]
                break

    return len(board) - 1 + BL # remove the floor at the end 


print(f"Part 1: {play_teris(2022, ROCKS)}")


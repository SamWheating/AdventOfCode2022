import sys

if len(sys.argv) >= 2 and sys.argv[1] == "--test":
    print("Using test input")
    filepath = "test_input.txt"
else:
    filepath = "input.txt"

with open(filepath) as ifp:
    rows = ifp.read().splitlines()

DIRECTIONS = {
    "U": (0,1),
    "D": (0,-1),
    "L": (-1, 0),
    "R": (1,0)
}

# Part 1;

solution = 0


head = (0,0)
tail = (0,0)
visited = set()
for row in rows:
    direction = row.split(" ")[0]
    count = int(row.split(" ")[1])
    for i in range(count):
        head = (head[0] + DIRECTIONS[direction][0], head[1] + DIRECTIONS[direction][1])

        dx = head[0] - tail[0]
        dy = head[1] - tail[1]

        if abs(dy) == 2:
            tail = (tail[0], tail[1] + dy//2)
            if abs(dx) == 1:
                tail = (tail[0] + dx, tail[1])
        elif abs(dx) == 2:
            tail = (tail[0] + dx//2, tail[1])
            if abs(dy) == 1:
                tail = (tail[0], tail[1] + dy)

        visited.add(tail)

solution = len(visited)


print(f"Part 1: {solution}")

# Part 2

def print_knots(knots):
    # max_x = max([k[0] for k in knots]) + 1
    # max_y = max([k[1] for k in knots]) + 1
    max_x = max_y = 10
    board = [["." for _ in range(max_x)] for _ in range(max_y)]

    b = False

    for i in range(len(knots)):
        if board[knots[i][1]][knots[i][0]] == ".":
            board[knots[i][1]][knots[i][0]] = str(i)
            if i == 6:
                b = True

    for row in board[::-1]:
        print("".join(row))

    # if b == True:
    #     exit()

# knots[0] is the head, knots[9] is the tail
knots = [(0,0)] * 10
visited = set()
for row in rows:
    direction = row.split(" ")[0]
    count = int(row.split(" ")[1])
    for i in range(count):

        # move the head
        knots[0] = (knots[0][0] + DIRECTIONS[direction][0], knots[0][1] + DIRECTIONS[direction][1])

        # now move all of the other knots sequentially
        for i in range(1,10):

            dx = knots[i-1][0] - knots[i][0]
            dy = knots[i-1][1] - knots[i][1]

            #print(i, dy, dx)

            if abs(dy) == 2:
                knots[i] = (knots[i][0], knots[i][1] + dy//2)
                if dx > 0:
                    knots[i] = (knots[i][0] + 1, knots[i][1])
                if dx < 0:
                    knots[i] = (knots[i][0] - 1, knots[i][1])
            elif abs(dx) == 2:
                knots[i] = (knots[i][0] + dx//2, knots[i][1])
                if dy > 0:
                    knots[i] = (knots[i][0], knots[i][1] + 1)
                if dy < 0:
                    knots[i] = (knots[i][0], knots[i][1] - 1)

        visited.add(knots[9])

        # print("\n\n")    
        # print_knots(knots)

solution = len(visited)

print(f"Part 2: {solution}")
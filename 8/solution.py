import sys

with open("input.txt") as ifp:
    rows = ifp.read().splitlines()

# `python solution.py --test` will use the test input
if len(sys.argv) >= 2 and sys.argv[1] == "--test":
    print("Using test input")
    with open("test_input.txt") as ifp:
        rows = ifp.read().splitlines()

grid = [[int(a) for a in row] for row in rows]
y_max = len(grid)
x_max = len(grid[0])

# Part 1
visible = set()

# look from the left side
for y in range(y_max):
    tallest = -1
    for x in range(x_max):
        if grid[y][x] > tallest:
            tallest = grid[y][x]
            visible.add((x,y))

# look from the right side
for y in range(y_max):
    tallest = -1
    for x in range(x_max-1, -1, -1):
        if grid[y][x] > tallest:
            tallest = grid[y][x]
            visible.add((x,y))

# top down:
for x in range(x_max):
    tallest = -1
    for y in range(y_max):
        if grid[y][x] > tallest:
            tallest = grid[y][x]
            visible.add((x,y))

# bottom up:
for x in range(x_max):
    tallest = -1
    for y in range(y_max-1, -1, -1):
        if grid[y][x] > tallest:
            tallest = grid[y][x]
            visible.add((x,y))

solution = len(visible)


print(f"Part 1 solution: {solution}")

# Part 2

def get_scenery(grid, x, y):
    xr = xl = yu = yd = 0
    height = grid[y][x]
    # to the right:
    for dx in range(x+1, len(grid[0])):
        xr += 1
        if grid[y][dx] >= height:
            break
    # to the left
    for dx in range(x-1, -1, -1):
        xl += 1
        if grid[y][dx] >= height:
            break
    # look down
    for dy in range(y+1, len(grid)):
        yd += 1
        if grid[dy][x] >= height:
            break
    for dy in range(y-1, -1, -1):
        yu += 1
        if grid[dy][x] >= height:
            break

    return xr * xl * yu * yd

max_scenery = 0
for y in range(len(grid)):
    for x in range(len(grid[0])):
        score = get_scenery(grid, x, y)
        if score > max_scenery:
            max_scenery = score


print(f"Part 2 solution: {max_scenery}")
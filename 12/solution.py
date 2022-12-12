import sys

if len(sys.argv) >= 2 and sys.argv[1] == "--test":
    print("Using test input")
    filepath = "test_input.txt"
else:
    filepath = "input.txt"

with open(filepath) as ifp:
    rows = ifp.read().splitlines()

# Part 1:
topo = [list(row) for row in rows]
distances = [[9999 for _ in range(len(topo[0]))] for _ in range(len(topo))] 

start = end = None
for y in range(len(topo)):
    for x in range(len(topo[0])):
        if topo[y][x] == "S":
            start = (y,x)
            topo[y][x] = "a"
        if topo[y][x] == "E":
            end = (y,x)
            topo[y][x] = "z"

distances[start[0]][start[1]] = 0

# look at every square S on the board
# find all of the neightbours N which can move to it
# distances[S] = min(distances[S], *distances[N]+1)
for p in range(1000): # Assume this is enough iterations, might need to adjust
    for y in range(len(topo)):
        for x in range(len(topo[0])):
            # find all valid neighbours
            neighbours = []
            if y > 0:
                neighbours.append((y-1,x))
            if x > 0:
                neighbours.append((y,x-1))
            if y < len(topo)-1:
                neighbours.append((y+1, x))
            if x < len(topo[0])-1:
                neighbours.append((y, x+1))

            distance_to_neighbours = []
            for n in neighbours:
                # we can move from n to y,x iff n is >= y,x - 1
                if ord(topo[n[0]][n[1]]) >=  ord(topo[y][x])-1:
                    distance_to_neighbours.append(distances[n[0]][n[1]])
            
            if len(distance_to_neighbours) == 0:
                continue

            distances[y][x] = min(distances[y][x], min([d+1 for d in distance_to_neighbours]))

    if distances[end[0]][end[1]] < 999:
        break

solution = distances[end[0]][end[1]]
print(f"Part 1: {solution}")

# Part 2:

# same as part 1, but start at the objective and work backwards
topo = [list(row) for row in rows]
distances = [[9999 for _ in range(len(topo[0]))] for _ in range(len(topo))] 

start = end = None
for y in range(len(topo)):
    for x in range(len(topo[0])):
        if topo[y][x] == "S":
            topo[y][x] = "a"
        if topo[y][x] == "E":
            # starting at the z
            start = (y,x)
            topo[y][x] = "z"

distances[start[0]][start[1]] = 0

for p in range(solution): # re-use p1 solution as an upper-bound on required iterations
    for y in range(len(topo)):
        for x in range(len(topo[0])):
            # find all valid neighbours
            neighbours = []
            if y > 0:
                neighbours.append((y-1,x))
            if x > 0:
                neighbours.append((y,x-1))
            if y < len(topo)-1:
                neighbours.append((y+1, x))
            if x < len(topo[0])-1:
                neighbours.append((y, x+1))

            distance_to_neighbours = []
            for n in neighbours:
                # now we're walking "down" the hill, following uphill rules
                # so we can only move to a square if its height is >= current height -1
                if ord(topo[y][x]) >=  ord(topo[n[0]][n[1]])-1:
                    distance_to_neighbours.append(distances[n[0]][n[1]])
            
            if len(distance_to_neighbours) == 0:
                continue

            distances[y][x] = min(distances[y][x], min([d+1 for d in distance_to_neighbours]))


shortest = 10000
for y in range(len(topo)):
    for x in range(len(topo[0])):
        if topo[y][x] == "a":
            shortest = min(shortest, distances[y][x])

print(f"Part 2: {shortest}")
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

distances[end[0]][end[1]] = 0

# Start from the end and work backwards until we reach the start
for p in range(600): # assume this is enough iterations
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

solution = distances[start[0]][start[1]]
print(f"Part 1: {solution}")

shortest = 10000
for y in range(len(topo)):
    for x in range(len(topo[0])):
        if topo[y][x] == "a":
            shortest = min(shortest, distances[y][x])

print(f"Part 2: {shortest}")
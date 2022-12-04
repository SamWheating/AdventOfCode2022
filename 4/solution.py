with open("input.txt") as ifp:
    rows = ifp.read().splitlines()

part1 = part2 = 0
for row in rows:

    a, b = (int(x) for x in row.split(",")[0].split("-"))
    c, d = (int(x) for x in row.split(",")[1].split("-"))

    if (a <= c and b >= d) or (c <= a and d >= b):
        part1 += 1

    if not (b < c or a > d):
        part2 +=1 

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")

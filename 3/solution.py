SCORES = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

with open("input.txt") as ifp:
    sacks = ifp.read().splitlines()

score = 0
for sack in sacks:
    l = set(sack[:int(len(sack)/2)])
    r = (sack[int(len(sack)/2):])
    intersect = l.intersection(r)
    assert len(intersect) == 1
    score += SCORES.index(intersect.pop())
    
print(f"Part 1: {score}")

score = 0
for i in range(0, len(sacks), 3):
    a, b, c = (set(sacks[j]) for j in range(i, i+3))
    intersect = a.intersection(b).intersection(c)
    assert len(intersect) == 1
    score += SCORES.index(intersect.pop())

print(f"Part 2: {score}")

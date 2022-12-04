with open("input.txt") as ifp:
    rows = ifp.read().splitlines()

score = 0
for row in rows:

    a, b = (int(x) for x in row.split(",")[0].split("-"))
    c, d = (int(x) for x in row.split(",")[1].split("-"))
   
    # --a-----b--
    # ----c--d--

    if a <= c:
        if b >= d:
            score += 1
            continue
    if c <= a:
        if d >= b:
            score += 1


print(f"Part 1: {score}")

score = 0
for row in rows:

    a, b = (int(x) for x in row.split(",")[0].split("-"))
    c, d = (int(x) for x in row.split(",")[1].split("-"))

    if a <= c:
        if b >= c:
            score += 1
    else:
        if d >= a:
            score +=1


print(f"Part 2: {score}")
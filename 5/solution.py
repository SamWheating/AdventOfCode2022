with open("input.txt") as ifp:
    rows = ifp.read().splitlines()

NUM_STACKS = 9

def parse_input(rows):
    moves = []
    stacks = {i: [] for i in range(1, NUM_STACKS+1)}
    for row in rows:
        if len(row) == 0:
            continue
        if row[0] == "[":
            for i in range(NUM_STACKS):
                c_idx = 1 + i * 4
                if row[c_idx] != " ":
                    stacks[i+1] = [row[c_idx]] + stacks[i+1]
        elif row[0] == "m":
            num = int(row.split(" ")[1]) 
            fstack = int(row.split(" ")[3]) 
            tstack = int(row.split(" ")[5])

            moves.append((num, fstack, tstack))

    return stacks, moves

# Part 1:
stacks, moves = parse_input(rows)
for num, fstack, tstack in moves:

    for i in range(num):
        a = stacks[fstack].pop()
        stacks[tstack].append(a)

solution = ""
for i in range(NUM_STACKS):
    solution += stacks[i+1].pop()

print(f"Part 1: {solution}")


# Part 2:
stacks, moves = parse_input(rows)
for num, fstack, tstack in moves:
    a = stacks[fstack][-num:]
    stacks[fstack] = stacks[fstack][:-num]
    stacks[tstack] += a

solution = ""
for i in range(NUM_STACKS):
    solution += stacks[i+1].pop()


print(f"Part 2: {solution}")
with open("input.txt") as ifp:
    rows = ifp.read().splitlines()

# with open("test_input.txt") as ifp:
#     rows = ifp.read().splitlines()

def parse_input(rows):
    return rows


# part 1
input = parse_input(rows)
row = rows[0]
for i in range(4,len(row)):
    if len(set(row[i-4:i])) == 4:
        result = i
        break



print(f"Part 1 result: {result}")


# part 2
input = parse_input(rows)
row = rows[0]
for i in range(14,len(row)):
    if len(set(row[i-14:i])) == 14:
        result = i
        break

print(f"Part 2 result: {result}")
with open("input.txt") as ifp:
    lines = ifp.readlines()

## Part 1
max_food = 0
current = 0

food_per_elf = []

for snack in lines:
    if snack == "\n":
        food_per_elf.append(current)
        current = 0
    else:
        current += int(snack)

food_per_elf.sort()

print(f"Part 1 Solution: {food_per_elf[-1]}")
print(f"Part 2 Solution: {sum(food_per_elf[-3:])}")
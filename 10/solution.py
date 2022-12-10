import sys

if len(sys.argv) >= 2 and sys.argv[1] == "--test":
    print("Using test input")
    filepath = "test_input.txt"
else:
    filepath = "input.txt"

with open(filepath) as ifp:
    rows = ifp.read().splitlines()

## Part 1

INTERESTING = [20,60,100,140,180,220]
cycle_values = {1: 1} # map of cycle num to register value
current_cycle = 1

for row in rows:

    if row == "noop":
        current_cycle += 1
        cycle_values[current_cycle] = cycle_values[current_cycle-1]
    
    if row.startswith("addx"):
        current_cycle += 2
        cycle_values[current_cycle-1] = cycle_values[current_cycle-2]
        cycle_values[current_cycle] = cycle_values[current_cycle-2] + int(row[5:])

strength = 0
for cycle in INTERESTING:
    strength += cycle * cycle_values[cycle]

print(f"Part 1: {strength}")

output = [" "] * 240
for i in range(240):
    cycle_num = i + 1
    sprite_position = cycle_values[cycle_num]
    pixel_idx = (i % 40) # the pixel being drawn, from 0-40
    if pixel_idx >= sprite_position -1 and pixel_idx <= sprite_position + 1:
        output[i] = "#"


print("Part 2:\n")
for i in range(6):
    print("".join(output[i*40:i*40+39]))
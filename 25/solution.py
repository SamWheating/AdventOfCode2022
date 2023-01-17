import sys
from collections import defaultdict
from typing import List, Tuple, Set
from copy import copy

if len(sys.argv) >= 2 and sys.argv[1] == "--test":
    print("Using test input")
    filepath = "test_input.txt"
else:
    filepath = "input.txt"

with open(filepath) as ifp:
    rows = ifp.read().splitlines()

DIGITS = {
    "=": -2,
    "-": -1,
    "0": 0, 
    "1": 1,
    "2": 2
}

def snafu_to_int(snafu: str) -> int:
    val = 0
    for i, c in enumerate(snafu[::-1]):
        place = 5**i
        val += place * DIGITS[c]
    return val

assert snafu_to_int("==") == -12
assert snafu_to_int("1=-0-2") == 1747

def int_to_snafu(i: int) -> str:
    """Given and integer, convert it to snafu
    This could be done way more concisely but my brain isn't working."""

    output = ""
    for place in range(30,-1,-1):
        magnitude = 5**place
        best_delta = i
        best_digit = "0"
        for d in DIGITS:
            delta = i - magnitude * DIGITS[d]
            if abs(delta) < abs(best_delta):
                best_delta = abs(delta)
                best_digit = d
        
        output += best_digit
        i -= magnitude * DIGITS[best_digit]

    return output.lstrip("0")

assert int_to_snafu(10) == "20"
assert int_to_snafu(3) == "1="
assert int_to_snafu(1747) == "1=-0-2"

# Part 1:

total = 0
for row in rows:
    total += snafu_to_int(row)

print(f"Part 1: {int_to_snafu(total)}")
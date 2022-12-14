import sys
from typing import List, Union
from functools import cmp_to_key

if len(sys.argv) >= 2 and sys.argv[1] == "--test":
    print("Using test input")
    filepath = "test_input.txt"
else:
    filepath = "input.txt"

with open(filepath) as ifp:
    rows = ifp.read().splitlines()
    rows = [r for r in rows if r != ""]


def tolist(p: Union[int, List]):
    # Wrap and int as a List, leave a List as-is
    if isinstance(p, List):
        return p
    if isinstance(p, int):
        return [p]
    raise Exception("Unexpected type: " + str(type(p)))


# Use custom exceptions as a short-circuit out of a deeply recursive function
class ValidPackets(Exception):
    pass

class InvalidPackets(Exception):
    pass


def validate_packets(l: str, r: str):
    # Wrap the recursive inspection and return based on exception raised
    try:
        inspect_packets(eval(l), eval(r))
    except ValidPackets:
        return True
    except InvalidPackets:
        return False

# Deeply inspect two packets (or subsection of packets)
# If deemed valid / invalid, raise an exception to recurse all the way up
def inspect_packets(l: List, r: List) -> bool:

    if isinstance(l, int) and isinstance(r, int):
        if l > r:
            raise InvalidPackets("left is larger than right")

        if l < r:
            raise ValidPackets("left is smaller than right")

    elif isinstance(l, List) and isinstance(r, List):

        num_l = len(l) 
        for _ in range(num_l):

            if len(l) != 0 and len(r) == 0:
                raise InvalidPackets("right ran out of items first")

            inspect_packets(l.pop(0), r.pop(0))

        if len(l) == 0 and len(r) != 0:
            raise ValidPackets("left ran out of items first")
        
    else: # mixed case List + Int
        inspect_packets(tolist(l), tolist(r))


# tests
assert validate_packets("[1,2,3]", "[4,5,6]")
assert not validate_packets("[4,5,6]","[1,2,3]")
assert validate_packets("[1,2]", "[1,2,3]")
assert not validate_packets("[1,2,3]", "[1,2]")
assert validate_packets("[[1,2,3]]", "[[4,5,6]]")
assert validate_packets("[[1],[2,3,4]]", "[[1],4]")

score = 0
for i in range(0, len(rows), 2):
    p1 = rows[i] # eval will parse string to nested list
    p2 = rows[i+1]
    if validate_packets(p1, p2):
        score += (i//2 + 1) # the 1-based `index of the pair

print(f"Part 1: {score}")

# Part 2

DIVIDER_1 = "[[2]]"
DIVIDER_2 = "[[6]]"
rows.extend([DIVIDER_1, DIVIDER_2])

def packet_comparator(l: str, r: str):
    if validate_packets(l, r):
        return -1
    return 1

a = sorted(rows, key=cmp_to_key(packet_comparator))

# Now just find the dividers and adjust for 1-based indexing 
solution = (a.index(DIVIDER_2)+1) * (a.index(DIVIDER_1)+1)

print(f"Part 2: {solution}")
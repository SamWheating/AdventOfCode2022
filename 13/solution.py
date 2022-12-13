import sys
from typing import List, Union

if len(sys.argv) >= 2 and sys.argv[1] == "--test":
    print("Using test input")
    filepath = "test_input.txt"
else:
    filepath = "input.txt"

with open(filepath) as ifp:
    rows = ifp.read().splitlines()
    rows = [r for r in rows if r != ""]


# Use custom exceptions as a short-circuit out of a deeply recursive function
class ValidPackets(Exception):
    pass

class InvalidPackets(Exception):
    pass

def tolist(p: Union[int, List]):
    if isinstance(p, List):
        return p
    if isinstance(p, int):
        return [p]
    raise "Unexpected type: " + str(type(p))
    
def validate_packets(l: List, r: List):

    try:
        inspect_packets(l, r)
    except ValidPackets:
        return True
    except InvalidPackets:
        return False

    return True


# Follows the convention:
# Returning True -> Known Valid
# Returning False -> Known False
# Returning None -> More information required
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
        
    else:
        inspect_packets(tolist(l), tolist(r))


# tests
assert validate_packets([1,2,3], [4,5,6])
assert not validate_packets([4,5,6],[1,2,3])

assert validate_packets([1,2], [1,2,3])
assert not validate_packets([1,2,3], [1,2])

assert validate_packets([[1,2,3]], [[4,5,6]])

assert validate_packets([[1],[2,3,4]], [[1],4])

score = 0
for i in range(0, len(rows), 2):
    p1 = eval(rows[i]) # eval will parse string to nested list
    p2 = eval(rows[i+1])
    if validate_packets(p1, p2):
        score += (i//2 + 1)

print(f"Part 1: {score}")



rows.extend(["[[2]]", "[[6]]"])

assert len(set(rows)) == len(rows)

# Part 2
matches = {row: 0 for row in rows}
for row in rows:
    for otherrow in [r for r in rows if r != row]:
        p1 = eval(row)
        p2 = eval(otherrow)
        if validate_packets(p1,p2):
            matches[row] += 1

a = sorted(matches, key=lambda row: matches[row], reverse=True)

solution = (a.index("[[2]]")+1) * (a.index("[[6]]")+1)

print(f"Part 2: {solution}")
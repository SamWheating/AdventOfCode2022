with open("input.txt") as ifp:
    datastream = ifp.read()

def find_solution(datastream, n):
    """find the index of the first character in datastream following n unique characters"""
    for i in range(n,len(datastream)):
        if len(set(datastream[i-n:i])) == n:
            return i

print(f"Part 1 result: {find_solution(datastream, 4)}")
print(f"Part 2 result: {find_solution(datastream, 14)}")
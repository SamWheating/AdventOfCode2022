import sys
from copy import copy
from typing import List, Tuple

if len(sys.argv) >= 2 and sys.argv[1] == "--test":
    print("Using test input")
    filepath = "test_input.txt"
else:
    filepath = "input.txt"

with open(filepath) as ifp:
    rows = ifp.read().splitlines()

voxels = []
for row in rows:
    voxel = row.split(",")
    voxels.append(tuple([int(x) for x in voxel]))

# Part 1:
# Each possible face will be present on 0, 1 or 2 voxels total.
# in order to make collisions easier to detect, we can record only three faces on each voxel (top, right, front) and then:
#   - treat the bottom face as the top of the below voxel
#   - consider the left face to be the right face of the voxel beside it
#   - consider the back face to be the front face of the voxel behind

# then its just a matter of iterating through all of the voxels and recording all of the unique faces.

def get_surface_area(voxels: List[Tuple[int]]):

    faces = set()

    for voxel in voxels:
        top = f"t-{voxel[0]},{voxel[1]},{voxel[2]}"
        bottom = f"t-{voxel[0]},{voxel[1]-1},{voxel[2]}"
        right = f"r-{voxel[0]},{voxel[1]},{voxel[2]}"
        left = f"r-{voxel[0]-1},{voxel[1]},{voxel[2]}"
        front = f"f-{voxel[0]},{voxel[1]},{voxel[2]}"
        back = f"f-{voxel[0]},{voxel[1]},{voxel[2]-1}"

        for face in [top, bottom, right, left, front, back]:
            if face in faces:
                faces.remove(face)
            else:
                faces.add(face)

    return len(faces)

print(f"Part 1 Solution: {get_surface_area(voxels)}")

# Part 2:
# 1) Find all finite-size connected components in the negative space
# 2) Subtract the surface area of these from the solution to Part 1

# Assumptions:
# - The largest single connected component represents the open space

def invert_voxels(voxels):
    # given a list of voxels:
    #  - compute the outer limits along all dimensions
    #  - return the negative of the given voxels within this bound
    max_x = max([v[0] for v in voxels])
    max_y = max([v[1] for v in voxels])
    max_z = max([v[2] for v in voxels])

    negative = []
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            for z in range(max_z + 1):
                if (x,y,z) not in voxels:
                    negative.append((x,y,z))

    return negative

def is_adj(a: Tuple[int], b: Tuple[int]):
    # return True if a and b are touching along any faces
    return sorted([abs(a[0]-b[0]), abs(a[1]-b[1]), abs(a[2]-b[2])]) == [0,0,1]

assert is_adj((1,2,4), (1,2,3))
assert not is_adj((0,0,0), (0,1,1))

def join_components(voxels):
    # given a list of voxels, return a list of lists of connected components
    components = []
    voxels = copy(voxels)

    while True:
        
        component = [voxels.pop(0)]

        while True:
            grown = False
            for a in component:
                for b in voxels:
                    if is_adj(a, b):
                        component.append(b)
                        voxels.remove(b)
                        grown = True

            if not grown:
                components.append(component)
                break

        if len(voxels) == 0:
            return components

assert join_components([(0,0,0), (0,0,1)]) == [[(0,0,0), (0,0,1)]]
assert join_components([(0,0,0), (0,0,1), (1,1,1)]) == [[(0,0,0), (0,0,1)], [(1,1,1)]]

empty_spaces = join_components(invert_voxels(voxels))
empty_spaces.sort(key=len)

total_surface = get_surface_area(voxels)
for space in empty_spaces[:-1]:
    total_surface -= get_surface_area(space)

print(f"Part 1 Solution: {total_surface}")

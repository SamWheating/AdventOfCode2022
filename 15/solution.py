import sys
import re
from typing import List
from multiprocessing.pool import Pool

if len(sys.argv) >= 2 and sys.argv[1] == "--test":
    print("Using test input")
    filepath = "test_input.txt"
    SPECIAL_ROW = 10
    SEARCH_RADIUS = 20
else:
    filepath = "input.txt"
    SPECIAL_ROW = 2000000
    SEARCH_RADIUS = 4000000

with open(filepath) as ifp:
    rows = ifp.read().splitlines()

MATCHER = r'.*x=(-?\d*), y=(-?\d*): .*x=(-?\d*), y=(-?\d*)'
rows = [tuple(int(i) for i in re.search(MATCHER, row).groups()) for row in rows]

def project_scan_to_line(sensor_x, sensor_y, beacon_x, beacon_y, line_y):
    """given a sensor and a beacon, provide the interval of x on line
       y=line_y which the sensor observes"""
    distance = abs(sensor_x-beacon_x) + abs(sensor_y-beacon_y)
    dy = abs(line_y - sensor_y) # how far is it from sensor to row of interest
    if distance < dy:
        return None
    dx = abs(distance - dy) # how far along the line do we scan?
    return (sensor_x-dx, sensor_x+dx)

assert project_scan_to_line(8,7,2,10,16) == (8,8)
assert project_scan_to_line(8,7,2,10,15) == (7,9)
assert project_scan_to_line(8,7,2,10,7) == (-1,17)
assert project_scan_to_line(8,7,2,10,7000) is None

def merge_intervals(intervals: List[tuple]):
    """Assuming every interval is nonzero width with i[0] < i[1]"""
    while True:
        changed = False
        for a in range(len(intervals)):
            if changed:
                break
            for b in range(len(intervals)):
                if a == b:
                    continue
                # only check for a overlapping from the left side
                if intervals[a][1] >= intervals[b][0] and intervals[a][0] <= intervals[b][0]:
                    new_interval = (min(intervals[a][0], intervals[b][0]), max(intervals[a][1], intervals[b][1]))
                    intervals = [i for i in intervals if i != intervals[a] and i != intervals[b]]
                    intervals.append(new_interval)
                    changed = True
                    break

        if not changed or len(intervals) == 1:
            break
    return intervals

assert merge_intervals([(1,10), (15,20)]) == [(1,10), (15,20)]
assert merge_intervals([(1,10), (10,20)]) == [(1,20)]
assert merge_intervals([(-10,-5), (-5,10)]) == [(-10,10)]
assert len(merge_intervals([(-10,-5), (-5,10), (8, 15), (-5,-5), (-8, -2)])) == 1

# Part 2:

def check_row(args):
    """given all of the rows, project them all onto the line formed by y=y
    then look for an empty slot in each row"""
    rows, y, search_radius = args
    intervals = []
    for row in rows:
        sx, sy, bx, by = row
        interval = project_scan_to_line(sx, sy, bx, by, y)
        if interval is not None:
            intervals.append(interval)

    intervals = merge_intervals(intervals)

    spanned = False
    for interval in intervals:
        if interval[0] <= 0 and interval[1] >= SEARCH_RADIUS:
            spanned = True
            break

    if not spanned:
        for interval in intervals:
            # is the left edge inside the window of interest?
            if interval[0] < SEARCH_RADIUS and interval[0] > 0:
                x = interval[0] - 1
                break
            # or the right edge:
            elif interval[1] < SEARCH_RADIUS and interval[1] > 0:
                x = interval[1] + 1
                break
        
        return 4000000 * x + y

    return None
    

if __name__ == "__main__":

# part 1:
    intervals = []
    for row in rows:
        sx, sy, bx, by = row
        interval = project_scan_to_line(sx, sy, bx, by, SPECIAL_ROW)
        if interval is not None:
            intervals.append(interval)

    solution = 0
    for i in merge_intervals(intervals):
        solution += (i[1] - i[0]) 

    print(f"Part 1: {solution}")

    # Part 2
    inputs = [(rows, y, SEARCH_RADIUS) for y in range(SEARCH_RADIUS+1)]

    # Use multiprocessing for embarassingly parallel computation
    # to account for inefficient implementation
    with Pool(8) as p:
        for result in p.imap_unordered(check_row, inputs, 10000):
            if result is not None:
                print(f"Part 2: {result}")
                p.terminate()
                break

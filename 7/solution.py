from typing import Dict, Any, List, Union

from pprint import pprint

with open("input.txt") as ifp:
    rows = ifp.read().splitlines()

# with open("test_input.txt") as ifp:
#     rows = ifp.read().splitlines()

def parse(rows: List[str]) -> Dict[Any, Any]:
    """Returns a nested Dict describing the entire Filesystem"""

    current = []
    fs = {"/": {}}
    for row in rows:
        cwd = fs
        for dir in current:
            cwd = cwd[dir]
        if row.startswith("$ cd"):
            if row.split(" ")[2] == "..":
                current.pop()
                continue
            current.append(row.split(" ")[2])
            continue
        if row.startswith("$ ls"):
            continue
        if row.startswith("dir"):
            dir = row.split(" ")[1]
            if dir not in cwd:
                cwd[dir] = {}
            continue
        else:
            filename = row.split(" ")[1]
            size = int(row.split(" ")[0])
            cwd[filename] = size

    return fs

def part1(fs: Dict[Any, Any]) -> int:
    """Given a dict describing the fs, return the
    sum of all Directories under 100000B total size"""

    # flat map of fullpath: total size
    dir_sizes = {}

    def total_size(cwd, dir: Union[Dict[Any, Any], int]):
        
        if isinstance(dir, int):
            return dir
        
        size = 0
        for subdir in dir.keys():
            size += total_size(cwd + "/" + subdir, dir[subdir])

        dir_sizes[cwd] = size
        return size


    total_size("", fs)
    del dir_sizes[""]

    total = 0
    for v in dir_sizes.values():
        if v <= 100000:
            total += v

    return total

fs = parse(rows)
print(f"part 1: {part1(fs)}")

def part2(fs: Dict[Any, Any]) -> int:
    """Given a dict describing the fs, return the largest direce"""

    # flat map of fullpath: total size
    dir_sizes = {}

    def total_size(cwd, dir: Union[Dict[Any, Any], int]):
        
        if isinstance(dir, int):
            return dir
        
        size = 0
        for subdir in dir.keys():
            size += total_size(cwd + "/" + subdir, dir[subdir])

        dir_sizes[cwd] = size
        return size


    total_size("", fs)
    # weird duplication issue :shrug:
    del dir_sizes[""]

    total_size = dir_sizes["//"]
    req = total_size - 40000000

    return min([v for v in dir_sizes.values() if v >= req])

fs = parse(rows)
print(f"part2: {part2(fs)}")
from typing import Dict, Any, List, Union

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


def get_directory_sizes(fs: Dict[str, Any]) -> Dict[str, int]:
    """DFS navigate the filesystem and get the expanded size of any directories"""

    dir_sizes = {} # all of the visited directories

    def dfs(prefix: str, node: Union[int, Dict[str, Any]]):
        
        if isinstance(node, int):
            return node

        dir_size = sum([dfs(prefix + k + "/", node[k]) for k in node])
        dir_sizes[prefix] = dir_size

        return dir_size

    dfs("/", fs["/"]) # recurse the whole FS from the root node

    return dir_sizes

# Part 1:
fs = parse(rows)
directories = get_directory_sizes(fs)
solution = sum([v for v in directories.values() if v <= 100000])
print(f"Part 1: {solution}")

# Part 2:
fs = parse(rows)
directories = get_directory_sizes(fs)
required_size = directories["/"] - 40000000
solution = min([v for v in directories.values() if v >= required_size])
print(f"Part 2: {solution}")

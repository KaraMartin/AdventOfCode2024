# Advent of Code 2024
# Day 1 Problem 8
from collections import defaultdict, Counter
import dataclasses

TEST_INPUT_1 = """0123
1234
8765
9876
"""
TEST_INPUT_2 = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""
ACTUAL_INPUT_FILENAME = "inputs/10.txt"


class Node:
    x: int
    y: int
    value: int
    score: int = 0
    rating: int = 0
    seen: bool = False

    def __init__(self, x: int, y: int, value: int):
        self.x = x
        self.y = y
        self.value = value


@dataclasses.dataclass
class TopoMap:
    grid: list[list[Node]]

    def __init__(self, grid: list[list[int]]):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])
        self.get_all_trailheads()

    def get_all_trailheads(self):
        th = set()
        for i in range(self.height):
            for j in range(self.width):
                n = self.grid[i][j]
                if int(n.value) == 0:
                    th.add((i,j))
        self.trailheads = th

    def node_is_valid(self, n: Node) -> bool:
        return 0 <= n.x < self.width and 0 <= n.y < self.height

    def location_is_valid(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def __str__(self):
        return "\n".join(["".join([str(c.value) for c in row]) for row in self.grid])
    
    def dfs_iter(self, n: Node) -> None:
        S = []
        # we need to keep track of which trailhead we came from
        S.append([n, n])
        seen = set()
        while S:
            #print([n[0].value for n in S])
            v,og = S.pop()
            if (v.y, v.x) not in seen:
                seen.add((v.y, v.x))
                if v.value == 9:
                    og.score += 1
                    continue
                S.extend(
                    [
                        [self.grid[i][j], og]
                        for i,j in [(v.y-1,v.x), (v.y+1,v.x), (v.y,v.x-1), (v.y,v.x+1)]
                        if self.location_is_valid(x=j, y=i)
                        and self.grid[i][j].value == v.value + 1
                    ]
                )

    def dfs(self):
        for th in self.trailheads:
            #print(f"DFS on {th}")
            self.dfs_iter(self.grid[th[0]][th[1]])
        total_score = 0
        for th in self.trailheads:
            #print(f"TH {th} has score {self.grid[th[0]][th[1]].score}")
            total_score += self.grid[th[0]][th[1]].score
        return total_score

    def dfs_p2(self):
        for th in self.trailheads:
            #print(f"DFS on {th}")
            self.dfs_iter_p2(self.grid[th[0]][th[1]])
        total_rating = 0
        for th in self.trailheads:
            #print(f"TH {th} has score {self.grid[th[0]][th[1]].score}")
            total_rating += self.grid[th[0]][th[1]].rating
        return total_rating

    def dfs_iter_p2(self, n: Node) -> None:
        S = []
        # we need to keep track of which trailhead we came from
        # AND the path we took
        S.append([n, n, []])
        while S:
            #print([n[0].value for n in S])
            v,og,seen = S.pop()
            if (v.y, v.x) not in seen:
                if v.value == 9:
                    og.rating += 1
                    continue
                S.extend(
                    [
                        [self.grid[i][j], og, seen + [(v.y, v.x)]]
                        for i,j in [(v.y-1,v.x), (v.y+1,v.x), (v.y,v.x-1), (v.y,v.x+1)]
                        if self.location_is_valid(x=j, y=i)
                        and self.grid[i][j].value == v.value + 1
                    ]
                )

def _parse_input(input_str) -> TopoMap:
    return TopoMap(
        grid=[
            [
                Node(x=x, y=y, value=int(c))
                for x,c in enumerate(row)
            ]
            for y,row in enumerate(input_str.strip().split("\n"))
        ]
    )

def _load_test_input(t: str = TEST_INPUT_1) -> TopoMap:
    return _parse_input(t)

def _load_actual_input() -> TopoMap:
    with open(ACTUAL_INPUT_FILENAME, "r") as f:
        return _parse_input(f.read().strip())

def main()  -> None:
    # Part 1:
    #   a
    #   b
    #   c
    test = _load_test_input(TEST_INPUT_2)
    #print(f"Test: \n{test}\n with trailheads: \n{[t for t in test.trailheads]}")
    print(f"Test 1: {test.dfs()}")
    # should be 36
    
    actual = _load_actual_input()
    print(f"Actual P1: {actual.dfs()}")

    print(f"Test P2: {test.dfs_p2()}")
    # should be 81

    print(f"Actual P2: {actual.dfs_p2()}")
    return

if __name__ == "__main__":
    main()

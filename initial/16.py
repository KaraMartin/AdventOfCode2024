# Advent of Code 2024
# Day 1 Problem 16
import dataclasses
from collections import defaultdict
from functools import reduce
import heapq

TEST_INPUT_1 = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

TEST_INPUT_2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

ACTUAL_INPUT_FILENAME = "inputs/16.txt"

def _parse_input(input_str: str) -> list[str]:
    if input_str == ACTUAL_INPUT_FILENAME:
        with open(ACTUAL_INPUT_FILENAME, "r") as f:
            lines = f.read().strip().split("\n")
    else:
        lines = input_str.strip().split("\n")
    G = defaultdict(str)
    for j,row in enumerate(lines):
        for i, c in enumerate(row):
            if c == "S":
                start = (j, i)
                G[(j, i)] = "."
            elif c == "E":
                end = (j, i)
                G[(j, i)] = "."
            else:
                G[(j, i)] = c
    return G, start, end

def search(
    G: defaultdict,
    start: tuple[int, int],
    end: tuple[int, int],
    dir: tuple[int, int]
)-> int:
    q = [(0, start, dir)]
    heapq.heapify(q)
    visited = set()
    # E, S, W, N
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    while q:
        score, pos, dir = heapq.heappop(q)
        if pos == end:
            return score
        pos_dir = (*pos, *dir)
        if pos_dir not in visited:
            visited.add(pos_dir)
            d_index = dirs.index(dir)
            # check if wall is straight ahead
            y, x = pos[0] + dir[0], pos[1] + dir[1]
            if G[(y, x)] != "#":
                heapq.heappush(q, (score+1, (y,x), dir))
            heapq.heappush(q, (score+1000, pos, dirs[(d_index+1)%4]))
            heapq.heappush(q, (score+1000, pos, dirs[(d_index-1)%4]))
    return -1

def search_p2(
    G: defaultdict,
    start: tuple[int, int],
    end: tuple[int, int]
)-> int:
    # E, S, W, N
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    def adjacencies(current):
        y, x, dy, dx = current
        ny, nx = y + dy, x + dx
        if G[(ny, nx)] != "#":
            yield 1, (ny, nx, dy, dx)
        d_index = dirs.index((dy, dx))
        cw = dirs[(d_index+1)%4]
        ccw = dirs[(d_index-1)%4]
        yield 1000, (y, x, *cw)
        yield 1000, (y, x, *ccw)

    q = [(0, (*start, 0, 1))]
    heapq.heapify(q)
    best_score = None
    distances = defaultdict(lambda: 999_999_999_999)
    from_dict = defaultdict(lambda: set())

    while q:
        score, current = heapq.heappop(q)
        (y, x, dy, dx) = current
        if (y, x) == end:
            if best_score is None:
                print('best path found')
                best_score = score
        else:
            for cost, neighbor in adjacencies(current):
                next_cost = score + cost
                if next_cost < distances[neighbor]:
                    distances[neighbor] = next_cost
                    heapq.heappush(q, (next_cost, neighbor))
                    from_dict[neighbor] = {current}
                elif next_cost <= distances[neighbor]:
                    from_dict[neighbor].add(current)
    # check each approach to end
    for d in dirs:
        print(f"{d}: {distances[(*end, *d)]}")
    stack = [(*end, -1, 0)]
    g = set(stack)
    while stack:
        curr = stack.pop()
        for prev in from_dict[curr]:
            if prev not in g:
                g.add(prev)
                stack.append(prev)
    return g

def print_map(
    G: defaultdict,
    start: tuple[int, int],
    end: tuple[int, int],
    best_tiles: set,
    n: int
) -> None:
    coords = list(set([(y, x) for y,x,_,_ in best_tiles]))
    for j in range(n):
        row = ""
        for i in range(n):
            if (j, i) == start:
                row += "S"
            elif (j, i) == end:
                row += "E"
            elif (j, i) in coords:
                row += "O"
            else:
                row += G[(j, i)]
        print(row)

def check_input(input_str: str) -> int:
    G, s, e = _parse_input(input_str)
    d = (0, 1)
    return search(G, s, e, d)

def check_input_p2(input_str: str) -> int:
    G, s, e = _parse_input(input_str)
    best_tiles = search_p2(G, s, e)
    #print_map(G, s, e, best_tiles, 17)
    unique = list(set([(y, x) for y,x,_,_ in best_tiles]))
    return len(unique)

def main() -> None:
    p1i1 = check_input(TEST_INPUT_1)
    print(f"Test P1: {p1i1}")
    assert p1i1 == 7036

    p1i2 = check_input(TEST_INPUT_2)
    print(f"Test P1: {p1i2}")
    assert p1i2 == 11048

    print(f"Actual P1: {check_input(ACTUAL_INPUT_FILENAME)}")

    p2i1 = check_input_p2(TEST_INPUT_1)
    print(f"Test P2: {p2i1}")
    assert p2i1 == 45

    p2i2 = check_input_p2(TEST_INPUT_2)
    print(f"Test P2: {p2i2}")
    assert p2i2 == 64

    actual = check_input_p2(ACTUAL_INPUT_FILENAME)
    print(f"Actual P2: {actual}")
    return

if __name__ == "__main__":
    main()

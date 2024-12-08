# Advent of Code 2024
# Day 1 Problem 8
from collections import defaultdict

T_in = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

# get input
with open("inputs/08.txt") as f:
    lines = f.read()

def parse_input(inp):
    freqs = defaultdict(list)
    for j,line in enumerate(inp.split("\n")):
        if not line:
            break
        for i, c in enumerate(line):
            if c == ".":
                continue
            else:
                freqs[c] += [(j,i)]
    return freqs

T = parse_input(T_in)
A = parse_input(lines)

def p1(inp):
    parsed_inp = parse_input(inp)
    height = len(inp.split("\n")) - 1
    width = len(inp.split("\n")[0])
    antinodes = set()

    for f in parsed_inp:
        if len(parsed_inp[f]) == 1:
            continue
        for i, (y,x) in enumerate(parsed_inp[f]):
            for _, (yy,xx) in enumerate(parsed_inp[f][i+1:]):
                cands = set()
                dx = abs(x - xx)
                dy = abs(y - yy)
                y1 = min(y, yy) - dy    # N
                y2 = max(y, yy) + dy    # S
                x1 = min(x, xx) - dx    # W
                x2 = max(x, xx) + dx    # E
                if x - xx <= 0 and y - yy <= 0:
                    cands.add((y1, x1))
                    cands.add((y2, x2))
                else:
                    cands.add((y1, x2))
                    cands.add((y2, x1))
                for (yyy,xxx) in cands:
                    if 0 <= yyy < height and 0 <= xxx < width:
                        antinodes.add((yyy,xxx))
    #print_map(inp.split("\n"), antinodes)
    return len(antinodes)

def print_map(grid, antinodes):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if (y,x) in antinodes:
                print("#", end="")
            else:
                print(c, end="")
        print()

print(f"Test input part 1: {p1(T_in)}")
# should be 14

print(f"Part 1: {p1(lines)}")
# 332 - not the right answer, but is for someone else

def p2(inp):
    parsed_inp = parse_input(inp)
    height = len(inp.split("\n")) - 1
    width = len(inp.split("\n")[0])
    antinodes = set()

    for f in parsed_inp:
        if len(parsed_inp[f]) == 1:
            continue
        for i, (y,x) in enumerate(parsed_inp[f]):
            antinodes.add((y,x))
            for _, (yy,xx) in enumerate(parsed_inp[f][i+1:]):
                dx = abs(x - xx)
                dy = abs(y - yy)
                if x - xx <= 0 and y-yy <= 0:
                    y_N = min(y, yy) - dy    # N
                    y_S = max(y, yy) + dy    # S
                    x_W = min(x, xx) - dx    # W
                    x_E = max(x, xx) + dx    # E
                    while 0 <= y_N < height and 0 <= x_W < width:
                        antinodes.add((y_N, x_W))
                        y_N -= dy
                        x_W -= dx
                    while 0 <= y_S < height and 0 <= x_E < width:
                        antinodes.add((y_S, x_E))
                        y_S += dy
                        x_E += dx
                else:
                    y_N = min(y, yy) - dy    # N
                    y_S = max(y, yy) + dy    # S
                    x_W = min(x, xx) - dx    # W
                    x_E = max(x, xx) + dx    # E
                    while 0 <= y_N < height and 0 <= x_E < width:
                        antinodes.add((y_N, x_E))
                        y_N -= dy
                        x_E += dx
                    while 0 <= y_S < height and 0 <= x_W < width:
                        antinodes.add((y_S, x_W))
                        y_S += dy
                        x_W -= dx
    #print_map(inp.split("\n"), antinodes)
    return len(antinodes)

print(f"Test input part 2: {p2(T_in)}")
# should be 34

print(f"Part 2: {p2(lines)}")

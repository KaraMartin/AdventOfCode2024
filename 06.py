# Advent of Code 2024
# Day 1 Problem 6
from collections import defaultdict
from bisect import insort

T_in = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


# get input
with open("06.txt") as f:
    lines = f.read()

def parse_input(inp):
    return [line for line in inp.split("\n") if line]

T = parse_input(T_in)
A = parse_input(lines)

def get_obstacles_and_start(inp):
    obstacles_by_x = defaultdict(list)
    obstacles_by_y = defaultdict(list)
    start = None
    for i,row in enumerate(inp):
        for j, c in enumerate(row):
            if c == "#":
                # so for first obstacle at grid[0][4]
                # we have obstacles_by_x[0] = [4]
                # and obstacles_by_y[4] = [0]
                insort(obstacles_by_y[i], j)
                insort(obstacles_by_x[j], i)
            elif c == "^":
                start = (i,j)
    return obstacles_by_x, obstacles_by_y, start

def p1(inp):
    obs_by_x, obs_by_y, curr_pos = get_obstacles_and_start(inp)
    grid_height = len(inp)
    grid_width = len(inp[0])
    dir = 0
    seen = set()

    while True:
        # check for next obstacle according to direction
        # if there is one:
        #   set next_pos to one before the obstacle
        #   add every space in between to seen
        #   set curr_pos to next_pos
        # if not:
        #   add every space from curr_pos to edge of grid to seen
        #   break
        curr_y, curr_x = curr_pos
        seen.add(curr_pos)
        next_y, next_x = None, None
        obstacle_found = False
        if dir % 4 == 0:
            possible_keys = obs_by_x[curr_x]
            #print(curr_pos, dir % 4, possible_keys[::-1])
            for y in possible_keys[::-1]:
                if y < curr_y:
                    next_y = y + 1
                    obstacle_found = True
                    break
        elif dir  % 4 == 2:
            possible_keys = obs_by_x[curr_x]
            #print(curr_pos, dir % 4, possible_keys)
            for y in possible_keys:
                if y < curr_y:
                    continue
                else:
                    next_y = y - 1
                    obstacle_found = True
                    break
        elif dir % 4 == 1:
            possible_keys = obs_by_y[curr_y]
            #print(curr_pos, dir % 4, possible_keys)
            for x in possible_keys:
                if x < curr_x:
                    continue
                else:
                    next_x = x - 1
                    obstacle_found = True
                    break
        elif dir % 4 == 3:
            possible_keys = obs_by_y[curr_y]
            #print(curr_pos, dir % 4, possible_keys[::-1])
            for x in possible_keys[::-1]:
                if x < curr_x:
                    next_x = x + 1
                    obstacle_found = True
                    break
        
        if not obstacle_found:
            if dir % 4 == 0:
                next_y = 0
            elif dir % 4 == 2:
                next_y = grid_height
            elif dir % 4 == 1:
                next_x = grid_width
            elif dir % 4 == 3:
                next_x = 0

        if next_y:
            for i in range(min(curr_y, next_y), max(curr_y, next_y)):
                seen.add((i, curr_x))
            curr_pos = (next_y, curr_x)
        elif next_x:
            for i in range(min(curr_x, next_x), max(curr_x, next_x)):
                seen.add((curr_y, i))
            curr_pos = (curr_y, next_x)

        if not obstacle_found:
            break
        dir += 1
    #print_map(seen, inp)
    return len(seen)

def print_map(seen, grid):
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "^":
                print("^", end="")
            elif (i,j) in seen:
                print("X", end="")
            else:
                print(c, end="")
        print()

print(f"Test input part 1: {p1(T)}")
# should be 41

print(f"Part 1: {p1(A)}")
# 117 too low
# 411 too low

def check_input_for_p2(inp):
    obs_by_x, obs_by_y, curr_pos = get_obstacles_and_start(inp)
    dir = 0
    # track obstacle with direction it saw before
    obstacles_seen = []

    while True:
        curr_y, curr_x = curr_pos
        next_y, next_x = None, None
        obstacle_found = False
        if dir % 4 == 0:
            possible_keys = obs_by_x[curr_x]
            for y in possible_keys[::-1]:
                if y < curr_y:
                    next_y = y + 1
                    obstacle_found = True
                    obstacles_seen.append((y, curr_x, dir % 4))
                    break
        elif dir  % 4 == 2:
            possible_keys = obs_by_x[curr_x]
            for y in possible_keys:
                if y < curr_y:
                    continue
                else:
                    next_y = y - 1
                    obstacle_found = True
                    obstacles_seen.append((y, curr_x, dir % 4))
                    break
        elif dir % 4 == 1:
            possible_keys = obs_by_y[curr_y]
            for x in possible_keys:
                if x < curr_x:
                    continue
                else:
                    next_x = x - 1
                    obstacle_found = True
                    obstacles_seen.append((curr_y, x, dir % 4))
                    break
        elif dir % 4 == 3:
            possible_keys = obs_by_y[curr_y]
            for x in possible_keys[::-1]:
                if x < curr_x:
                    next_x = x + 1
                    obstacle_found = True
                    obstacles_seen.append((curr_y, x, dir % 4))
                    break
        
        if len(obstacles_seen) >= 5 and obstacles_seen[-1] in obstacles_seen[:-1]:
            return True
        if not obstacle_found:
            return False
        if next_y:
            curr_pos = (next_y, curr_x)
        elif next_x:
            curr_pos = (curr_y, next_x)
        dir += 1

def p2(inp):
    num_positions = 0
    for j, row in enumerate(inp):
        for i, c in enumerate(row):
            if c == "#" or c == "^":
                continue
            #print(j, i)
            inp_copy = inp.copy()
            inp_copy[j] = inp_copy[j][:i] + "#" + inp_copy[j][i+1:]
            if check_input_for_p2(inp_copy):
                #print("found one")
                num_positions += 1
    return num_positions

print(f"Test input part 2: {p2(T)}")
print(f"Part 2: {p2(A)}")


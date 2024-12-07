# Advent of Code 2024
# Day 1 Problem 7
from collections import defaultdict, Counter
from bisect import insort

T_in = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

# get input
with open("07.txt") as f:
    lines = f.read()

def parse_input(inp):
    x = []
    for line in inp.split("\n"):
        if not line:
            break
        result = int(line.split(":")[0])
        nums = [int(y) for y in line.split(":")[1][1:].split(" ")]
        x.append([result, nums])
    return x

T = parse_input(T_in)
A = parse_input(lines)

def test_case(res, nums):
    possible = set([nums[0]])
    for r in nums[1:]:
        possible = {
            a for a in set([r * p for p in possible])
            | set([r + p for p in possible])
            if a <= res
        }
    return res in possible

def p1(inp):
    total = 0
    for res, nums in inp:
        if test_case(res, nums):
            total += res
    return total

print(f"Test input part 1: {p1(T)}")
# should be 

print(f"Part 1: {p1(A)}")

def test_case_p2(res, nums):
    possible = [nums[0]]
    for r in nums[1:]:
        possible = {
            a for a in set([r * p for p in possible])
            | set([r + p for p in possible])
            | set([int("".join([str(p),str(r)])) for p in possible])
            if a <= res
        }
    return res in possible

def p2(inp):
    total = 0
    for res, nums in inp:
        if test_case_p2(res, nums):
            total += res
    return total

print(f"Test input part 2: {p2(T)}")
print(f"Part 2: {p2(A)}")


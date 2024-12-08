# Advent of Code 2024
# Day 1 Problem 1

testL = [3, 4, 2, 1, 3, 3]
testR = [4, 3, 5, 3, 9, 3]

def file_input():
    L = []
    R = []

    f = open("inputs/01.txt", "r")
    while f:
        line = f.readline()
        if len(line) > 0:
            line = line.split()
            L.append(int(line[0]))
            R.append(int(line[1]))
        else:
            break
    return L, R

def day01_p1(L, R):
    # sort left, sort right
    # compare each index, get abs diff
    # add them up

    L.sort()
    R.sort()
    total = 0

    for i,v in enumerate(L):
        total += abs(v - R[i])

    return total

def day01_p2(L, R):
    d = {}
    total = 0

    for r in R:
        if r in d:
            d[r] += 1
        else:
            d[r] = 1

    for l in L:
        if l in d:
            total += l * d[l]

    return total

L, R = file_input()
print(f"Test input part 1: {day01_p1(testL, testR)}")
print(f"Part 1: {day01_p1(L, R)}")
print(f"Test input part 2: {day01_p2(testL, testR)}")
print(f"Part 2: {day01_p2(L, R)}")

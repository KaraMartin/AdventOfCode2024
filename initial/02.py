# Advent of Code 2024
# Day 1 Problem 2

T = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

with open("inputs/02.txt") as f:
    A = f.readlines()

def process(lines):
    if "\n" in lines:
        return [[int(v) for v in line.split(" ")] for line in lines.split("\n")]
    return [[int(v) for v in line.split(" ")] for line in lines]

def check_report(r):
    # check if increasing or decreasing
    # then get all deltas between adjacent values
    # then check  if all meet criteria

    diff = r[0] - r[1]
    # ignore diff == 0

    # decreasing
    if diff > 0:
        deltas = [r[i]-r[i+1] for i in range(len(r)-1)]
        if all([3 >= delta >= 1 for delta in deltas]):
            return True
    # increasing
    elif diff < 0:
        deltas = [r[i+1]-r[i] for i in range(len(r)-1)]
        if all([3 >= delta >= 1 for delta in deltas]):
            return True
    return False

# for each record:
#   check if it meets criteria
#   if so increment counter
def p1(lines):
    records = process(lines)
    meets_criteria = [check_report(r) for r in records]
    return meets_criteria.count(True)

def p2(lines):
    records = process(lines)
    meets_criteria = [check_report(r) for r in records]
    for j,already_passes in enumerate(meets_criteria):
        if not already_passes:
            r = records[j]
            for i in range(len(r)):
                if check_report(r[:i] + r[i+1:]):
                    meets_criteria[j] = True
                    break
    return meets_criteria.count(True)

## PART 1
print(f"Test input part 1: {p1(T)}")
# should be 2
print(f"Part 1: {p1(A)}")

## PART 2
print(f"Test input part 2: {p2(T)}")
# should be 4
print(f"Part 2: {p2(A)}")

# Advent of Code 2024
# Day 1 Problem 3

T = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""

MIN_COMMAND = "mul(1,1)"
MIN_DIGITS = 1
MAX_DIGITS = 3
LEN_MIN_COMMAND = len(MIN_COMMAND)
MUL = "mul("
LEN_MUL = len(MUL)
NUMS = "0123456789"
COMMA = ","
R_PAREN = ")"

# get input
with open("03.txt") as f:
    A = "".join(a for a in f.readlines())

def p1(memory):
    L = 0
    R = len(memory)-LEN_MIN_COMMAND+1
    total = 0

    while L < R:
        if memory[L:L+LEN_MUL] == MUL:
            L += LEN_MUL
            first = ""
            second = ""

            while memory[L] in NUMS:
                first += memory[L]
                L += 1
            if MIN_DIGITS <= len(first) <= MAX_DIGITS and memory[L] == COMMA:
                L += 1
            else:
                continue

            while memory[L] in NUMS:
                second += memory[L]
                L += 1
            if MIN_DIGITS <= len(second) <= MAX_DIGITS and memory[L] == R_PAREN:
                total += int(first) * int(second)
                L += 1
        else:
            L += 1
    return total

print(f"Test input part 1: {p1(T)}")
print(f"Part 1: {p1(A)}")

T2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

DO = r"do()"
DONT = r"don't()"
LEN_DO = len(DO)
LEN_DONT = len(DONT)

def p2(memory):
    L = 0
    R = len(memory)-LEN_MIN_COMMAND+1
    total = 0
    enabled = True

    while L < R:
        if memory[L:L+LEN_MUL] == MUL:
            L += LEN_MUL
            first = ""
            second = ""

            while memory[L] in NUMS:
                first += memory[L]
                L += 1
            if MIN_DIGITS <= len(first) <= MAX_DIGITS and memory[L] == COMMA:
                L += 1
            else:
                continue

            while memory[L] in NUMS:
                second += memory[L]
                L += 1
            if enabled and MIN_DIGITS <= len(second) <= MAX_DIGITS and memory[L] == R_PAREN:
                total += int(first) * int(second)
                L += 1
        elif memory[L:L+LEN_DO] == DO:
            enabled = True
            L += LEN_DO
        elif memory[L:L+LEN_DONT] == DONT:
            enabled = False
            L += LEN_DONT
        else:
            L += 1
    return total

print(f"Test input part 2: {p2(T2)}")
print(f"Part 2: {p2(A)}")

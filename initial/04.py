# Advent of Code 2024
# Day 1 Problem 4

T = ["MMMSXXMASM",
"MSAMXMSMSA",
"AMXSXMAAMM",
"MSAMASMSMX",
"XMASAMXAMM",
"XXAMMXXAMA",
"SMSMSASXSS",
"SAXAMASAAA",
"MAMMMXMMMM",
"MXMXAXMASX"]

# get input
with open("inputs/04.txt") as f:
    lines = f.readlines()

X = "X"
M = "M"
A = "A"
S = "S"
XMAS = "XMAS"
len_XMAS = len(XMAS)

def p1(wordsearch):
    total = 0
    pws = pad_wordsearch(wordsearch)
    for i,row in enumerate(pws):
        #print(row)
        for j,letter in enumerate(row):
            if letter == X:
                # thank you copilot for my autocompletions
                # check NW
                if all([pws[i-1][j-1] == M, pws[i-2][j-2] == A, pws[i-3][j-3] == S]):
                    #print(f"NW @ {i, j}")
                    total += 1
                # check N
                if all([pws[i-1][j] == M, pws[i-2][j] == A, pws[i-3][j] == S]):
                    #print(f"N @ {i, j}")
                    total += 1
                # check NE
                if all([pws[i-1][j+1] == M, pws[i-2][j+2] == A, pws[i-3][j+3] == S]):
                    #print(f"NE @ {i, j}")
                    total += 1
                # check W
                if all([pws[i][j-1] == M, pws[i][j-2] == A, pws[i][j-3] == S]):
                    #print(f"W @ {i, j}")
                    total += 1
                # check E
                if all([pws[i][j+1] == M, pws[i][j+2] == A, pws[i][j+3] == S]):
                    #print(f"E @ {i, j}")
                    total += 1
                # check SW
                if all([pws[i+1][j-1] == M, pws[i+2][j-2] == A, pws[i+3][j-3] == S]):
                    #print(f"SW @ {i, j}")
                    total += 1
                # check S
                if all([pws[i+1][j] == M, pws[i+2][j] == A, pws[i+3][j] == S]):
                    #print(f"S @ {i, j}")
                    total += 1
                # check SE
                if all([pws[i+1][j+1] == M, pws[i+2][j+2] == A, pws[i+3][j+3] == S]):
                    #print(f"SE @ {i, j}")
                    total += 1
    return total

def pad_wordsearch(wordsearch):
    height = len(wordsearch)
    width = len(wordsearch[0]) + 2 * len_XMAS
    new_wordsearch = ["." * width for _ in range(len_XMAS)]
    for row in wordsearch:
        new_row = "".join(["." * len_XMAS, row , "." * len_XMAS])
        new_wordsearch.append(new_row)
    new_wordsearch += ["." * width for _ in range(len_XMAS)]
    return new_wordsearch

print(f"Test input part 1: {p1(T)}")
# should be 18
print(f"Part 1: {p1(lines)}")

def p2(wordsearch):
    total = 0
    pws = pad_wordsearch(wordsearch)
    for i,row in enumerate(pws):
        #print(row)
        for j,letter in enumerate(row):
            if letter == A:
                # thank you copilot for my autocompletions
                # check MSMS
                if all([pws[i-1][j-1] == M, pws[i-1][j+1] == S, pws[i+1][j-1] == M, pws[i+1][j+1] == S]):
                    total += 1
                # check MMSS
                if all([pws[i-1][j-1] == M, pws[i-1][j+1] == M, pws[i+1][j-1] == S, pws[i+1][j+1] == S]):
                    total += 1
                # check SMSM
                if all([pws[i-1][j-1] == S, pws[i-1][j+1] == M, pws[i+1][j-1] == S, pws[i+1][j+1] == M]):
                    total += 1
                # check SSMM
                if all([pws[i-1][j-1] == S, pws[i-1][j+1] == S, pws[i+1][j-1] == M, pws[i+1][j+1] == M]):
                    total += 1
    return total

print(f"Test input part 2: {p2(T)}")
# should be 9
print(f"Part 2: {p2(lines)}")

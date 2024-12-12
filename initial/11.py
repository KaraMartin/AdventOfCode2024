# Advent of Code 2024
# Day 1 Problem 11
import math
from collections import defaultdict

TEST_INPUT_1 = """0 1 10 99 999
"""
TEST_INPUT_2 = """125 17
"""
ACTUAL_INPUT_FILENAME = "inputs/11.txt"


def _parse_input(input_str) -> list[int]:
    return [int(c) for c in input_str.strip().split()]

def _load_test_input(t: str = TEST_INPUT_1) -> list[int]:
    return _parse_input(t)

def _load_actual_input() -> list[int]:
    with open(ACTUAL_INPUT_FILENAME, "r") as f:
        return _parse_input(f.read().strip())

def get_num_digits(n: int) -> int:
    return math.floor(math.log10(n)) + 1

def blink(inp: list[int]) -> list[int]:
    outp = []
    for i,v in enumerate(inp):
        #print(f"outp: {outp}")
        if v == 0:
            outp.append(1)
            continue
        if (v_len := math.floor(math.log10(v)) + 1) % 2 == 0:
            mid = v_len//2
            div = 10**mid
            outp.append(v//div)
            outp.append(v%div)
        else:
            outp.append(v * 2024)
    return outp

def blink_n_times(inp: list[int], n: int) -> int:
    for i in range(n):
        inp = blink(inp)
    return len(inp)

# p2 stuff
cache = defaultdict(int)

def blink_rec(n: int, depth: int) -> int:
    if (n, depth) in cache:
        return cache[(n, depth)]
    children = blink([n])
    if depth == 1:
        cache[(n, depth)] = len(children)
        return cache[(n, depth)]
    total_size = sum([
        blink_rec(c, depth-1)
        for c in children
    ])
    cache[(n, depth)] = total_size
    return cache[(n, depth)]

def p2(inp: list[int], depth: int) -> int:
    return sum([blink_rec(n, depth) for n in inp])

def main() -> None:
    test = _load_test_input(TEST_INPUT_2)
    print(test)
    test_out = blink_n_times(test, 25)
    print(f"Test 1: {test_out}")
    # should be 55312

    actual = _load_actual_input()
    print(f"Actual P1: {blink_n_times(actual, 25)}")

    # actually lets cache the final number of stones based on input
    # then we can just calculate based on that

    #print(f"Actual P2: {blink_n_times_with_caching(actual, 75)}")
    # The idea here will be to cache number of stones at each step
    # 0 -> 1 -> 2024 -> 20, 24 -> 2, 0, 2, 4 ...
    # {0: [1, 1, 1, 2, 4, ...]}
    # then whenever we see 0 at any point in another stones processing
    # we can calculate the number of stones we will get n steps later
    test_2 = p2([0], 25)
    print(f"Test 2: {test_2}")
    actual_2 = p2(actual, 75)
    print(f"Actual P2: {actual_2}")
    return

if __name__ == "__main__":
    main()

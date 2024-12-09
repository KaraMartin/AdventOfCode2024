from collections import Counter
import dataclasses

TEST_INPUT = """3   4
4   3
2   5
1   3
3   9
3   3"""
ACTUAL_INPUT_FILENAME = "inputs/01.txt"

@dataclasses.dataclass
class IDList:
    left: list[int]
    right: list[int]

    def __post_init__(self):
        self.left = sorted(self.left)
        self.right = sorted(self.right)
        self.frequency_r = Counter(self.right)

    def distances(self) -> list[int]:
        return [abs(l - r) for l, r in zip(self.left, self.right)]

    def sum_distances(self) -> int:
        return sum(self.distances())

    def similarity_score(self) -> int:
        return sum([l * self.frequency_r[l] for l in self.left])

def _parse_input(input_str) -> IDList:
    left_nums, right_nums = zip(
        *[
            map(int, line.split())
            for line in input_str.strip().split("\n")
        ]
    )
    return IDList(left=left_nums, right=right_nums)

def _load_test_input() -> IDList:
    return _parse_input(TEST_INPUT)

def _load_actual_input() -> IDList:
    with open(ACTUAL_INPUT_FILENAME, "r") as f:
        return _parse_input(f.read())

def main()  -> None:
    # Part 1:
    #   Pair up the smallest number in the left list
    #   with the smallest number in the right list.
    #   Sum up the distances between these pairs.
    test_locations = _load_test_input()
    actual_locations = _load_actual_input()
    test_distances = test_locations.sum_distances()
    actual_distances = actual_locations.sum_distances()
    assert test_distances == 11

    print(f"Day 1 Part 1, Sum of distances:")
    print(f"    Test:   {test_distances}")
    print(f"    Actual: {actual_distances}")

    # Part 2:
    #   Calculate a total similarity score based on 
    #   summing up the product of left numbers with occurances
    #   from the right list.
    test_score = test_locations.similarity_score()
    actual_score = actual_locations.similarity_score()
    assert test_score == 31

    print(f"Day 1 Part 2, Similarity score:")
    print(f"    Test:   {test_score}")
    print(f"    Actual: {actual_score}")

if __name__ == "__main__":
    main()

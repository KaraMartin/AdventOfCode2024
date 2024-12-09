import dataclasses

TEST_INPUT = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
ACTUAL_INPUT_FILENAME = "inputs/02.txt"


@dataclasses.dataclass
class Report:
    # all levels must be increasing or decreasing to be safe
    # any two adjacent levels differ by at least 1 and at most 3
    levels = list[int]

    def print(self) -> None:
        print(self.levels)


@dataclasses.dataclass
class Data:
    reports = list[Report]

    def print(self) -> None:
        for report in self.reports:
            report.print()

def _parse_input(input_str: str) -> Data:
    print([list(map(int, line.split())) for line in input_str.strip().split("\n")])
    return Data([
        Report(
            levels=list(map(int, line.split()))
        )
        for line in input_str.strip().split("\n")
    ])

def _load_test_input() -> Data:
    return _parse_input(TEST_INPUT)

def _load_actual_input() -> Data:
    with open(ACTUAL_INPUT_FILENAME, "r") as f:
        return _parse_input(f.read())

def main() -> None:
    test_data = _load_test_input()
    test_data.print()
    return

if __name__ == "__main__":
    main()

# Advent of Code 2024
# Day 1 Problem 13
import dataclasses

TEST_INPUT_1 = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

ACTUAL_INPUT_FILENAME = "inputs/13.txt"
MAX_PRESSES = 100
CONVERSION_ERROR = 10000000000000

def _parse_input(input_str: str, convert: bool = False) -> list[str]:
    if input_str == ACTUAL_INPUT_FILENAME:
        with open(ACTUAL_INPUT_FILENAME, "r") as f:
            lines = f.read().strip()
    else:
        lines = input_str.strip()

    games = []
    for a, b, p in [game.split("\n") for game in lines.strip().split("\n\n")]:
        aa = a.split(": ")[1].split(", ")
        A = Point(int(aa[0][2:]), int(aa[1][2:]))
        bb = b.split(": ")[1].split(", ")
        B = Point(int(bb[0][2:]), int(bb[1][2:]))
        pp = p.split(": ")[1].split(", ")
        if convert:
            Prize = Point(CONVERSION_ERROR + int(pp[0][2:]), CONVERSION_ERROR + int(pp[1][2:]))
        else:
            Prize = Point(int(pp[0][2:]), int(pp[1][2:]))
        games.append(Game(A, B, Prize))
    return games

@dataclasses.dataclass
class Point:
    X: int
    Y: int

@dataclasses.dataclass
class Game:
    A: Point
    B: Point
    Prize: Point

    def get_cheapest(self) -> int:
        # (point, A presses, B presses)
        frontier = [(0,0,0,0)]
        while frontier:
            x, y, a_presses, b_presses = frontier.pop(0)
            if x == self.Prize.X and y == self.Prize.Y:
                return a_presses * 3 + b_presses
            B_1 = (x+self.B.X, y+self.B.Y, a_presses, b_presses + 1)
            B_2 = (x+self.B.X*2, y+self.B.Y*2, a_presses, b_presses + 2)
            B_3 = (x+self.B.X*3, y+self.B.Y*3, a_presses, b_presses + 3)
            for B in [B_1, B_2, B_3]:
                if B not in frontier and B[3] <= MAX_PRESSES:
                    frontier.append(B)
            if a_presses + 1 <= MAX_PRESSES:
                next_A = (x+self.A.X, y+self.A.Y, a_presses + 1, b_presses)
                frontier.append(next_A)
        return 0

    def get_cheapest_p2(self) -> int:
        B_numerator = self.Prize.Y * self.A.X - self.Prize.X * self.A.Y
        B_denominator = self.B.Y * self.A.X - self.A.Y * self.B.X
        B_presses = B_numerator // B_denominator

        A_numerator = (
            self.Prize.X * self.B.Y * self.A.X
            - self.Prize.X * self.B.X * self.A.Y
            - self.B.X * self.Prize.Y * self.A.X
            + self.B.X * self.A.Y * self.Prize.X
        )
        A_denominator = self.B.Y * self.A.X * self.A.X - self.B.X * self.A.Y * self.A.X
        A_presses = A_numerator // A_denominator
        if (
            self.A.X * A_presses + self.B.X * B_presses == self.Prize.X
            and self.A.Y * A_presses + self.B.Y * B_presses == self.Prize.Y
        ):
            return A_presses * 3 + B_presses
        return 0


def check_input(input_str: str) -> int:
    return sum([G.get_cheapest() for G in _parse_input(input_str)])

def check_input_p2(input_str: str) -> int:
    return sum([G.get_cheapest_p2() for G in _parse_input(input_str, convert=True)])

def main() -> None:
    p1i1 = check_input(TEST_INPUT_1)
    print(f"Test P1: {p1i1}")
    assert p1i1 == 480

    print(f"Actual P1: {check_input(ACTUAL_INPUT_FILENAME)}")

    # p2i1 = check_input_p2(TEST_INPUT_1)
    # print(f"Test P2, input 2: {p2i1}")
    # check for 2nd and 4th

    actual = check_input_p2(ACTUAL_INPUT_FILENAME)
    print(f"Actual P2: {actual}")
    return

if __name__ == "__main__":
    main()

# Advent of Code 2024
# Day 1 Problem 14
import dataclasses
from functools import reduce

TEST_INPUT_1 = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""
TEST_INPUT_2 = """p=2,4 v=2,-3
"""

ACTUAL_INPUT_FILENAME = "inputs/14.txt"

@dataclasses.dataclass
class Point:
    X: int
    Y: int

@dataclasses.dataclass
class Velocity:
    X: int
    Y: int



@dataclasses.dataclass
class Robot:
    position: Point
    velocity: Velocity
    width: int
    height: int

    def move(self) -> None:
        self.position.X += self.velocity.X
        self.position.Y += self.velocity.Y
        self.position.X %= self.width
        self.position.Y %= self.height

def _parse_input(input_str: str, width: int, height: int) -> list[str]:
    if input_str == ACTUAL_INPUT_FILENAME:
        with open(ACTUAL_INPUT_FILENAME, "r") as f:
            lines = f.read().strip().split("\n")
    else:
        lines = input_str.strip().split("\n")
    robots = []
    for line in lines:
        p,v = line[2:].split(" v=")
        x,y = map(int, p.split(","))
        vx,vy = map(int, v.split(","))
        robots.append(Robot(position=Point(X=x, Y=y), velocity=Velocity(X=vx, Y=vy), width=width, height=height))
    return robots

def print_map(robots: list[Robot], width: int, height: int) -> None:
    for y in range(height):
        for x in range(width):
            if any(robot.position.X == x and robot.position.Y == y for robot in robots):
                print("#", end="")
            else:
                print(".", end="")
        print()

def count_quadrants(robots: list[Robot], width: int, height: int) -> int:
    quadrants = [0,0,0,0]
    for robot in robots:
        x = robot.position.X
        y = robot.position.Y
        if x < width//2 and y < height//2:
            quadrants[0] += 1
        elif x > width//2 and y < height//2:
            quadrants[1] += 1
        elif x < width//2 and y > height//2:
            quadrants[2] += 1
        elif x > width//2 and y > height//2:
            quadrants[3] += 1
    return reduce(lambda x,y: x*y, quadrants)

def check_input(input_str: str, width: int, height: int, seconds: int) -> int:
    robots = _parse_input(input_str, width, height)
    for _ in range(seconds):
        #print_map(robots, width, height)
        for robot in robots:
            robot.move()
        #print()
    #print_map(robots, width, height)
    return count_quadrants(robots, width, height)

def check_input_p2(input_str: str, width: int, height: int) -> int:
    robots = _parse_input(input_str, width, height)
    with open("14_output_4.txt", "a") as f:
        def print_map_to_file(robots: list[Robot], width: int, height: int) -> None:
            for y in range(height):
                for x in range(width):
                    if any(robot.position.X == x and robot.position.Y == y for robot in robots):
                        print("#", file=f, end="")
                    else:
                        print(".", file=f, end="")
                print(file=f)
        # manually checked
        #n = 318
        #n = 520
        n = 65
        for _ in range(n):
            for robot in robots:
                robot.move()
        print(n, file=f)
        print_map_to_file(robots, width, height)
        print(file=f)
        while True:
            for _ in range(103):
                n += 1
                for robot in robots:
                    robot.move()
            print(n, file=f)
            print_map_to_file(robots, width, height)
            print(file=f)
            x = input()
    return n

def main() -> None:
    T_width = 11
    T_height = 7
    p1i1 = check_input(TEST_INPUT_1, T_width, T_height, 100)
    print(f"Test P1: {p1i1}")
    assert p1i1 == 12

    ACTUAL_WIDTH = 101
    ACTUAL_HEIGHT = 103
    print(f"Actual P1: {check_input(ACTUAL_INPUT_FILENAME, ACTUAL_WIDTH, ACTUAL_HEIGHT, 100)}")

    # The way this worked was I was spitting out 25 seconds at a time and manually inspecting
    # I noticed a weird pattern at n = 65 and repeating every 103 seconds
    # so I changed the code to only print out this interval and manually checked
    # until I saw the christmas tree.... janky!
    actual = check_input_p2(ACTUAL_INPUT_FILENAME, ACTUAL_WIDTH, ACTUAL_HEIGHT)
    print(f"Actual P2: {actual}")
    return

if __name__ == "__main__":
    main()

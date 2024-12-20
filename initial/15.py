# Advent of Code 2024
# Day 1 Problem 15
import dataclasses
from collections import defaultdict

TEST_INPUT_1 = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""
TEST_INPUT_2 = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""
TEST_INPUT_3 = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
"""

ACTUAL_INPUT_FILENAME = "inputs/15.txt"

@dataclasses.dataclass
class Robot:
    X: int
    Y: int
    instructions: list[str]

@dataclasses.dataclass
class Coord:
    X: int
    Y: int

    def __hash__(self):
        return hash((self.Y, self.X))

@dataclasses.dataclass
class Box:
    left: Coord
    right: Coord

    def __hash__(self):
        return hash((self.left, self.right))

@dataclasses.dataclass
class Grid:
    height: int
    width: int
    walls: defaultdict
    boxes: defaultdict
    robot: Robot

    def print_grid(self) -> None:
        for j in range(self.height):
            for i in range(self.width):
                if (j,i) in self.walls:
                    print("#", end="")
                elif (j,i) in self.boxes:
                    print("O", end="")
                elif i == self.robot.X and j == self.robot.Y:
                    print("@", end="")
                else:
                    print(".", end="")
            print()
        return

    def get_GPS(self) -> int:
        return sum([100*j + i for (j,i) in self.boxes.keys()])

    def move_robot(self) -> None:
        m = self.robot.instructions.pop(0)
        #print(f"Moving {m}")
        dir = "^>v<".index(m)
        dirs = [(-1,0), (0,1), (1,0), (0,-1)]
        dy,dx = dirs[dir]
        #print(f"Moving {m} {dy} {dx}")
        curr_y, curr_x = self.robot.Y+dy, self.robot.X+dx
        if (curr_y, curr_x) in self.walls:
            return
        if (curr_y, curr_x) not in self.boxes:
            self.robot.Y += dy
            self.robot.X += dx
            return
        first_box = (curr_y, curr_x)
        while (curr_y, curr_x) in self.boxes:
            curr_y += dy
            curr_x += dx
        if (curr_y, curr_x) in self.walls:
            return
        # else push box up one
        self.boxes.pop(first_box)
        self.boxes[(curr_y, curr_x)] = True
        self.robot.Y += dy
        self.robot.X += dx
        return

    # PART 2

    def print_grid_p2(self) -> None:
        for j in range(self.height):
            for i in range(self.width):
                c = Coord(Y=j,X=i)
                if c in self.walls:
                    print("#", end="")
                elif c in self.boxes:
                    b = self.boxes[c]
                    if c == b.left:
                        print("[", end="")
                    elif c == b.right:
                        print("]", end="")
                elif i == self.robot.X and j == self.robot.Y:
                    print("@", end="")
                else:
                    print(".", end="")
            print()
        return

    def get_GPS_p2(self) -> int:
        return sum([100*L.Y + L.X for L in set([b.left for b in self.boxes.values()])])

    def move_box(self, box: Box, dy: int, dx: int) -> None:
        # print("\t all boxes before: ")
        # for b in self.boxes:
        #     print(f"\t{b}")
        # print(f"Moving box {box} : {dx} {dy}")
        self.boxes.pop(box.left)
        self.boxes.pop(box.right)

        # print("\t all boxes during: ")
        # for b in self.boxes:
        #     print(f"\t{b}")

        new_box = Box(
            left = Coord(Y=box.left.Y+dy, X=box.left.X+dx),
            right = Coord(Y=box.right.Y+dy, X=box.right.X+dx)
        )

        # print(f"\tNew box: {new_box.left}, {new_box.right}")
        self.boxes[new_box.left] = new_box
        self.boxes[new_box.right] = new_box

        # print("\t all boxes after: ")
        # for b in self.boxes:
        #     print(f"\t{b}")

## TODO: account for boxes having a left and right part
    def move_robot_p2(self) -> None:
        m = self.robot.instructions.pop(0)
        dir = "^>v<".index(m)
        # print(f"Trying to move {m}")
        dirs = [(-1,0), (0,1), (1,0), (0,-1)]
        dy,dx = dirs[dir]
        c = Coord(Y=self.robot.Y+dy, X=self.robot.X+dx)
        if c in self.walls:
            # print(f"Hit wall at {c}")
            return
        if c not in self.boxes:
            # print(f"Moving robot to {c}")
            # for b in self.boxes:
                # print(b)
            self.robot.Y += dy
            self.robot.X += dx
            return
        # print("checking boxes")
        boxes_to_move_together = self.get_all_boxes_to_move(dy, dx)
        # print(f"Found boxes to move: {boxes_to_move_together}")
        if not boxes_to_move_together:
            return
        for b in boxes_to_move_together:
            self.move_box(box=b, dy=dy, dx=dx)
        # print([b for b in self.boxes])
        self.robot.Y += dy
        self.robot.X += dx
        return

    def get_all_boxes_to_move(self, dy: int, dx: int) -> list[Box]:
        boxes_to_move = []
        seen = set()
        coords_to_check = [Coord(Y=self.robot.Y, X=self.robot.X)]
        while coords_to_check:
            # print(coords_to_check, boxes_to_move)
            c = coords_to_check.pop(0)
            seen.add(c)
            d = Coord(Y=c.Y+dy, X=c.X+dx)
            # print(f"Checking {c} -> {d}")
            if d in self.boxes:
                box_to_add = self.boxes[d]
                if box_to_add not in boxes_to_move:
                    boxes_to_move.append(box_to_add)
                    L = box_to_add.left
                    R = box_to_add.right
                    if L not in seen and L not in coords_to_check:
                        coords_to_check.append(L)
                    if R not in seen and R not in coords_to_check:
                        coords_to_check.append(R)
            elif d in self.walls:
                return []
        # we need to sort this list based on the direction
        # to ensure that there are open spaces where we move and
        # not other boxes that would overwrite each other
        # print(f"\tBoxes to move: {boxes_to_move}")
        match (dy,dx):
            # moving up
            case (-1, 0):
                boxes_to_move.sort(
                    key=lambda b: (b.left.Y, b.left.X)
                )
            # moving down
            case (1, 0):
                boxes_to_move.sort(
                    key=lambda b: (b.left.Y, b.left.X),
                    reverse=True
                )
            # moving left
            case (0, -1):
                boxes_to_move.sort(
                    key=lambda b: (b.left.X, b.left.Y)
                )
            # moving right
            case (0, 1):
                boxes_to_move.sort(
                    key=lambda b: (b.left.X, b.left.Y),
                    reverse=True
                )
        return boxes_to_move

def _parse_input(input_str: str) -> list[str]:
    if input_str == ACTUAL_INPUT_FILENAME:
        with open(ACTUAL_INPUT_FILENAME, "r") as f:
            grid,instr = f.read().strip().split("\n\n")
            lines = grid.strip().split("\n")
    else:
        grid,instr = input_str.strip().split("\n\n")
        lines = grid.strip().split("\n")
    h = len(lines)
    w = len(lines[0])
    walls = defaultdict()
    boxes = defaultdict()
    for j,row in enumerate(lines):
        for i, c in enumerate(row):
            if c == "#":
                walls[(j,i)] = True
            elif c == "O":
                boxes[(j,i)] = True
            elif c == "@":
                R = Robot(X=i, Y=j, instructions=[c for c in instr if c in "^>v<"])
    return Grid(height=h, width=w, walls=walls, boxes=boxes, robot=R)

def _parse_input_p2(input_str: str) -> list[str]:
    if input_str == ACTUAL_INPUT_FILENAME:
        with open(ACTUAL_INPUT_FILENAME, "r") as f:
            grid,instr = f.read().strip().split("\n\n")
            lines = grid.strip().split("\n")
    else:
        grid,instr = input_str.strip().split("\n\n")
        lines = grid.strip().split("\n")
    h = len(lines)
    w = len(lines[0]) * 2
    walls = defaultdict()
    boxes = defaultdict()
    for j,row in enumerate(lines):
        for i, c in enumerate(row):
            if c == "#":
                walls[Coord(Y=j,X=2*i)] = True
                walls[Coord(Y=j,X=2*i+1)] = True
            elif c == "O":
                L = Coord(X=2*i, Y=j)
                R = Coord(X=2*i+1, Y=j)
                b = Box(left=L, right=R)
                boxes[L] = b
                boxes[R] = b
            elif c == "@":
                robot = Robot(X=2*i, Y=j, instructions=[c for c in instr if c in "^>v<"])
    return Grid(height=h, width=w, walls=walls, boxes=boxes, robot=robot)

def check_input(input_str: str) -> int:
    G = _parse_input(input_str)
    #print(G)
    #print("".join(G.robot.instructions))
    while G.robot.instructions:
        #print(G.robot)
        G.move_robot()
        #G.print_grid()
        #print()
    return G.get_GPS()

def check_input_p2(input_str: str) -> int:
    G = _parse_input_p2(input_str)
    #print(G)
    #G.print_grid_p2()
    #print("".join(G.robot.instructions))
    # for b in G.boxes:
    #     print(f"\t{b}")
    while G.robot.instructions:
        #print(G.robot)
        G.move_robot_p2()
    #     G.print_grid_p2()
    #     print()
    # G.print_grid_p2()
    return G.get_GPS_p2()

def main() -> None:
    # p1i2 = check_input(TEST_INPUT_2)
    # print(f"Test P1: {p1i2}")
    # assert p1i2 == 2028

    # p1i1 = check_input(TEST_INPUT_1)
    # print(f"Test P1: {p1i1}")
    # assert p1i1 == 10092

    #print(f"Actual P1: {check_input(ACTUAL_INPUT_FILENAME)}")

    # === continue from here === #

    p2i3 = check_input_p2(TEST_INPUT_3)
    print(f"Test P2, input 3: {p2i3}")

    p2i1 = check_input_p2(TEST_INPUT_1)
    print(f"Test P2: {p2i1}")
    assert p2i1 == 9021

    actual = check_input_p2(ACTUAL_INPUT_FILENAME)
    print(f"Actual P2: {actual}")
    return

if __name__ == "__main__":
    main()

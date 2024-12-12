# Advent of Code 2024
# Day 1 Problem 12

TEST_INPUT_1 = """AAAA
BBCD
BBCC
EEEC
"""

TEST_INPUT_2 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

TEST_INPUT_3 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""

ACTUAL_INPUT_FILENAME = "inputs/12.txt"


def _parse_input(input_str) -> list[str]:
    if "\n" in input_str:
        return input_str.strip().split("\n")
    return [c for c in input_str]

def _load_test_input(t: str = TEST_INPUT_1) -> list[str]:
    return _parse_input(t)

def _load_actual_input() -> list[str]:
    with open(ACTUAL_INPUT_FILENAME, "r") as f:
        return _parse_input(f.read().strip())

class Region:
    def __init__(self, plant: str, y: int, x: int):
        self.plant = plant
        self.coords = [(y,x)]
        self.area = 1
        self.perimeter = 4
        self.num_sides = 4

    def score(self) -> int:
        return self.area * self.perimeter

    def score_p2(self) -> int:
        return self.area * self.num_sides

    def add_coord(self, y: int, x: int) -> None:
        self.coords.append((y,x))
        above = (y-1,x)
        left = (y,x-1)
        self.area += 1
        #old_sides = self.num_sides
        if above in self.coords:
            up_right = (y-1,x+1)
            if left in self.coords:
                self.perimeter += 0
                if up_right in self.coords:
                    self.num_sides += 0
                else:
                    self.num_sides -= 2
            else:
                self.perimeter += 2
                up_left = (y-1,x-1)
                if up_left in self.coords and up_right in self.coords:
                    self.num_sides += 4
                elif up_left in self.coords or up_right in self.coords:
                    self.num_sides += 2
                else:
                    self.num_sides += 0
        else:
            if left in self.coords:
                self.perimeter += 2
                left_up = (y-1,x-1)
                left_down = (y+1,x-1)
                if left_up in self.coords and left_down in self.coords:
                    self.num_sides += 4
                elif left_up in self.coords or left_down in self.coords:
                    self.num_sides += 2
                else:
                    self.num_sides += 0
            else:
                # Neither above nor left are in this region yet, but we're combining regions
                self.perimeter += 4
                self.num_sides += 4
        # P1 debugging
        #print(f"Added {y},{x} to {self.plant} region, area: {self.area}, perimeter: {self.perimeter}, score: {self.score()}")

        # P2 debugging
        #print(f"[{self.plant}] Added {(y,x)} changing num_sides from {old_sides} to {self.num_sides}")
        return

    def combine(self, other: 'Region', isthmus: tuple[int, int]) -> None:
        self.area += other.area
        self.perimeter += other.perimeter
        self.num_sides += other.num_sides
        self.coords.extend(other.coords)
        self.add_coord(*isthmus)
        return

    def __str__(self):
        return f"[{self.plant}] Area: {self.area}, Perimeter: {self.perimeter}, Score: {self.score()}, Num_sides: {self.num_sides}, Score P2: {self.score_p2()}"

def check_left_and_above(y: int, x: int, plant: str, coord_to_region: dict, regions: list[Region]) -> None:
    above = (y-1,x)
    left = (y,x-1)
    above_and_left = (y-1,x-1)
    if (
        above in coord_to_region and left in coord_to_region
        and coord_to_region[left].plant == coord_to_region[above].plant == plant
        and above_and_left not in coord_to_region[above].coords
        and coord_to_region[left] != coord_to_region[above]
    ):
        # combine the two regions
        upper_region = coord_to_region[above]
        left_region = coord_to_region[left]
        upper_region.combine(left_region, (y,x))
        coord_to_region[(y,x)] = upper_region
        for coord in left_region.coords:
            coord_to_region[coord] = upper_region
        regions.pop(regions.index(left_region))
        return
    if above in coord_to_region and coord_to_region[above].plant == plant:
        my_region = coord_to_region[above]
        my_region.add_coord(y,x)
        coord_to_region[(y,x)] = my_region
        return
    elif left in coord_to_region and coord_to_region[left].plant == plant:
        my_region = coord_to_region[left]
        my_region.add_coord(y,x)
        coord_to_region[(y,x)] = my_region
        return
    coord_to_region[(y,x)] = Region(plant=plant, y=y, x=x)
    regions.append(coord_to_region[(y,x)])
    return

def fence_garden(inp: str) -> int:
    coord_to_region = {}
    regions = []
    garden = _parse_input(inp)
    for y, row in enumerate(garden):
        for x, plant in enumerate(row):
            #print(f"Checking {y},{x} for {plant}")
            check_left_and_above(y, x, plant, coord_to_region=coord_to_region, regions=regions)
    return regions

def calc_score(inp: str) -> int:
    # for region in regions:
    #     print(region)
    return sum(r.score() for r in fence_garden(inp))

def calc_score_p2(inp: str) -> int:
    R = fence_garden(inp)
    # for region in R:
    #     print(region)
    return sum(r.score_p2() for r in R)


def main() -> None:
    p1i1 = calc_score(_load_test_input(TEST_INPUT_1))
    print(f"Test P1: {p1i1}")
    assert p1i1 == 140

    p1i2 = calc_score(_load_test_input(TEST_INPUT_2))
    print(f"Test P1, input 2: {p1i2}")
    assert p1i2 == 1930

    print(f"Actual P1: {calc_score(_load_actual_input())}")

    p2i1 = calc_score_p2(_load_test_input(TEST_INPUT_1))
    print(f"Test P2, input 1: {p2i1}")
    assert p2i1 == 80

    p2i3 = calc_score_p2(_load_test_input(TEST_INPUT_3))
    assert p2i3 == 436
    print(f"Test P2, input 2: {p2i3}")

    p2i2 = calc_score_p2(_load_test_input(TEST_INPUT_2))
    print(f"Test P2, input 2: {p2i2}")
    assert p2i2 == 1206

    actual_2 = calc_score_p2(_load_actual_input())
    print(f"Actual P2: {actual_2}")
    return

if __name__ == "__main__":
    main()

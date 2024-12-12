# Advent of Code 2024
# Day 1 Problem 9
import dataclasses

TEST_INPUT = """2333133121414131402"""
ACTUAL_INPUT_FILENAME = "inputs/09.txt"


@dataclasses.dataclass
class File:
    ID: int
    length: int
    move_attempted: bool

    def __init__(self, ID=-1, length=1, move_attempted=False):
        self.ID = ID
        self.length = length
        self.move_attempted = move_attempted

    def is_empty(self):
        return self.ID == -1


@dataclasses.dataclass
class FileSystem:
    files: list[File]
    last_empty_pos: int = 0

    def has_empty(self):
        return any([f.ID == -1 for f in self.files])
    
    def has_unchecked_file(self):
        return any([f.move_attempted == False for f in self.files])

    def first_empty(self):
        for i,f in enumerate(self.files[self.last_empty_pos:], start=self.last_empty_pos):
            if f.ID == -1:
                self.last_empty_pos = self.files.index(f)
                return self.last_empty_pos

    def first_empty_nblock_from_leftmost(self, targ: int):
        for i,f in enumerate(self.files):
            if f.ID == -1 and f.length >= targ:
                return i
        return -1

    def append_file(self, file: File):
        self.files.append(file)

    def _move_block(self):
        last = self.files.pop()
        if last.is_empty():
            return

        first_empty_pos = self.first_empty()
        empty_file = self.files[first_empty_pos]
        # same length
        if empty_file.length == last.length:
            empty_file.ID = last.ID
        # empty is longer
        elif empty_file.length > last.length:
            self.files.insert(first_empty_pos, last)
            self.files[first_empty_pos+1].length -= last.length
        # last is longer
        else:
            empty_file.ID = last.ID
            self.append_file(File(ID=last.ID, length=last.length - empty_file.length))
            
    def _move_entire_block(self, f: File):
        suitable_index = self.first_empty_nblock_from_leftmost(f.length)
        if suitable_index == -1 or suitable_index > self.files.index(f):
            return
        new_location = self.files[suitable_index]
        old_length = new_location.length
        #print(f"suitable_index: {suitable_index}, new_location: {new_location}, old_length: {old_length}, f.length: {f.length}")
        self.files[suitable_index] = File(ID=f.ID, length=f.length, move_attempted=True)
        f.ID = -1
        if new_location.length > f.length:
            diff = old_length - f.length
            smaller_empty = File(ID=-1, length=diff, move_attempted=True)
            #print(diff, smaller_empty)
            self.files = self.files[:suitable_index+1] + [smaller_empty] + self.files[suitable_index+1:]
        #self.print()
        return

    def checksum(self) -> int:
        res = 0
        pos = 0
        for f in self.files:
            if f.ID == -1:
                pos += f.length
                continue
            for _ in range(f.length):
                res += pos * f.ID
                pos += 1
        return res

    def move_all_blocks(self) -> int:
        while self.has_empty():
            #self.print()
            self._move_block()
        return self.checksum()
    
    def move_entire_blocks(self) -> int:
        while self.has_unchecked_file():
            for i,file in enumerate(self.files[::-1]):
                if file.move_attempted:
                    continue
                if file.is_empty():
                    file.move_attempted = True
                    continue
                file.move_attempted = True
                self._move_entire_block(file)
        return self.checksum()
    
    def print(self):
        for f in self.files:
            if f.ID == -1:
                print("." * f.length, end="")
            else:
                print(f"{str(f.ID)*f.length}", end="")
        print()

def _parse_input(input_str) -> FileSystem:
    n = 0
    empty = False
    files = []
    for c in input_str:
        if empty:
            files.append(File(length=int(c)))
            empty = False
        else:
            files.append(File(ID=n, length=int(c)))
            n += 1
            empty = True
    return FileSystem(files)

def _load_test_input(t: str = TEST_INPUT) -> FileSystem:
    return _parse_input(t)

def _load_actual_input():
    with open(ACTUAL_INPUT_FILENAME, "r") as f:
        return _parse_input(f.read().strip())

def main()  -> None:
    # Part 1:
    #   a
    #   b
    #   c
    test = _load_test_input()
    #print(f"Test: {test.move_all_blocks()}")

    # should be 1928
    actual = _load_actual_input()
    #print(f"Actual: {actual.move_all_blocks()}")

    print(f"Test P2: {test.move_entire_blocks()}")
    # should be 2858

    print(f"Actual P2: {actual.move_entire_blocks()}")
    return

if __name__ == "__main__":
    main()

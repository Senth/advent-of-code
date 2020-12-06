from typing import List


class Toboggan:
    def __init__(self) -> None:
        self._map: List[str] = []

    def add_line(self, line: str) -> None:
        self._map.append(line)

    def length(self) -> int:
        return len(self._map)

    def is_tree(self, x: int, y: int) -> bool:
        line = self._map[y]
        wrapped_x = Toboggan._wrap_x_coord(line, x)
        return line[wrapped_x] == "#"

    def count_trees(self, x_step: int, y_step: int) -> int:
        tree_count = 0
        i = 0
        while True:
            x = i * x_step
            y = i * y_step

            if y >= self.length():
                break

            if self.is_tree(x, y):
                tree_count += 1

            i += 1
        return tree_count

    @staticmethod
    def _wrap_x_coord(line: str, x: int) -> int:
        wrapped = x % len(line)
        return wrapped


# Read toboggan
toboggan = Toboggan()
with open("03.in", "r") as file:
    for line in file.readlines():
        toboggan.add_line(line.replace("\n", ""))


# Part 1 - Calculate trees
tree_count = toboggan.count_trees(3, 1)
print(f"Part 1, tree count: {tree_count}")

# Part 2 - Multiply all tree counts
tree_count = toboggan.count_trees(1, 1)
tree_count *= toboggan.count_trees(3, 1)
tree_count *= toboggan.count_trees(5, 1)
tree_count *= toboggan.count_trees(7, 1)
tree_count *= toboggan.count_trees(1, 2)

print(f"Part 2, tree count: {tree_count}")
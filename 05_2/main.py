class Line:
    def __init__(self, inp):
        pts = inp.split(" -> ")
        self.p1 = tuple(map(int, pts[0].split(",")))
        self.p2 = tuple(map(int, pts[1].split(",")))

    def __repr__(self):
        return f"{self.p1[0]},{self.p1[1]} -> {self.p2[0]},{self.p2[1]}"

    @property
    def is_cardinal(self):
        return self.p1[0] == self.p2[0] or self.p1[1] == self.p2[1]

    @property
    def is_diagonal(self):
        return abs(self.p1[0] - self.p2[0]) == abs(self.p1[1] - self.p2[1])

    def draw_line(self, grid):
        x1, x2 = (self.p1[0], self.p2[0]) if self.p1[0] < self.p2[0] else (
            self.p2[0], self.p1[0])
        y1, y2 = (self.p1[1], self.p2[1]) if self.p1[0] < self.p2[0] else (
            self.p2[1], self.p1[1])
        dx = x2 - x1
        dy = y2 - y1

        if dx == 0:
            _y1, _y2 = (y1, y2) if y1 < y2 else (y2, y1)
            for y in range(_y1, _y2 + 1):
                grid[y][x1] += 1
            return grid

        for x in range(x1, x2 + 1):
            y = y1 + dy * (x - x1) // dx
            grid[y][x] += 1

        return grid


def solve(test_input):
    lines = list(map(Line, test_input))

    extremes = (
        max([p[0] for line in lines for p in [line.p1, line.p2]]) + 1,
        max([p[1] for line in lines for p in [line.p1, line.p2]]) + 1
    )

    grid = [[0 for x in range(extremes[0])] for y in range(extremes[1])]

    for line in lines:
        if not line.is_cardinal and not line.is_diagonal:
            continue
        grid = line.draw_line(grid)

    return sum(p >= 2 for row in grid for p in row)


example_input = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""".strip().split("\n")


def main():
    with open("05_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

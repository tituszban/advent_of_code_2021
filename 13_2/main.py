import re


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str(self))


class Fold:
    inst_re = re.compile(r"fold\salong\s([xy])=(\d+)")

    def __init__(self, inst):
        match = self.inst_re.match(inst)
        if not match:
            raise Exception(f"Couldn't match instruction: {inst}")
        self.axis = match.group(1)
        self.v = int(match.group(2))

    def __repr__(self):
        return f"Fold({self.axis}, {self.v})"

    def _fold_y(self, point):
        if point.y < self.v:
            return Point(point.x, point.y)
        if point.y == self.v:
            raise Exception("Point lies on fold")
        return Point(point.x, 2 * self.v - point.y)

    def _fold_x(self, point):
        if point.x < self.v:
            return Point(point.x, point.y)
        if point.x == self.v:
            raise Exception("Point lies on fold")
        return Point(2 * self.v - point.x, point.y)

    def apply_fold(self, point):
        return {
            "x": self._fold_x,
            "y": self._fold_y
        }[self.axis](point)


def visualise_points(points):
    x_max = max(map(lambda p: p.x, points))
    y_max = max(map(lambda p: p.y, points))

    for y in range(y_max + 1):
        row = ""
        for x in range(x_max + 1):
            if any(point.x == x and point.y == y for point in points):
                row += "#"
            else:
                row += "."
        print(row)


example_input = """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""".strip().split("\n")


def solve(test_input):
    sp = test_input.index("")
    points = list(map(
        lambda l: Point(*map(int, l.split(","))),
        test_input[:sp]))
    # visualise_points(points)

    folds = list(map(Fold, test_input[sp+1:]))

    for fold in folds:
        points = set([fold.apply_fold(point) for point in points])

    visualise_points(points)


def main():
    with open("13_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

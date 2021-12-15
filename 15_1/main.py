class SortedSet:
    def __init__(self, initial, set_key, sort_key):
        self.list = sorted(initial, key=sort_key)
        self.set_key = set_key
        self.sort_key = sort_key
        self.set = set(map(set_key, initial))

    @property
    def any(self):
        return any(self.list)

    def pop(self):
        v = self.list.pop(0)
        self.set.remove(self.set_key(v))
        return v

    def add(self, item):
        if (s := self.set_key(item)) in self.set:
            return
        
        self.set.add(s)

        i = 0
        while i < len(self.list) and self.sort_key(self.list[i]) < self.sort_key(item):
            i += 1
        
        self.list.insert(i, item)

def print_best_grid(grid, best_grid):
    for i, row in enumerate(grid):
        row_txt = "\t".join(str(best_grid[(i, j)]) if best_grid[(i, j)] != float("inf") else "." for j, _ in enumerate(row))
        print(row_txt)
    

def solve(test_input):
    grid = [list(map(int, row)) for row in test_input]

    best_grid = {(i, j): float('inf') for i, row in enumerate(grid)
                 for j, _ in enumerate(row)}

    start = (0, 0)
    end = (len(grid) - 1, len(grid[0]) - 1)

    frontier = SortedSet([(start, 0)], lambda s: s[0], lambda s: s[1])
    explored = set()

    while frontier.any:
        next_point, _ = frontier.pop()
        x, y = next_point

        neighbours = [
            (x + 1, y), (x - 1, y),
            (x, y + 1), (x, y - 1),
        ]

        if next_point == start:
            best_grid[next_point] = grid[x][y]
        else:
            best_grid[next_point] = min([
                best_grid.get(p, float('inf')) for p in
                neighbours
            ]) + grid[x][y]

        explored.add(next_point)

        for n in neighbours:
            if n in explored or n not in best_grid:
                continue
            frontier.add((n, best_grid[next_point] + grid[n[0]][n[1]]))

    print_best_grid(grid, best_grid)
    return best_grid[end] - grid[0][0]


example_input = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""".strip().split("\n")


def main():
    with open("15_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

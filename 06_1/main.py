from functools import reduce


class FishGroup:
    def __init__(self, days, count):
        self.days = days
        self.count = count

    def update(self):
        if self.days == 0:
            self.days = 6
            return FishGroup(8, self.count)
        self.days -= 1


def solve(test_input):
    fish = reduce(lambda d, i: {**d, i: d.get(i, 0) + 1},
                  map(int, test_input[0].split(",")),
                  {})

    fish_groups = [FishGroup(key, value) for key, value in fish.items()]

    for _ in range(80):
        new_groups = []
        for group in fish_groups:
            if (new_group := group.update()):
                new_groups.append(new_group)
        fish_groups.extend(new_groups)

    return sum(group.count for group in fish_groups)

example_input = "3,4,3,1,2".split("\n")

def main():
    with open("06_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

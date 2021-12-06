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

    @classmethod
    def merge(cls, fish):
        assert len(fish) > 0, "No fish"
        assert all(f.days == fish[0].days for f in fish), "Same day"

        return cls(fish[0].days, sum(f.count for f in fish))

    def __repr__(self):
        return f"FishGroup({self.days}, {self.count})"


def solve(test_input, n = 256):
    fish = reduce(lambda d, i: {**d, i: d.get(i, 0) + 1},
                  map(int, test_input[0].split(",")),
                  {})

    fish_groups = [FishGroup(key, value) for key, value in fish.items()]

    for _ in range(n):
        new_groups = []
        for group in fish_groups:
            if (new_group := group.update()):
                new_groups.append(new_group)
        fish_groups.extend(new_groups)

        group_by_days = reduce(
            lambda d, i: {**d, i.days: d.get(i.days, []) + [i]}, fish_groups, {})

        fish_groups = [FishGroup.merge(fishes)
                       for fishes in group_by_days.values()]

    return sum(group.count for group in fish_groups)


example_input = "3,4,3,1,2".split("\n")


def main():
    with open("06_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

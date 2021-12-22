from __future__ import annotations
import itertools
import re


class Range:
    def __init__(self, start, end):
        assert start <= end
        self.start = start
        self.end = end

    def is_overlapping(self, other: Range):
        return self.start <= other.end and self.end >= other.start

    def split_with_range(self, other: Range):
        if not self.is_overlapping(other):
            return [Range(self.start, self.end)], []

        if other.start <= self.start and other.end >= self.end:
            return [], [Range(self.start, self.end)]

        if other.start <= self.start and other.end < self.end:
            return [Range(other.end + 1, self.end)], [Range(self.start, other.end)]

        if other.start > self.start and other.end >= self.end:
            return [Range(self.start, other.start - 1)], [Range(other.start, self.end)]

        if self.start < other.start and self.end > other.end:
            return [Range(self.start, other.start - 1), Range(other.end + 1, self.end)], [Range(other.start, other.end)]

    def __eq__(self, other: Range):
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash((self.start, self.end))

    def __repr__(self):
        return f"{self.start}..{self.end}"

    @property
    def length(self):
        return self.end + 1 - self.start

    @classmethod
    def from_str(self, s):
        return Range(*map(int, s.split("..")))


class Cuboid:
    cuboid_re = re.compile(
        r"(?P<state>o(n|ff)) x=(?P<x>-?\d+\.\.-?\d+),y=(?P<y>-?\d+\.\.-?\d+),z=(?P<z>-?\d+\.\.-?\d+)")

    def __init__(self, state: bool, x_range: Range, y_range: Range, z_range: Range):
        self.state = state
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range

    def split_with_cuboid(self, other: Cuboid):
        if not (self.x_range.is_overlapping(other.x_range)
                and self.y_range.is_overlapping(other.y_range)
                and self.z_range.is_overlapping(other.z_range)):
            yield self
            return

        x_keeping, x_loosing = self.x_range.split_with_range(other.x_range)
        y_keeping, y_loosing = self.y_range.split_with_range(other.y_range)
        z_keeping, z_loosing = self.z_range.split_with_range(other.z_range)

        for x_range, y_range, z_range in itertools.product([*x_keeping, *x_loosing], [*y_keeping, *y_loosing], [*z_keeping, *z_loosing]):
            if x_range in x_loosing and y_range in y_loosing and z_range in z_loosing:
                continue

            yield Cuboid(self.state, x_range, y_range, z_range)

    @property
    def count(self):
        return self.x_range.length * self.y_range.length * self.z_range.length

    def __repr__(self):
        return f"Cuboid({'on' if self.state else 'off'}, x={self.x_range}, y={self.y_range}, z={self.z_range})"

    @classmethod
    def from_str(cls, s):
        match = cls.cuboid_re.match(s)
        assert match
        return cls(
            match.group("state") == "on",
            Range.from_str(match.group("x")),
            Range.from_str(match.group("y")),
            Range.from_str(match.group("z")),
        )


def solve(test_input):
    cuboids = []

    filter_range = Range(-50, 50)

    for line in test_input:
        cuboid = Cuboid.from_str(line)

        if not (filter_range.is_overlapping(cuboid.x_range)
                and filter_range.is_overlapping(cuboid.y_range)
                and filter_range.is_overlapping(cuboid.z_range)):
            continue

        new_list = []

        for c in cuboids:
            c_split = list(c.split_with_cuboid(cuboid))
            new_list.extend(c_split)

        new_list.append(cuboid)
        cuboids = new_list

    sum_on = sum([c.count for c in cuboids if c.state])

    return sum_on


example_input_0 = """
on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10
""".strip().split("\n")

example_input_1 = """
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682
""".strip().split("\n")


def main():
    with open("22_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

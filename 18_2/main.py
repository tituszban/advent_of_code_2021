from enum import Enum
import itertools


class ReturnType(Enum):
    regular = "regular"
    to_split = "to_split"
    to_exp_partial = "to_explode_partial"
    to_exp_full = "to_explode_full"
    null = "null"


class ChildSide(Enum):
    left = "left"
    right = "right"


class Number:
    def __init__(self):
        self._parent = None
        self._parent_side = None

    def set_parent(self, p, side):
        self._parent = p
        self._parent_side = side

    def replace(self, new):
        assert self._parent, "No parent"
        if self._parent_side == ChildSide.left:
            self._parent.left = new
            new.set_parent(self._parent, ChildSide.left)
        elif self._parent_side == ChildSide.right:
            self._parent.right = new
            new.set_parent(self._parent, ChildSide.right)
        else:
            raise Exception("No child side set")


class Pair(Number):
    def __init__(self, left, right):
        self.left = left
        left.set_parent(self, ChildSide.left)
        self.right = right
        right.set_parent(self, ChildSide.right)

    def __repr__(self):
        return f"[{self.left}, {self.right}]"

    def traverse(self):
        return self.left.traverse() + self.right.traverse()

    @property
    def pure_pair(self):
        return isinstance(self.left, Regular) and isinstance(self.right, Regular)

    @property
    def magnitude(self):
        return self.left.magnitude * 3 + self.right.magnitude * 2


class Regular(Number):
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return str(self.val)

    def traverse(self):
        return [self.val]

    @property
    def magnitude(self):
        return self.val


def parse(line):
    if line.isdigit():
        return Regular(int(line))

    assert line[0] == "[" and line[-1] == "]"

    def split_line(_s):
        brc_count = 0
        for i, s in enumerate(_s):
            if s == "[":
                brc_count += 1
            elif s == "]":
                brc_count -= 1
            elif brc_count == 0 and s == ",":
                return (_s[:i], _s[i + 1:])

    left, right = split_line(line[1:-1])

    return Pair(
        parse(left),
        parse(right),
    )


def reduce_number(number):

    def find_first_regular(_n):
        if isinstance(_n, Regular):
            return _n

        if (l := find_first_regular(_n.left)):
            return l

        if (r := find_first_regular(_n.right)):
            return r

        return None

    def find_number_to_split(_n):
        if isinstance(_n, Regular) and _n.val >= 10:
            return ReturnType.to_split, _n

        if isinstance(_n, Pair):
            if ((l := find_number_to_split(_n.left))[0] == ReturnType.to_split):
                return l

            if ((r := find_number_to_split(_n.right))[0] == ReturnType.to_split):
                return r

        return ReturnType.null, None

    def find_number_to_explode(_n, depth=0, last_regular=None):
        if isinstance(_n, Pair) and depth >= 4 and _n.pure_pair:
            return ReturnType.to_exp_partial, (last_regular, _n)

        if isinstance(_n, Regular):
            return ReturnType.regular, _n

        assert isinstance(_n, Pair)

        left_find = find_number_to_explode(
            _n.left, depth=depth + 1, last_regular=last_regular)
        if left_find[0] == ReturnType.regular:
            last_regular = left_find[1]
        if left_find[0] == ReturnType.to_split or left_find[0] == ReturnType.to_exp_full:
            return left_find
        if left_find[0] == ReturnType.to_exp_partial:
            first_right_regular = find_first_regular(_n.right)
            if first_right_regular:
                return ReturnType.to_exp_full, (*left_find[1], first_right_regular)
            return left_find

        return find_number_to_explode(_n.right, depth=depth + 1, last_regular=last_regular)

    result_type, val = find_number_to_explode(number)
    if result_type in (ReturnType.to_exp_full, ReturnType.to_exp_partial):
        if result_type == ReturnType.to_exp_full:
            left, split, right = val
        else:
            left, split = val
            right = None

        if left:
            left.replace(Regular(left.val + split.left.val))
        if right:
            right.replace(Regular(right.val + split.right.val))
        split.replace(Regular(0))

        return reduce_number(number)

    result_type, val = find_number_to_split(number)
    if result_type == ReturnType.to_split:
        val.replace(Pair(
            Regular(val.val // 2),
            Regular(val.val - (val.val // 2)),
        ))
        return reduce_number(number)

    return number


def add_numbers(n1, n2):
    number = Pair(n1, n2)
    res = reduce_number(number)
    return res

def get_magnitude(ls):
    l1, l2 = map(parse, ls)
    return add_numbers(l1, l2).magnitude

def solve(test_input):
    return max(map(get_magnitude, itertools.permutations(test_input, 2)))


example_input_1 = """
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""".strip().split("\n")


def main():
    with open("18_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

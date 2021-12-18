import re
import itertools


def sign(v):
    return 1 if v > 0 else (-1 if v < 0 else 0)


def get_min_v_x(x0):
    v_x = 0
    x = 0

    while v_x + x <= x0:
        x += v_x
        v_x += 1
    return v_x


def get_step_counts_x(v_x, x0, x1, max_c=250):
    x = 0
    c = 0
    while x < x1:
        x += v_x
        c += 1
        v_x -= sign(v_x)
        if x0 <= x <= x1:
            yield c
            if v_x == 0:
                yield from range(c + 1, max_c)
                break


def simulate_c_y_steps(v_y, c):
    y = 0
    for _ in range(c):
        y += v_y
        v_y -= 1
    return y


def get_v_ys(step_count, y0, y1):
    if step_count == 1:
        yield from range(y0, y1 + 1)

    v_y = y0
    while (y := simulate_c_y_steps(v_y, step_count)) <= y1:
        if y0 <= y <= y1:
            yield v_y
        v_y += 1


def solve(test_input):
    m = re.match(
        r"target\sarea:\sx=(?P<x0>-?\d+)\.\.(?P<x1>-?\d+),\sy=(?P<y0>-?\d+)\.\.(?P<y1>-?\d+)", test_input[0])
    assert m

    x0, x1, y0, y1 = map(lambda g: int(m.group(g)), ["x0", "x1", "y0", "y1"])

    min_v_x = get_min_v_x(x0)
    max_v_x = x1

    steps_by_vx = {
        v_x: s
        for v_x in range(min_v_x, max_v_x + 1)
        if any(s := list(get_step_counts_x(v_x, x0, x1)))}

    unique_steps = {}
    for v_x, steps in steps_by_vx.items():
        for step in steps:
            unique_steps[step] = [*unique_steps.get(step, []), v_x]

    valid_shots = set()

    for step, vxs in unique_steps.items():
        vys = list(get_v_ys(step, y0, y1))
        for s in itertools.product(vxs, vys):
            valid_shots.add(s)

    return len(valid_shots)


example_input = ["target area: x=20..30, y=-10..-5"]


def main():
    with open("17_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

import re
from enum import Enum


class ShotResult(Enum):
    on_target = "on_target"
    overshoot = "overshoot"
    undershoot = "undershoot"
    missed = "missed"


def sign(v):
    return 1 if v > 0 else (-1 if v < 0 else 0)


def simulate_shot(v_x, v_y, target_area):
    x0, x1, y0, y1 = target_area
    x = 0
    y = 0
    max_y = y
    while y > y1:
        x += v_x
        y += v_y
        max_y = max(y, max_y)
        v_x -= sign(v_x)
        v_y -= 1
        if x0 <= x <= x1 and y0 <= y <= y1:
            return ShotResult.on_target, max_y
    if x < x0:
        return ShotResult.undershoot, max_y
    if x > x1:
        return ShotResult.overshoot, max_y
    return ShotResult.missed, max_y


def sweep_y(x, target_area):
    y = 1
    best_max_y = 0
    while True:
        result, max_y = simulate_shot(x, y, target_area)
        if result == ShotResult.on_target:
            best_max_y = max(max_y, best_max_y)
        if result == ShotResult.overshoot:
            return best_max_y
        if y > 1000:
            return best_max_y
        y += 1
        


def solve(test_input):
    m = re.match(
        r"target\sarea:\sx=(?P<x0>-?\d+)\.\.(?P<x1>-?\d+),\sy=(?P<y0>-?\d+)\.\.(?P<y1>-?\d+)", test_input[0])
    assert m

    x0, x1, y0, y1 = map(lambda g: int(m.group(g)), ["x0", "x1", "y0", "y1"])

    return max(sweep_y(x, (x0, x1, y0, y1)) for x in range(1, x0))

example_input = ["target area: x=20..30, y=-10..-5"]

def main():
    with open("17_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

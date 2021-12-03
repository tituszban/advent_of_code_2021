from enum import Enum

class Axis(Enum):
    horizontal = "horizontal"
    vertical = "vertical"

def solve(test_input):
    directions = {
        "forward": (Axis.horizontal, 1),
        "down": (Axis.vertical, 1),
        "up": (Axis.vertical, -1)
    }

    position = {v:0 for v in Axis}

    for command in test_input:
        direction, distance = command.split()
        axis, multiplier = directions[direction]

        position[axis] = position[axis] + int(distance) * multiplier

    return position[Axis.horizontal] * position[Axis.vertical]


def main():
    with open("02_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))
    
    result = solve(test_input)
    print(result)

if __name__ == "__main__":
    main()
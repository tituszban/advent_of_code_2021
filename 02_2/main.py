from enum import Enum

class Axis(Enum):
    horizontal = "horizontal"
    vertical = "vertical"
    aim = "aim"

def solve(test_input):
    directions = {
        "forward": lambda v, x, y, a: (x + v, y + v * a, a),
        "down": lambda v, x, y, a: (x, y, a + v),
        "up": lambda v, x, y, a: (x, y, a - v)
    }

    x = 0
    y = 0
    a = 0

    for command in test_input:
        direction, distance = command.split()
        x, y, a = directions[direction](int(distance), x, y, a)

    return x * y


def main():
    with open("02_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))
    
    result = solve(test_input)
    print(result)

if __name__ == "__main__":
    main()
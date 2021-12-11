import numpy as np
from scipy.signal import convolve2d

kernel = np.array([
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
])


def update(m):
    m = m + 1
    count = 0
    while np.any(flasing := (m > 9)):
        count += np.sum(flasing)
        c = convolve2d(flasing, kernel, mode="same")
        
        m[flasing] = -1000
        m += c
    m[m < 0] = 0
    return m, count


def solve(test_input):
    m = np.array([list(map(int, line)) for line in test_input])
    print(m)
    count = 0
    for _ in range(100):
        m, c = update(m)
        print(m)
        count += c
    return count


example_input = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""".strip().split("\n")

def main():
    with open("11_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

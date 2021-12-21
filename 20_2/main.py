import numpy as np
import itertools
from scipy.signal import convolve2d

kernel = np.array([
    [1, 2, 4],
    [8, 16, 32],
    [64, 128, 256],
])


def apply_conv(mapping, matrix, padding):
    updated = convolve2d(matrix, kernel, fillvalue=padding)
    # new[x,y] = mapping[updated[x,y]]

    new = np.zeros(updated.shape, dtype=np.int32)

    for x in range(updated.shape[0]):
        for y in range(updated.shape[1]):
            new[x, y] = int(mapping[updated[x, y]])
    # print(matrix[0:10, 0:10])
    # print(updated[0:11, 0:11])
    # print(new[0:11, 0:11])
    # print(new)
    return new, mapping[0] if padding == 0 else mapping[-1]


def solve(test_input, n=50):
    mapping = list(map(lambda c: 1 if c == "#" else 0, test_input[0]))

    matrix = np.array([list(map(lambda c: 1 if c == "#" else 0, line))
                      for line in test_input[2:]])

    padding = 0
    for _ in range(n):
        matrix, padding = apply_conv(mapping, matrix, padding)

    return np.sum(matrix)


example_input = """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
""".strip().split("\n")


def main():
    with open("20_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

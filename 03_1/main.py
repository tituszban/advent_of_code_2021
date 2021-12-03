def solve(test_input):
    bit_count = [{"0": 0, "1": 0} for _ in range(len(test_input[0]))]

    for row in test_input:
        for i, c in enumerate(row):
            bit_count[i][c] += 1

    gamma = int(
        ''.join(["0" if d["0"] > d["1"] else "1" for d in bit_count]), 2)
    epsilon = int(
        ''.join(["0" if d["0"] < d["1"] else "1" for d in bit_count]), 2)

    return gamma * epsilon


def main():
    with open("03_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

def get_digit_frequency(test_input):
    bit_count = [{"0": 0, "1": 0} for _ in range(len(test_input[0]))]

    for row in test_input:
        for i, c in enumerate(row):
            bit_count[i][c] += 1

    return bit_count


def get_value(test_input, comparison):
    for i in range(len(test_input[0])):
        f = get_digit_frequency(test_input)

        selected_digit = comparison(f[i])

        test_input = [item for item in test_input if item[i] == selected_digit]

        if len(test_input) == 1:
            return int(test_input[0], 2)
        if len(test_input) == 0:
            raise Exception("??")
    raise Exception("?")


def solve(test_input):

    o = get_value(test_input, lambda f: "0" if f["0"] > f["1"] else "1")
    co = get_value(test_input, lambda f: "0" if f["0"] <= f["1"] else "1")

    return o * co


example_test_input = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
""".strip().split("\n")


def main():
    with open("03_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

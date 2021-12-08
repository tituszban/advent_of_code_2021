def solve(test_input):
    values = list(map(int, test_input[0].split(",")))
    sorted_values = sorted(values)

    guess = round(sum(values) / len(values))

    def fuel_needed(n):
        return sum(x for v in values for x in range(1, abs(n - v) + 1))

    f0 = fuel_needed(guess)
    direction = 0
    if fuel_needed(guess + 1) < f0:
        direction = 1
    elif fuel_needed(guess - 1) < f0:
        direction = -1
    else:
        return f0

    n = direction
    while (f1 := fuel_needed(guess + n)) < f0:
        f0 = f1
        n += direction
    return f0

example_input = "16,1,2,0,4,2,7,1,2,14".split("\n")

def main():
    with open("07_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))
    
    result = solve(test_input)
    print(result)

if __name__ == "__main__":
    main()
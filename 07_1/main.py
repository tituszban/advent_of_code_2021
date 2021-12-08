def solve(test_input):
    values = list(map(int, test_input[0].split(",")))
    sorted_values = sorted(values)

    guess = sorted_values[len(values) // 2]

    def fuel_needed(n):
        return sum(abs(n - v) for v in values)

    return fuel_needed(guess)

example_input = "16,1,2,0,4,2,7,1,2,14".split("\n")

def main():
    with open("07_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))
    
    result = solve(test_input)
    print(result)

if __name__ == "__main__":
    main()
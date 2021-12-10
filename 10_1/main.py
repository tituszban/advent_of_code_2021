from collections import deque

closing_brackets = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}

error_scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

def evaluate_syntax(line):
    bracket_stack = deque([])
    opening_brackets = set(closing_brackets.values())

    for c in line:
        if c in opening_brackets:
            bracket_stack.append(c)
        if c in closing_brackets:
            if bracket_stack[-1] == closing_brackets[c]:
                bracket_stack.pop()
            else:
                return error_scores[c]
    return 0
        

def solve(test_input):
    return sum(map(evaluate_syntax, test_input))

example_input = """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""".strip().split("\n")

def main():
    with open("10_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))
    
    result = solve(test_input)
    print(result)

if __name__ == "__main__":
    main()
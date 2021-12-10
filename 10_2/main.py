from collections import deque
from functools import reduce

closing_brackets = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}

closing_scores = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4
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
                return 0
    return reduce(lambda s, c: s * 5 + closing_scores[c], reversed(bracket_stack), 0)
        

def solve(test_input):
    scores = sorted(list(filter(lambda x: x != 0, map(evaluate_syntax, test_input))))
    return scores[len(scores) // 2]

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
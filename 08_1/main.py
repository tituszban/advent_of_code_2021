class Digit:
    def __init__(self, s):
        self.s = s

    def decode_length(self):
        if len(self.s) == 2:
            return 1
        if len(self.s) == 3:
            return 7
        if len(self.s) == 4:
            return 4
        if len(self.s) == 7:
            return 8
        return None


class DigitConfig:
    def __init__(self, seq):
        reference, output = seq.split(" | ")
        self.reference = list(map(Digit, reference.split()))
        self.output = list(map(Digit, output.split()))

    def count_known_digits_based_on_length(self):
        return sum([1 for digit in self.output if digit.decode_length() is not None])


def solve(test_input):
    configs = map(DigitConfig, test_input)
    return sum(config.count_known_digits_based_on_length() for config in configs)


example_input = """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""".strip().split("\n")


def main():
    with open("08_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

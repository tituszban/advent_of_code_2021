import itertools as it
from typing import Mapping


class Digit:
    def __init__(self, s):
        self.s = ''.join(sorted(s))

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

    def __len__(self):
        return len(self.s)

    def __repr__(self):
        return f"\"{self.s}\""

    def __hash__(self):
        return hash(self.s)

    def __eq__(self, other):
        return self.s == other.s

    def __lt__(self, other):
        return self.s < other.s


class ValidDigit(Digit):
    digit_to_value = {
        "abcdefg": 8,
        "abcefg": 0,
        "abdefg": 6,
        "abcdfg": 9,
        "acdeg": 2,
        "acdfg": 3,
        "abdfg": 5,
        "bcdf": 4,
        "acf": 7,
        "cf": 1,
    }
    value_to_digit = {
        value: digit for digit, value in digit_to_value.items()
    }

    def __init__(self, s):
        super().__init__(s)
        if self.s not in self.digit_to_value.keys():
            raise Exception(f"Invalid digit {self.s}")

    @classmethod
    def is_valid(cls, s):
        return ''.join(sorted(s)) in cls.digit_to_value.keys()

    def decode(self):
        return self.digit_to_value[self.s]


class DigitMapping:
    def __init__(self, mapping):
        self.mapping = mapping

    def _apply_mapping(self, scrambled_digit):
        return ''.join(self.mapping[c] for c in scrambled_digit.s)

    def apply_mapping(self, scrambled_digit):
        s = self._apply_mapping(scrambled_digit)
        if ValidDigit.is_valid(s):
            return ValidDigit(s)
        return None

    def __repr__(self):
        return str(self.mapping)


class DigitConfig:

    def __init__(self, seq):
        self.original_seq = seq
        reference, output = seq.split(" | ")
        self.reference = list(map(Digit, reference.split()))
        self.output = list(map(Digit, output.split()))

    def __repr__(self):
        return self.original_seq

    def decode(self):
        print(f"Decoding {self}")
        chars = "abcdefg"
        for m in it.permutations(chars, 7):
            mapping = DigitMapping({o: g for o, g in zip(m, chars)})

            mapped = [mapping.apply_mapping(d)
                      for d in [*self.reference, *self.output]]
            is_consistent = all(m for m in mapped)
            if not is_consistent:
                continue

            mapped_output = [
                mapping.apply_mapping(o).decode()
                for o in self.output
            ]
            return int(''.join(map(str, mapped_output)))

        raise Exception("No mapping found")

    def count_known_digits_based_on_length(self):
        return sum([1 for digit in self.output if digit.decode_length() is not None])


def solve(test_input):
    configs = map(DigitConfig, test_input)
    return sum(config.decode() for config in configs)


example_input = """
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""".strip().split("\n")

example_input_0 = """
acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
""".strip().split("\n")


def main():
    with open("08_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

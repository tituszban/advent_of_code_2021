import itertools as it


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


class DigitConfig:
    digit_configs = {
        8: "abcdefg",
        0: "abcefg",
        6: "abdefg",
        9: "abcdfg",
        2: "acdeg",
        3: "abdfg",
        5: "abdfg",
        4: "bcdf",
        7: "acf",
        1: "cf",
    }
    digit_configs_by_len = {
        7: [8],
        6: [0, 6, 9],
        5: [2, 3, 5],
        4: [4],
        3: [7],
        2: [1]
    }

    def __init__(self, seq):
        reference, output = seq.split(" | ")
        self.reference = list(map(Digit, reference.split()))
        self.output = list(map(Digit, output.split()))

    def decode2(self):
        def apply_mapping(digit, mapping):
            return frozenset(mapping[s] for s in digit.s)

        correct_mapping = {"d": "a", "e": "b", "a": "c", "f": "d", "g": "e", "b": "f", "c": "g"}

        digits = set(frozenset(v) for v in self.digit_configs.values())
        chars = "abcdefg"
        for m in it.permutations(chars, 7):
            mapping = {o: g for o, g in zip(m, chars)}
            mapped = [apply_mapping(d, mapping) for d in [*self.reference, *self.output]]
            is_consistent = all(m in digits for m in mapped)
            if is_consistent:
                print(mapping)
        return 0

    def decode(self):
        digits_by_len = {i: set([]) for i in range(2, 8)}
        for digit in [*self.reference, *self.output]:
            digits_by_len[len(digit)].add(digit)

        digits_with_possible_digits = {}

        for l, digits in digits_by_len.items():
            possible_digits = self.digit_configs_by_len[l]
            for digit in digits:
                digits_with_possible_digits[digit] = possible_digits

        def get_all_configs(_dwpd):
            keys = list(_dwpd.keys())
            key = keys.pop(0)
            for p in _dwpd[key]:
                if not any(keys):
                    yield {key: p}
                else:
                    for c in get_all_configs({k: _dwpd[k] for k in keys}):
                        yield {key: p, **c}

        possible_configurations = list(
            get_all_configs(digits_with_possible_digits))

        def is_mapping_valid(mapping, digit, config):
            c = self.digit_configs[config]

            return all(mapping[x] in c for x in digit.s if x in mapping)

        def is_consistent(config, mappings={}):
            digits = list(config.keys())
            digit = digits.pop(0)

            if not is_mapping_valid(mappings, digit, config[digit]):
                return

            unmapped_digits = [d for d in digit.s if d not in mappings]

            for p in it.permutations(unmapped_digits):
                mapping = {o: g for o, g in zip(
                    p, self.digit_configs[config[digit]])}
                if not any(digits):
                    yield {**mappings, **mapping}
                else:
                    c = list(is_consistent(
                        {d: config[d] for d in digits}, mappings={**mappings, **mapping}))

                    if not any(c):
                        continue
                    yield from c

        for possible_config in possible_configurations:
            c = list(is_consistent(possible_config))
            if any(c):
                print(c)
        print(digits_by_len)

        """
        8: 7; abcdefg
        0: 6; abc efg
        6: 6; ab defg
        9: 6; abcd fg
        2: 5; a cde g
        3: 5; a bd fg
        5: 5; ab d fg
        4: 4;  bcd f 
        7: 3; a c  f 
        1: 2;   c  f 
        """

    def count_known_digits_based_on_length(self):
        return sum([1 for digit in self.output if digit.decode_length() is not None])


def solve(test_input):
    configs = map(DigitConfig, test_input)
    return sum(config.decode2() for config in configs)


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

    result = solve(example_input_0)
    print(result)


if __name__ == "__main__":
    main()

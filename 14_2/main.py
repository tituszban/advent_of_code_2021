from collections import defaultdict


def count_letters(pair_counts, last_letter):
    freq = defaultdict(int)

    for letters, c in pair_counts.items():
        freq[letters[0]] += c

    freq[last_letter] += 1
    return sorted(freq.values())


def solve(test_input, n=40):
    chain = test_input[0]

    mappings = {pair: (pair[0] + insert, insert + pair[1])
                for pair, insert in map(lambda s: s.split(" -> "), test_input[2:])}

    pairs = list(zip(chain, chain[1:]))

    pair_count = defaultdict(int)

    for pair in pairs:
        pair_count[''.join(pair)] += 1

    for i in range(n):
        print(i, sum(count_letters(pair_count, chain[-1])))
        start_pair = dict(pair_count)
        new_pairs = defaultdict(int)

        for pair, count in start_pair.items():
            if pair not in mappings:
                new_pairs[pair] += count
                continue

            for m in mappings[pair]:
                new_pairs[m] += count
        pair_count = new_pairs

    print(sum(count_letters(pair_count, chain[-1])))

    freq = count_letters(pair_count, chain[-1])
    return freq[-1] - freq[0]


example_input = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
""".strip().split("\n")


def main():
    with open("14_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

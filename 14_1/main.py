class Node:
    def __init__(self, letter, nxt):
        self.letter = letter
        self.nxt = nxt
    
    def extend(self, mapping):
        if self.nxt is None:
            return None
        pair = self.letter + self.nxt.letter
        if pair not in mapping:
            return self.nxt
        
        o_nxt = self.nxt
        new_nxt_letter = mapping[pair]
        self.nxt = Node(new_nxt_letter, o_nxt)
        return o_nxt

def extend(node, mapping):
    while node:
        node = node.extend(mapping)

def count_chain(node):
    i = 0
    while node:
        i += 1
        node = node.nxt
    return i

def find_frequency(node):
    d = {}
    while node:
        d[node.letter] = d.get(node.letter, 0) + 1
        node = node.nxt
    return d


def solve(test_input):
    chain = test_input[0]
    node = None
    for c in reversed(chain):
        node = Node(c, node)

    mappings = {pair: insert for pair, insert in map(lambda s: s.split(" -> "), test_input[2:])}

    for i in range(10):
        print(i, count_chain(node))
        extend(node, mappings)

    print(count_chain(node))

    f = sorted(find_frequency(node).values())
    return f[-1] - f[0]


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
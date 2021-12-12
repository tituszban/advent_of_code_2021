from collections import defaultdict

def solve(test_input):
    def is_end(node):
        return node == "end"
    
    def is_small(node):
        return node.islower()

    def is_start(node):
        return node == "start"

    nodes = defaultdict(list)

    for f, t in map(lambda s: s.split("-"), test_input):
        nodes[f].append(t)
        nodes[t].append(f)
    
    to_expore = [["start"]]

    paths = []

    while any(to_expore):
        path = to_expore.pop(0)
        end = path[-1]

        if is_end(end):
            paths.append(path)
            continue

        for neighbour in nodes[end]:
            if is_small(neighbour) and neighbour in path:
                continue
            to_expore.append([*path, neighbour])
    
    return len(paths)

example_input1 = """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""".strip().split("\n")

example_input2 = """
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
""".strip().split("\n")

example_input3 = """
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
""".strip().split("\n")

def main():
    with open("12_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))
    
    result = solve(test_input)
    print(result)

if __name__ == "__main__":
    main()
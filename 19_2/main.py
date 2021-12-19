import re

def manhattan_distance(a, b):
    return sum(abs(a[i] - b[i]) for i in range(3))

def solve(test_input):
    scanner_re = re.compile(r"OrientedScanner\(Scanner\(\d+\), \((-?\d+), (-?\d+), (-?\d+)\), \d+\)")

    points = []

    for line in test_input:
        match = scanner_re.match(line)
        assert match
        points.append(tuple(map(int, [match.group(1), match.group(2), match.group(3)])))
    
    max_dist = 0
    for p1 in points:
        for p2 in points:
            max_dist = max(max_dist, manhattan_distance(p1, p2))
    return max_dist

def main():
    with open("19_2/scanners.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))
    
    result = solve(test_input)
    print(result)

if __name__ == "__main__":
    main()
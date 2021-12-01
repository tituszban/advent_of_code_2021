def count_increasing(measurements):
    p = None
    c = 0
    for v in measurements:
        if p is None:
            p = v
            continue
        if v > p:
            c += 1
        p = v
    return c

def main():
    with open("01_1/input.txt") as f:
        lines = list(map(lambda l: int(l.strip()), f.readlines()))

    measurements = list(map(lambda z: sum(z), zip(lines[:-2], lines[1:-1], lines[2:])))
    print(count_increasing(measurements))
    


if __name__ == "__main__":
    main()
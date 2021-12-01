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
    print(count_increasing(lines))
    


if __name__ == "__main__":
    main()
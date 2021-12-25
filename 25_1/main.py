def update_state(state):
    w = len(state[0])
    h = len(state)

    can_move = set()

    state_copy = list(map(list, state))

    for y, row in enumerate(state):
        for x, p in enumerate(row):
            if state_copy[y][x] == ">" and state_copy[y][(xn := ((x + 1) % w))] == ".":
                can_move.add(((x, y), (xn, y), ">"))

    for (x, y), (xn, yn), sym in can_move:
        state_copy[y][x] = "."
        state_copy[yn][xn] = sym

    can_move = set()

    for y, row in enumerate(state_copy):
        for x, p in enumerate(row):
            if state_copy[y][x] == "v" and state_copy[(yn := ((y + 1) % h))][x] == ".":
                can_move.add(((x, y), (x, yn), "v"))

    for (x, y), (xn, yn), sym in can_move:
        state_copy[y][x] = "."
        state_copy[yn][xn] = sym

    return state_copy

def print_state(state, i):
    print(f"Step {i}")
    print("\n".join(map(lambda l: ''.join(l), state)))
    

def solve(test_input):
    state = list(map(list, test_input))
    print_state(state, 0)
    prev = None
    i = 0
    while state != prev:
        i += 1
        prev = state
        state = update_state(state)
        # if i % 10 == 0:
        #     print_state(state, i)

    return i


example_input_1 = """
..........
.>v....v..
.......>..
..........
""".strip().split("\n")

example_input_2 = """
...>...
.......
......>
v.....>
......>
.......
..vvv..
""".strip().split("\n")

example_input_3 = """
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
""".strip().split("\n")


def main():
    with open("25_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

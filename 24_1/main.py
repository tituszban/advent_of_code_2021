import time


class InputProvider:
    def __init__(self, inputs):
        self.inputs = inputs
        self.i = 0

    def read(self):
        assert self.i < len(self.inputs)
        v = self.inputs[self.i]
        self.i += 1
        return v


class ALU:
    def __init__(self, input_provider: InputProvider):
        self.memory = {
            "w": 0,
            "x": 0,
            "y": 0,
            "z": 0
        }

        self.input_provider = input_provider

        self._inst_map = {
            "inp": self._inp,
            "add": self._add,
            "mul": self._mul,
            "div": self._div,
            "mod": self._mod,
            "eql": self._eql
        }

    def _inp(self, a):
        i = self.input_provider.read()
        self.memory[a] = i

    def _add(self, a, b):
        b_val = self.memory[b] if b in self.memory else int(b)
        self.memory[a] = self.memory[a] + b_val

    def _mul(self, a, b):
        b_val = self.memory[b] if b in self.memory else int(b)
        self.memory[a] = self.memory[a] * b_val

    def _div(self, a, b):
        b_val = self.memory[b] if b in self.memory else int(b)
        assert b_val != 0
        self.memory[a] = self.memory[a] // b_val

    def _mod(self, a, b):
        b_val = self.memory[b] if b in self.memory else int(b)
        assert not (self.memory[a] < 0 or b_val <= 0)
        self.memory[a] = self.memory[a] % b_val

    def _eql(self, a, b):
        b_val = self.memory[b] if b in self.memory else int(b)
        self.memory[a] = int(self.memory[a] == b_val)

    def execute_instructions(self, instructions):
        for instruction in instructions:
            inst, *args = instruction.split()
            self._inst_map[inst](*args)


def run_alu(model_num, instructions):
    alu = ALU(
        InputProvider(
            model_num
        )
    )

    alu.execute_instructions(instructions)

    return alu.memory["z"]


class ModalBlock:
    def __init__(self, n, m, d):
        self.n = n
        self.m = m
        self.d = d

    def __repr__(self):
        return f"MB({self.n}, {self.m}, {self.d})"

    def calc_z(self, w, z):
        x0 = z % 26 + self.n
        z1 = z // self.d

        x1 = int(x0 != w)

        y1 = 25 * x1 + 1
        z2 = z1 * y1

        y2 = w + self.m
        y3 = y2 * x1
        return z2 + y3

    def find_value(self, val: int, with_check: bool = False):
        if self.d == 26 and self.n < 0:
            # if 0 < (val - self.m) % 26 < 10:
            #     w = (val - self.m) % 26
            #     for i in range(26):
            #         z = (val - self.m) // 26 * 26 + i
            #         if w - z == self.n:
            #             continue
            #         if with_check:
            #             assert self.calc_z(w, z) == val
            #         yield (w, z)

            for w in range(1, 10):
                z = val * 26 - self.n + w
                if with_check:
                    assert self.calc_z(w, z) == val
                yield (w, z)

        elif self.d == 1 and self.n >= 10:
            z = val // 26
            w = val % 26 - self.m
            if 0 < w < 10:
                if with_check:
                    assert self.calc_z(w, z) == val
                yield (w, z)
        else:
            raise Exception("Unhandled case")

    @classmethod
    def from_inst_set(cls, inst):
        d = int(inst[4].split()[-1])
        n = int(inst[5].split()[-1])
        m = int(inst[15].split()[-1])

        return cls(n, m, d)


def find_values(blocks: list[ModalBlock], val: int):
    block = blocks[-1]

    values = list(block.find_value(val))

    res = {}

    for w, z in values:
        if len(blocks) > 1:
            r = find_values(blocks[:-1], z)
            if any(r):
                res[w] = r
        elif z == 0:
            res[w] = z

    return res


def get_nums(_res):
    for k, v in _res.items():
        if v == 0:
            yield k
        else:
            for n in get_nums(v):
                yield 10 * n + k

def test_model_num_blocks(blocks, num):
    model_num = list(map(int, str(num)))
    z = 0
    for w, block in zip(model_num, blocks):
        z = block.calc_z(w, z)

    return z

def test_model_num_alu(inst, num):
    model_num = list(map(int, str(num)))
    return run_alu(model_num, inst)


def solve(test_input):
    blocks = [ModalBlock.from_inst_set(
        test_input[i * 18: (i + 1) * 18]) for i in range(14)]

    res = find_values(blocks, 0)

    nums = list(get_nums(res))

    return max(nums)

example_input_1 = """
inp x
mul x -1
""".strip().split("\n")

example_input_2 = """
inp z
inp x
mul z 3
eql z x
""".strip().split("\n")

example_input_3 = """
inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2
""".strip().split("\n")


def main():
    with open("24_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

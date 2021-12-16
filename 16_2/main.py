from functools import reduce
from operator import mul


class Packet:
    def __init__(self, bits, expected_type=None):
        self._bits = bits
        self.version = int(bits[0:3], 2)
        self.type_id = int(bits[3:6], 2)
        if expected_type is not None:
            assert self.type_id == expected_type

    def __repr__(self):
        return f"Packet({self.version}, {self.type_id})"

    def version_sum(self):
        return self.version

    def eval(self):
        raise NotImplementedError()


class LiteralPacket(Packet):
    def __init__(self, bits):
        super().__init__(bits, 4)
        self.value, l = self._decode_bits(bits[6:])
        self.length = l + 6

    def _decode_bits(self, bits):
        bit_groups = ""
        i = 0
        while True:
            group = bits[i * 5: (i + 1) * 5]
            bit_groups += group[1:]
            i += 1
            if group[0] == "0":
                break
        return int(bit_groups, 2), i * 5

    def eval(self):
        return self.value

    def __repr__(self):
        return f"LiteralPacket({self.version}, {self.value})"

    def __str__(self):
        return str(self.value)


class OperatorPacket(Packet):
    def __init__(self, bits):
        super().__init__(bits)
        self.length_type_id = bits[6] == "1"
        self._length_bits = bits[7:(18 if self.length_type_id else 22)]
        self.sub_length = int(self._length_bits, 2)

        self.sub_packets = parse(bits[18:], self.sub_length) if self.length_type_id else parse(
            bits[22:22 + self.sub_length])
        self.length = sum(packet.length for packet in self.sub_packets) + \
            (18 if self.length_type_id else 22)

    def version_sum(self):
        return super().version_sum() + sum(packet.version_sum() for packet in self.sub_packets)

    def eval(self):
        sub_evals = [packet.eval() for packet in self.sub_packets]
        if self.type_id == 0:
            return sum(sub_evals)
        if self.type_id == 1:
            return reduce(mul, sub_evals)
        if self.type_id == 2:
            return min(sub_evals)
        if self.type_id == 3:
            return max(sub_evals)
        if self.type_id == 5:
            assert len(sub_evals) == 2
            return 1 if sub_evals[0] > sub_evals[1] else 0
        if self.type_id == 6:
            assert len(sub_evals) == 2
            return 1 if sub_evals[0] < sub_evals[1] else 0
        if self.type_id == 7:
            assert len(sub_evals) == 2
            return 1 if sub_evals[0] == sub_evals[1] else 0

    def __repr__(self):
        op = {
            0: "+", 1: "-", 2: "min", 3: "max", 5: ">", 6: "<", 7: "="
        }
        return f"OperatorPacket({self.version}, {op[self.type_id]}, {self.sub_packets})"

    def __str__(self):
        sub_strs = [str(packet) for packet in self.sub_packets]
        if self.type_id == 0:
            return f"({' + '.join(sub_strs)})"
        if self.type_id == 1:
            return f"({' * '.join(sub_strs)})"
        if self.type_id == 2:
            return f"min({', '.join(sub_strs)})"
        if self.type_id == 3:
            return f"max({', '.join(sub_strs)})"
        if self.type_id == 5:
            assert len(sub_strs) == 2
            return f"{sub_strs[0]} > {sub_strs[1]}"
        if self.type_id == 6:
            assert len(sub_strs) == 2
            return f"{sub_strs[0]} < {sub_strs[1]}"
        if self.type_id == 7:
            assert len(sub_strs) == 2
            return f"{sub_strs[0]} == {sub_strs[1]}"


def parse(bits, stop_after_packets=None):
    packets = []

    if all(bit == "0" for bit in bits):
        return packets

    raw_packet = Packet(bits)
    if raw_packet.type_id == 4:
        packet = LiteralPacket(bits)
    else:
        packet = OperatorPacket(bits)

    packets.append(packet)

    if packet.length + 6 < len(bits) and (stop_after_packets is None or stop_after_packets > 1):
        packets.extend(parse(
            bits[packet.length:], None if stop_after_packets is None else stop_after_packets - 1))

    return packets


def solve(test_input):
    s = test_input[0]
    bits = bin(int(s, 16))[2:].zfill(len(s) * 4)

    packet = parse(bits, 1)[0]

    print(packet)

    return packet.eval()


example_input_1 = ["C200B40A82"]    # 3
example_input_2 = ["04005AC33890"]  # 54
example_input_3 = ["880086C3E88112"]    # 7
example_input_4 = ["CE00C43D881120"]    # 9
example_input_5 = ["D8005AC2A8F0"]    # 1
example_input_6 = ["F600BC2D8F"]    # 0
example_input_7 = ["9C005AC2F8F0"]    # 0
example_input_8 = ["9C0141080250320F1802104A08"]    # 1


def main():
    with open("16_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

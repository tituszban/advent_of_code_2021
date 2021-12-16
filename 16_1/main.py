class Packet:
    def __init__(self, bits, expected_type=None):
        self._bits = bits
        self.version = int(bits[0:3], 2)
        self.type_id = int(bits[3:6], 2)
        if expected_type is not None:
            assert self.type_id == expected_type

    def version_sum(self):
        return self.version


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


class OperatorPacket(Packet):
    def __init__(self, bits):
        super().__init__(bits)
        self.length_type_id = bits[6] == "1"
        self._length_bits = bits[7:(18 if self.length_type_id else 22)]
        self.length = int(self._length_bits, 2)

        self.sub_packets = parse(bits[18:], self.length) if self.length_type_id else parse(
            bits[22:22 + self.length])
        self.length = sum(packet.length for packet in self.sub_packets) + \
            (18 if self.length_type_id else 22)

    def version_sum(self):
        return super().version_sum() + sum(packet.version_sum() for packet in self.sub_packets)


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

    if packet.length + 6 < len(bits) and (stop_after_packets is None or stop_after_packets > 0):
        packets.extend(parse(bits[packet.length:], None if stop_after_packets is None else stop_after_packets - 1))

    return packets


def solve(test_input):
    s = test_input[0]
    bits = bin(int(s, 16))[2:].zfill(len(s) * 4)

    packet = parse(bits, 1)[0]

    return packet.version_sum()


example_input_1 = ["D2FE28"]
example_input_2 = ["38006F45291200"]
example_input_3 = ["EE00D40C823060"]
example_input_4 = ["8A004A801A8002F478"]    # Version sum: 16
example_input_5 = ["620080001611562C8802118E34"]    # Version sum: 12
example_input_6 = ["C0015000016115A2E0802F182340"]    # Version sum: 23
example_input_7 = ["A0016C880162017C3686B18A3D4780"]    # Version sum: 31

def main():
    with open("16_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

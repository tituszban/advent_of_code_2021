import numpy as np
import re
from functools import reduce


class AngleCache:
    def __init__(self):
        self.a_cache = {}
        self.b_cache = {}
        self.c_cache = {}

    def get_rot_matrix(self, a, b, c):
        if a not in self.a_cache:
            cos_a = np.cos(np.deg2rad(a))
            sin_a = np.sin(np.deg2rad(a))
            self.a_cache[a] = np.array([
                [cos_a, -sin_a, 0],
                [sin_a, cos_a, 0],
                [0, 0, 1]
            ])

        if b not in self.b_cache:
            cos_b = np.cos(np.deg2rad(b))
            sin_b = np.sin(np.deg2rad(b))
            self.b_cache[b] = np.array([
                [cos_b, 0, sin_b],
                [0, 1, 0],
                [-sin_b, 0, cos_b]
            ])

        if c not in self.c_cache:
            cos_c = np.cos(np.deg2rad(c))
            sin_c = np.sin(np.deg2rad(c))
            self.c_cache[c] = np.array([
                [1, 0, 0],
                [0, cos_c, -sin_c],
                [0, sin_c, cos_c]
            ])

        return np.matmul(np.matmul(self.a_cache[a], self.b_cache[b]), self.c_cache[c])


angle_cache = AngleCache()


def generate_rotations(p):
    angles = [
        (0, 0,   0), (0, 0,   90), (0, 0,   180), (0, 0,   270),
        (0, 90,  0), (0, 90,  90), (0, 90,  180), (0, 90,  270),
        (0, 180, 0), (0, 180, 90), (0, 180, 180), (0, 180, 270),
        (0, 270, 0), (0, 270, 90), (0, 270, 180), (0, 270, 270),
        (90, 0, 0), (90, 0, 90), (90, 0, 180), (90, 0, 270),
        (90, 180, 0), (90, 180, 90), (90, 180, 180), (90, 180, 270),
    ]

    for a, b, c in angles:
        # print(np.deg2rad(a), np.deg2rad(b), np.deg2rad(c))
        rot_matrix = angle_cache.get_rot_matrix(a, b, c)

        yield tuple(map(int, np.round(np.matmul(rot_matrix, p), 0)))


class Scanner:
    id_re = re.compile(r"--- scanner (\d+) ---")

    def __init__(self, text):
        self.text = text
        match = self.id_re.match(text[0])
        assert match
        self.id = int(match.group(1))

        coords = [np.array(list(map(int, line.split(","))))
                  for line in text[1:]]

        self.rotations = list(zip(*map(generate_rotations, coords)))

    @property
    def rotation_set(self):
        return set(
            self.rotations
        )

    def __repr__(self):
        return f"Scanner({self.id})"

    def __eq__(self, other):
        return self.id == other.id and self.rotation_set == other.rotation_set

    def get_relative_vectors(self, orientation):
        coords = list(map(np.array, self.rotations[orientation]))

        for point in coords:
            rel_vectors = set()
            for p in coords:
                rel_vectors.add(tuple(point - p))
            yield tuple(point), rel_vectors


class OrientedScanner:
    def __init__(self, scanner, location, orientation):
        self.scanner = scanner
        self.location = location
        self.orientation = orientation

    def match_scanner(self, scanner, min_match=12):   # Return OrientedScanner from scanner or None
        for ref_point, ref_rel_vectors in self.scanner.get_relative_vectors(self.orientation):
            for orientation in range(24):
                for point, rel_vectors in scanner.get_relative_vectors(orientation):
                    if len(ref_rel_vectors.intersection(rel_vectors)) >= min_match:
                        loc = tuple(np.array(ref_point) - np.array(point) + np.array(self.location))
                        return OrientedScanner(scanner, loc, orientation)
                        # print(ref_point, point, orientation)

    def __repr__(self):
        return f"OrientedScanner({self.scanner}, {self.location}, {self.orientation})"

    @property
    def points(self):
        return set(
            map(lambda p: tuple(np.array(p) + np.array(self.location)), self.scanner.rotations[self.orientation])
        )



def parse(scanners):
    i = 0
    while "" in scanners[i:]:
        j = scanners[i:].index("")
        yield Scanner(scanners[i:i + j])
        i += j + 1
    yield Scanner(scanners[i:])


expected_matches = """
1: 68,-1246,-43
4: -20,-1133,1061
2: 1105,-1205,1229
3: -92,-2380,-20
"""

def solve(test_input):
    scanners = list(parse(test_input))

    root = OrientedScanner(scanners[0], (0, 0, 0), 0)
    oriented_scanners = [root]
    new_scanners = [root]

    remaining_scanners = list(scanners[1:])

    while any(remaining_scanners):
        to_remove = []
        to_add = []
        for scanner in remaining_scanners:
            for oriented_scanner in new_scanners:
                scanner_match = oriented_scanner.match_scanner(scanner)
                if scanner_match:
                    to_remove.append(scanner)
                    to_add.append(scanner_match)
                    break
        
        for r in to_remove:
            remaining_scanners.remove(r)
        
        for a in to_add:
            oriented_scanners.append(a)
        new_scanners = to_add

    all_points = reduce(lambda u, s: u.union(s.points), oriented_scanners, set())

    # Dump scanners for part 2, so no need for the SLOW calculation above again
    with open("scanners.txt", "w") as f:
        for scanner in oriented_scanners:
            f.write(f"{scanner}\n")

    return len(all_points)


example_input_1 = """
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
""".strip().split("\n")


def main():
    with open("19_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

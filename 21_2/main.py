import re
from collections import defaultdict


class DiracDice:
    def roll_n(self, n):
        assert n == 3, "Ugly hack allowing to pre-bake results"
        return {
            3: 1,
            4: 3,
            5: 6,
            6: 7,
            7: 6,
            8: 3,
            9: 1
        }


dice = DiracDice()


class Universe:
    def __init__(self, p1_pos, p2_pos, p1_score, p2_score, next_player):
        self.p1_pos = p1_pos
        self.p1_score = p1_score
        self.p2_pos = p2_pos
        self.p2_score = p2_score
        self.next_player = next_player

    def __hash__(self):
        return hash((self.p1_pos, self.p1_score, self.p2_pos, self.p2_score, self.next_player))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return f"Universe({self.p1_pos, self.p2_pos, self.p1_score, self.p2_score, self.next_player})"

    def _step(self, n):
        p1_pos = (self.p1_pos + (n if self.next_player == 0 else 0)) % 10
        p2_pos = (self.p2_pos + (n if self.next_player == 1 else 0)) % 10
        p1_score = (self.p1_score + (p1_pos + 1 if self.next_player == 0 else 0))
        p2_score = (self.p2_score + (p2_pos + 1 if self.next_player == 1 else 0))
        return Universe(
            p1_pos,
            p2_pos,
            p1_score,
            p2_score,
            (self.next_player + 1) % 2
        )

    @property
    def winner(self):
        if self.p1_score >= 21:
            return 1
        if self.p2_score >= 21:
            return 2
        return None

    def step(self):
        outcomes = defaultdict(int)

        for step, count in dice.roll_n(3).items():
            outcomes[self._step(step)] += count
        return dict(outcomes)


def solve(test_input):
    starting_re = re.compile(r"Player (\d) starting position: (\d+)")

    player_pos = {}
    for line in test_input:
        match = starting_re.match(line)
        assert match
        player_pos[int(match.group(1))] = int(match.group(2)) - 1

    universes = {Universe(player_pos[1], player_pos[2], 0, 0, 0): 1}
    completed_universes = {1: 0, 2: 0}

    while any(universes):
        new_universes = defaultdict(int)
        for u, c in universes.items():
            outcomes = u.step()
            for outcome, outcome_count in outcomes.items():
                if outcome.winner:
                    completed_universes[outcome.winner] += outcome_count * c
                else:
                    new_universes[outcome] += outcome_count * c

        universes = dict(new_universes)

    return max(completed_universes.values())


example_input = """
Player 1 starting position: 4
Player 2 starting position: 8
""".strip().split("\n")


def main():
    with open("21_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))

    result = solve(test_input)
    print(result)


if __name__ == "__main__":
    main()

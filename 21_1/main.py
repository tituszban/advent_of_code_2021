import re

class DeterministicDice:
    def __init__(self):
        self.val = 0
        self.roll_count = 0

    def roll(self):
        v = self.val + 1
        self.val = (self.val + 1) % 100
        self.roll_count += 1
        return v

    def roll_n(self, n):
        return (
            self.roll()
            for _ in range(n)
        )


def solve(test_input):
    starting_re = re.compile(r"Player (\d) starting position: (\d+)")

    player_pos = {}
    for line in test_input:
        match = starting_re.match(line)
        assert match
        player_pos[int(match.group(1))] = int(match.group(2)) - 1
    
    players = [1, 2]
    
    player_score = {p: 0 for p in players}

    player_index = 0

    dice = DeterministicDice()
    
    while all(score < 1000 for score in player_score.values()):
        player = players[player_index]
        player_pos[player] = (player_pos[player] + sum(dice.roll_n(3))) % 10
        player_score[player] += player_pos[player] + 1
        player_index = (player_index + 1) % 2

    print(player_score[players[player_index]], dice.roll_count)

    return player_score[players[player_index]] * dice.roll_count


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

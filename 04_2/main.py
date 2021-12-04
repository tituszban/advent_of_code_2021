class Card:
    def __init__(self, card):
        self._grid = [[c for c in row.split(" ") if c] for row in card]
        self._winner_cache = None

    @property
    def is_winner(self):
        def check_rows():
            for row in self._grid:
                if all(n is None for n in row):
                    return True
            return False
        
        def check_columns():
            for col in zip(*self._grid):
                if all(n is None for n in col):
                    return True
            return False

        if self._winner_cache is None:
            self._winner_cache = check_rows() or check_columns()
        
        return self._winner_cache

    @property
    def unmarked_sum(self):
        return sum(int(n) for row in self._grid for n in row if n)

    def apply_number(self, n):
        self._winner_cache = None
        for i in range(len(self._grid)):
            for j in range(len(self._grid[i])):
                if self._grid[i][j] == n:
                    self._grid[i][j] = None

def play_cards(cards, numbers):
    for n in numbers:
        for card in cards:
            if card.is_winner:
                continue
            card.apply_number(n)
            if all(c.is_winner for c in cards):
                return card, n

def solve(test_input):
    numbers = test_input[0]

    cards = list(map(Card, zip(*[test_input[i::6] for i in range(2, 7)])))

    card, n = play_cards(cards, numbers.split(","))

    return card.unmarked_sum * int(n)

example_input = """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7

""".strip().split("\n")

def main():
    with open("04_1/input.txt") as f:
        test_input = list(map(lambda l: l.strip(), f.readlines()))
    
    result = solve(test_input)
    print(result)

if __name__ == "__main__":
    main()

ACs = list[str]

class Cluster:
    def __init__(self, cards: ACs, factors: list[float]):
        self.cards : ACs = cards
        self.factors : list = factors
        self.played : int = 0
        self.factor = factors[0]

    def play(self, card: str):
        i : int = self.cards.index(card)
        self.played = self.played ^ (1 << i)
        self.factor = self.factors[self.played]

    def unplay(self, card: str):
        i : int = self.cards.index(card) # index at other end (b0001)
        self.played = self.played ^ (1 << i)
        self.factor = self.factors[self.played]


if __name__ == "__main__":
    c: Cluster = Cluster(["c1", "c2", "c3", "c4"],
            [x for x in range(16)])
    assert c.factor == 0
    c.play("c1")
    assert c.played == 1
    assert c.factor == 1
    c.play("c2")
    assert c.played == 3
    assert c.factor == 3
    c.unplay("c1")
    assert c.played == 2
    assert c.factor == 2


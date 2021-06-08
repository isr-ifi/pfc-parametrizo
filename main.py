
ACs = list[str]

class Cluster:
    def __init__(self, cards: ACs, factors: list[float]):
        self.cards : ACs = cards
        self.factors : list = factors
        self.played : str = "0000"

    def play(self, card: str):
        i : int = 3 - self.cards.index(card) # index at other end (b0001)
        self.played = self.played[:i] + "1" + self.played[i + 1:]

    def unplay(self, card: str):
        i : int = 3 - self.cards.index(card) # index at other end (b0001)
        self.played = self.played[:i] + "0" + self.played[i + 1:]

    def factor(self, cards: ACs):
        pass

if __name__ == "__main__":
    c: Cluster = Cluster(["c1", "c2", "c3", "c4"],
            [x for x in range(16)])
    c.play("c1")
    assert c.played == "0001"
    c.play("c2")
    assert c.played == "0011"
    c.unplay("c1")
    assert c.played == "0010"
    #assert c.factor == 3
    #assert c.factor(["c1"]) == 0.9
    #assert c.factor(["c1", "c2"]) == 0.8
    #assert c.factor(["c1", "c2"]) == 0.6
    #assert c.factor(["c1", "c2"]) == 0.8

import csv
import logging

logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)

DEBUG = True
ACs = list[str]

def flip(n: int, pos: int):
    """Flip the bit on int n at position pos"""
    return n ^ (1 << pos)

class Cluster:
    def __init__(self, cards: ACs, factors: list[float] = []):
        """
        If no `factors` are passed, then a list of 0s of size `2 ** cards` is created.
        """
        self.cards : ACs = cards
        self.factors : list = factors
        self.played : int = 0
        if len(self.factors) == 0:
            self.factors = [0] * (2**len(cards))
        if len(self.factors) > 0:
            self.factor = self.factors[0]
        assert len(self.factors) == 2 ** len(cards)

    def play(self, card: str):
        self.played = flip(self.played, self.cards.index(card))
        self.factor = self.factors[self.played]

    def unplay(self, card: str):
        self.played = flip(self.played, self.cards.index(card))
        self.factor = self.factors[self.played]

    def get_idx(self, cards: ACs):
        """Returns the index at which the value for the combination is"""
        pos : int = 0
        for i in cards:
            pos = flip(pos, self.cards.index(i))
        return pos

def read_from_file(file_name : str):
    clusters : list[Cluster] = []
    with open(file_name) as f:
        r = csv.reader(f)
        for row in r:
            if row[0] == "Cluster":
                logging.info('\n###\tCluster: {}\n\tAffects: {}\n\tCards: {}'
                        .format(row[1], row[2], row[4:]))
                clusters.append(Cluster(row[4:]))
            else:
                clusters[-1].factors[clusters[-1].get_idx(row[:-1])] = row[-1]
    return clusters

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

    # Test correct positions of values in list
    assert 15 == c.get_idx(["c1", "c2", "c3", "c4"])
    assert 9 == c.get_idx(["c4", "c1"])

    clusters = read_from_file("acs.csv")
    logging.debug(clusters[0].cards)
    logging.debug(clusters[0].factors)
    logging.debug(clusters[1].cards)
    logging.debug(clusters[1].factors)

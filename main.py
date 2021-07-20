import csv
import logging
from functools import reduce
from typing import Optional

logging.basicConfig(level=logging.WARNING)

ACs = list[str]

def flip(n: int, pos: int):
    """Flip the bit on int n at position pos"""
    return n ^ (1 << pos)

class Cluster:
    def __init__(self, name: str, mfa_var: str, effect: str, cards: ACs,
            factors: Optional[list[float]] = None):
        """
        If no `factors` are passed it defaults to a list of 1s of size `2 ** cards`
        """
        self.name = name
        self.mfa_var = mfa_var
        self.effect = effect # either mul or sum
        n_effect = 1 if effect == 'mul' else 0
        self.cards = cards
        self.played = 0
        self.factors = factors or [n_effect] * (2**len(cards))
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
        return reduce(flip, map(self.cards.index, cards), 0)

def read_from_file(file_name : str):
    clusters : list[Cluster] = []
    with open(file_name) as f:
        r = csv.reader(f)
        for row in r:
            if row[0] == "Cluster":
                logging.debug(f'\n###\tCluster: {row[1]}\n\tAffects: {row[2]}\n\tCards: {row[4:]}')
                clusters.append(Cluster(row[1], row[2], row[3], row[4:]))
            else:
                clusters[-1].factors[clusters[-1].get_idx(row[:-1])] = float(row[-1])
    return clusters

if __name__ == "__main__":
    c: Cluster = Cluster('Test', 'a.b', 'mul', ["c1", "c2", "c3", "c4"],
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
    logging.debug(clusters[2].factors)
    logging.debug(clusters[3].factors)

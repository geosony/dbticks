from difflib import SequenceMatcher
import numpy as np
import itertools


class Similarity:

    def calcSimilarity(self, s1, s2):
        l = [s1, s2]
        sim = lambda x: np.mean([SequenceMatcher(None, a,b).ratio() for a,b in itertools.combinations(x, 2)])
        return sim(l)

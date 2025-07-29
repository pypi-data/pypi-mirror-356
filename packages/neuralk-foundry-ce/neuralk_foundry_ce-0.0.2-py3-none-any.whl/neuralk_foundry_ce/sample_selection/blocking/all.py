import numpy as np

from .base import BaseBlocking
from ...utils.splitting import with_masked_split


class AllPairsBlocking(BaseBlocking):
    name = "all-pairs-blocking"

    def __init__(self):
        super().__init__(leaking=False)

    @with_masked_split
    def train(self, X, y):
        pass

    @with_masked_split
    def forward(self, X, y):
        # Generate all pairs of indices
        indices = np.arange(len(X))
        index_pairs = [(i, j) for i in indices for j in indices if i < j]
        y_pairs = np.array([int(y[i] == y[j]) for i, j in index_pairs])
        return index_pairs, y_pairs
    
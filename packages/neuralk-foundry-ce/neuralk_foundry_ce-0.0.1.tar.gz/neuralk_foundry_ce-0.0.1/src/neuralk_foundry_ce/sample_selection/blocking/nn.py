import numpy as np
from sklearn.neighbors import NearestNeighbors

from .base import BaseBlocking
from ...utils.splitting import with_masked_split


class NearestNeighborsBlocking(BaseBlocking):
    name = "nearest-neighbors-blocking"

    def __init__(self, n_neighbors=50):
        super().__init__(leaking=False)
        self.n_neighbors = n_neighbors
        self.nn_model = None

    @with_masked_split
    def train(self, X, y):
        # Fit nearest neighbors model
        self.nn_model = NearestNeighbors(n_neighbors=self.n_neighbors + 1, algorithm="auto")
        self.nn_model.fit(X)

    @with_masked_split
    def forward(self, X, y):
        self.nn_model = NearestNeighbors(n_neighbors=self.n_neighbors + 1, algorithm="auto")
        self.nn_model.fit(X)

        # Get k-nearest neighbors for each point (excluding self-pairs)
        distances, neighbors = self.nn_model.kneighbors(X)

        # Construct unique index pairs
        index_pairs = []
        for i, nbrs in enumerate(neighbors):
            for j in nbrs[1:]:  # skip self
                if i < j:
                    index_pairs.append((i, j))
                elif j < i:
                    index_pairs.append((j, i))

        # Remove duplicates
        index_pairs = list(set(index_pairs))

        # Compute y_pairs
        y_pairs = np.array([int(y[i] == y[j]) for i, j in index_pairs])
        return index_pairs, y_pairs
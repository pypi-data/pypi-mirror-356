import numpy as np
import pandas as pd

from ...workflow import Step, Field
from ...utils.splitting import with_masked_split, Split


class BaseBlocking(Step):

    inputs = [
        Field('X', 'Input features for each record'),
        Field('y', 'Group identifiers indicating which records refer to the same entity'),
        Field('splits', 'Masks for train, validation, and test sets'),
    ]

    outputs = [
        Field("index_pairs", "List of index tuples representing candidate record pairs"),
        Field("X_pairs", "Concatenated feature representations for each record pair"),
        Field("y_pairs", "Binary labels indicating whether each pair is a match (1) or a non-match (0)"),
        Field("splits_pairs", "Masks for train, validation, and test sets at the pair level"),
    ]

    def __init__(self, leaking):
        super().__init__()
        self.leaking = leaking
        
    @with_masked_split
    def train(self, X, y):
        raise NotImplementedError("train method should be implemented in subclasses")

    @with_masked_split
    def forward(self, X, y):
        raise NotImplementedError("train method should be implemented in subclasses")
    

    def _execute(self, inputs: dict) -> dict:
        """
        For *all* splits collect a unified list of unique pairs, one y-label
        per pair, and a (n_splits × n_pairs) matrix telling in which subset
        (train/val/test/none) each pair lives for every split.
        """
        X, y, splits = inputs["X"], inputs["y"], inputs["splits"]

        # ------------------------------------------------------------------
        # 1.  Containers
        # ------------------------------------------------------------------
        pair_to_idx: dict[tuple[int, int], int] = {}   # map (i,j) -> global id
        index_pairs: list[tuple[int, int]] = []        # global list of pairs
        y_pairs: list = []                             # y label per pair

        # we will fill this after we know n_splits × n_pairs
        per_split_membership: list[list[tuple[tuple[int,int], int]]] = []

        # ------------------------------------------------------------------
        # 2.  Iterate over splits – collect pairs and remember their subset
        # ------------------------------------------------------------------
        for split_mask in splits:
            split_members: list[tuple[tuple[int, int], int]] = []  # (pair, subset)
            split_mask = np.array(split_mask)

            def collect(subset_flag):
                reindexer = np.arange(len(X))[np.isin(split_mask, [subset_flag])]
                pairs, y_local = self.forward(X, y, split_mask, splits=[subset_flag])
                pairs = [(reindexer[i].item(), reindexer[j].item()) for (i, j) in pairs]

                for p, y_val in zip(pairs, y_local):
                    # register pair globally if new
                    if p not in pair_to_idx:
                        pair_to_idx[p] = len(index_pairs)
                        index_pairs.append(p)
                        y_pairs.append(y_val)
                    # remember that in *this* split the pair has `subset_flag`
                    split_members.append((p, subset_flag))

            collect(Split.TRAIN)
            collect(Split.VAL)
            collect(Split.TEST)

            per_split_membership.append(split_members)

        # ------------------------------------------------------------------
        # 3.  Build the (n_splits × n_pairs) membership mask
        # ------------------------------------------------------------------
        n_splits, n_pairs = len(splits), len(index_pairs)
        splits_pairs_masks = [np.full(n_pairs, Split.NONE, dtype=int) for _ in range(n_splits)]

        for s_idx, (split_members, splits_pairs_mask) in enumerate(zip(per_split_membership, splits_pairs_masks)):
            for pair, subset_flag in split_members:
                p_idx = pair_to_idx[pair]
                splits_pairs_mask[p_idx] = subset_flag

        # ------------------------------------------------------------------
        # 4.  Output
        # ------------------------------------------------------------------
        # convert y_pairs to a numpy array if you prefer
        self.output("index_pairs", index_pairs)                # list[(i,j)]
        index_1, index_2 = zip(*index_pairs)
        self.output("X_pairs", pd.concat([
            X.iloc[list(index_1)].reset_index(drop=True).add_suffix("_1"),
            X.iloc[list(index_2)].reset_index(drop=True).add_suffix("_2")
        ], axis=1))
        self.output("y_pairs", np.asarray(y_pairs))
        self.output("splits_pairs", splits_pairs_masks)      # (n_splits,n_pairs)
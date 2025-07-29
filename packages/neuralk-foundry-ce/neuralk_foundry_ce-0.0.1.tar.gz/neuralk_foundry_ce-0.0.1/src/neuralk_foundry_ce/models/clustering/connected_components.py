from typing import List, Tuple

import numpy as np
import networkx as nx
import optuna
from sklearn.metrics import adjusted_rand_score

from ...utils.splitting import Split
from ...workflow import Step, Field


def extract_clusters_from_scores(
    index_pairs: List[Tuple[int, int]],
    y_score_pairs: List[float],
    threshold: float,
    num_nodes: int,
    ref_idx: np.ndarray,
) -> np.ndarray:
    """
    Extracts connected components as cluster labels from a thresholded edge list.

    Args:
        index_pairs: List of (i, j) edges.
        y_pred_scores: Predicted scores for each edge.
        threshold: Minimum score to include an edge.
        num_nodes: Total number of nodes (assumed to be labeled 0 to num_nodes-1).

    Returns:
        A NumPy array of shape (num_nodes,) with cluster labels.
    """
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))

    node_mapper = {node_id: abs_id for node_id, abs_id in zip(ref_idx, range(ref_idx.shape[0]))}
    for (i, j), score in zip(index_pairs, y_score_pairs):
        if score >= threshold:
            G.add_edge(node_mapper[i], node_mapper[j])

    components = list(nx.connected_components(G))
    labels = np.full(num_nodes, -1, dtype=int)

    for cluster_id, component in enumerate(components):
        for node in component:
            labels[node] = cluster_id

    return labels


def optimize_clustering_threshold(
    index_pairs: List[Tuple[int, int]],
    y_score_pairs: List[float],
    y_true: np.ndarray,
    ref_idx: np.ndarray,
    n_trials: int = 50,
) -> Tuple[float]:
    """
    Uses Optuna to find the best threshold on edge scores to extract
    clusters as connected components and maximize ARI.

    Args:
        index_pairs: List of (i, j) tuples indicating candidate edges.
        y_pred_scores: List of float scores for each edge.
        true_labels: np.ndarray of shape (num_nodes,), cluster IDs.
        n_trials: Number of Optuna trials.
        ref_idx: mapping table between node and absolute index
        direction: Optimization direction ('maximize' for ARI).

    Returns:
        best_threshold: The threshold that gave the best ARI.
    """
    num_nodes = len(y_true)
    assert len(index_pairs) == len(y_score_pairs), "Mismatch in edge data lengths"

    def objective(trial: optuna.Trial) -> float:
        threshold = trial.suggest_float("threshold", 0.0, 1.0)
        pred_labels = extract_clusters_from_scores(index_pairs, y_score_pairs, threshold, num_nodes, ref_idx)
        return adjusted_rand_score(y_true, pred_labels)

    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)

    return study.best_params["threshold"]


class ComponentExtractor(Step):
    """
    Extracts connected components from predicted record pairs to assign group identifiers.

    This step operates on pairwise predictions indicating whether two records refer to the same entity.
    Based on these predictions, it constructs connected components (clusters) of matching records
    and assigns a unique group ID to each component. The output is a sample-level prediction of entity IDs.

    Parameters
    ----------
    index_pairs : list of tuple of int
        List of index tuples representing record pairs.

    y_score_pairs : array-like of shape (n_pairs,)
        Predicted probability that each pair refers to the same entity.

    y_pairs : array-like of shape (n_pairs,)
        Binary labels indicating whether each pair is a match (1) or not (0).

    splits_pairs : dict of str to array-like of bool
        Boolean masks indicating train/val/test membership at the pair level.

    y : array-like of shape (n_samples,)
        Sample-level ground truth labels, used for evaluation.

    splits : dict of str to array-like of bool
        Boolean masks indicating train/val/test membership at the sample level.

    Returns
    -------
    y_pred : array-like of shape (n_samples,)
        Predicted group IDs, where each unique value identifies a connected component (i.e., an entity).

    Notes
    -----
    - Components are constructed using a threshold or clustering logic based on the pairwise scores.
    - This step assumes the input pairs represent undirected edges in a similarity graph.
    - Evaluation (e.g., clustering metrics) can be done downstream using `y` and `y_pred`.
    """

    name = "component-extractor"
    inputs = [
        Field("index_pairs", "List of index tuples representing record pairs"),
        Field("y_score_pairs", "Predicted probability that each pair refers to the same entity"),
        Field("y_pairs", "Binary labels indicating whether each pair is a match (1) or not (0)"),
        Field("splits_pairs", "Boolean masks for train, validation, and test sets at the pair level"),
        Field('y', 'Target variable to predict'),
        Field('splits', 'Masks for train, validation, and test sets'),
    ]
    outputs = [
        Field('y_pred', 'Sample-level predicted entity/group ID indicating matched record clusters'),
    ]

    def _execute(self, inputs: dict) -> dict:
        index_pairs = inputs["index_pairs"]
        y_score_pairs = inputs["y_score_pairs"]
        splits_pairs = inputs["splits_pairs"]
        splits = inputs["splits"]
        y_true = inputs["y"]

        if y_score_pairs.shape[1] == 2:
            y_score_pairs = y_score_pairs[:, 1:]

        ref_idx = np.arange(y_true.shape[0])

        # First, calibrate the thresholding on train
        train_mask = np.isin(np.array(splits_pairs[0]), [Split.TRAIN])
        best_thr = optimize_clustering_threshold(
            np.array(index_pairs)[train_mask],
            y_score_pairs[train_mask],
            y_true[np.isin(np.array(splits[0]), [Split.TRAIN])],
            ref_idx[np.isin(np.array(splits[0]), [Split.TRAIN])],
            n_trials=20,
        )

        self.log_metric('best_threshold', best_thr)

        y_pred = -np.ones(np.array(splits[0]).shape[0], dtype=int)

        for split in (Split.TRAIN, Split.VAL, Split.TEST):
            split_mask_pairs = np.isin(np.array(splits_pairs[0]), [split])
            split_mask = np.isin(np.array(splits[0]), [split])

            y_pred_split = extract_clusters_from_scores(
                np.array(index_pairs)[split_mask_pairs],
                y_score_pairs[split_mask_pairs],
                best_thr,
                np.sum(split_mask),
                ref_idx[split_mask],
            )
            y_pred[split_mask] = y_pred_split
            self.log_metric(f'ari_{split.name.lower()}', adjusted_rand_score(y_true[split_mask], y_pred_split))

        self.output("y_pred", y_pred)

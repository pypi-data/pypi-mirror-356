import itertools
import logging
from typing import Dict, List, Tuple

import numpy as np
import torch

log = logging.getLogger(__name__)
print = log.info


def sample_on_segment(
    feat1: torch.Tensor, feat2: torch.Tensor, n_sampled: int
) -> List[torch.Tensor]:
    """
    Sample equidistant points on a segment between two vectors.

    Arguments:
        feat1 (torch.Tensor): first vector
        feat2 (torch.Tensor): second vector
        n_sampled (int): number of sampled points

    Returns:
        List[torch.Tensor]: sampled vectors
    """
    new_points = []
    lambda_ = 1 / (n_sampled + 1)
    for i in range(n_sampled):
        new_lambda = (i + 1) * lambda_
        new_points.append(new_lambda * feat1 + (1 - new_lambda) * feat2)
    return new_points


def euclidean_one_concept(
    features: np.ndarray,
    indices: np.ndarray,
    label_id: int,
    predict_from_middle,
    layer: int,
    n_pairs: int = 5000,
    n_sampled: int = 10,
) -> List:
    """
    Compute Euclidean convexity for one concept.

    Arguments:
        features (np.ndarray): latent representations with shape (n_data, n_tokens, n_features)
        indices (np.ndarray): indices of the points belonging to the concept
        label_id (int): label id of the concept known by the model
        predict_from_middle (function): function that takes features as input and returns predictions:
                                        inputs: features (shape (n_interpolated data, n_tokens, n_features)),
                                                layer (int),
                                        output: predictions (shape n_interpolated data),
        layer (int): layer to compute Euclidean convexity for
        n_pairs (int): maximum number of pairs within a concept used for evaluation
        n_sampled (int): number of points sampled on each segment

    Returns:
        List: list of Euclidean convexity scores for each pair of points
    """
    scores = []
    all_paths = list(itertools.combinations(indices, r=2))
    n_paths_max = min(len(all_paths), n_pairs)
    sampled_indices = np.random.choice(
        list(range(len(all_paths))), n_paths_max, replace=False
    )
    sampled_paths = [all_paths[index] for index in sampled_indices]
    for id1, id2 in sampled_paths:
        new_points = sample_on_segment(features[id1], features[id2], n_sampled)
        predictions = predict_from_middle(torch.asarray(np.stack(new_points)), layer)
        is_correct = [pred == label_id for pred in predictions]
        n_correct = sum(is_correct) / len(is_correct)
        scores.append(n_correct)
    return scores


def compute_euclidean_convexity(
    representations: np.ndarray,
    labels: np.ndarray,
    predict_from_middle,
    layer: int,
    n_pairs: int = 5000,
    n_sampled: int = 10,
) -> Tuple[float, Dict[int, float]]:
    """
    Compute Euclidean convexity for given representations and labels.

    Arguments:
        representations (np.ndarray): latent representations with shape (n_data, n_tokens, n_features)
        labels (np.ndarray): labels with shape (n_data,)
        predict_from_middle (function): function that takes features as input and returns predictions:
                                        inputs: features (shape (n_interpolated data, n_tokens, n_features)),
                                                layer (int),
                                        output: predictions (shape n_interpolated data),
        layer (int): layer to compute Euclidean convexity for
        n_pairs (int): maximum number of pairs within a concept used for evaluation
        n_sampled (int): number of points sampled on each segment

    Returns:
        float: mean Euclidean convexity over all pairs
        Dict[int, float]: dictionary mapping concept label to Euclidean convexity of that concept
    """
    convexity = {}
    individual_scores = []
    labels_set = set(labels)

    for i, label in enumerate(labels_set):
        ids = np.argwhere(np.array(labels) == label).flatten()
        proportion = euclidean_one_concept(
            representations,
            ids,
            label_id=label,
            predict_from_middle=predict_from_middle,
            layer=layer,
            n_pairs=n_pairs,
            n_sampled=n_sampled,
        )
        individual_scores.extend(proportion)
        convexity[label] = round(np.mean(proportion) * 100, 2)
    mean_convexity = round(np.mean(individual_scores) * 100, 2)
    return mean_convexity, convexity

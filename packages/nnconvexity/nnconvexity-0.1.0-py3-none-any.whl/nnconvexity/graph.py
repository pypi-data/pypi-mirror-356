import itertools
from typing import Dict, List, Tuple

import numpy as np
import pandas
import pandas as pd
from igraph import Graph
from joblib import Parallel, delayed
from scipy.spatial.distance import cdist


def nearest_neighbors_one(
    id: int,
    n_neigh: int,
    df: pandas.DataFrame,
    df_dist: pandas.DataFrame,
    df_inc: pandas.DataFrame,
):
    """
    Finds nearest neighbors for given id.

    Arguments:
        id (int): index
        n_neigh (int): number of nearest neighbors
        df (pandas.DataFrame): distance matrix
        df_dist (pandas.DataFrame): distance matrix of only n_neigh nearest neighbors saved, other distances are 0
        df_inc (pandas.DataFrame): incidence matrix of df_dist
    """
    distances = df.loc[id]
    shortest = distances.nsmallest(n=n_neigh + 1)
    for key, val in shortest.items():
        if val > 0:
            df_inc.loc[key, id] = 1
            df_dist.loc[key, id] = val


def get_nearest_neighbors(
    df: pandas.DataFrame,
    n: int,
    n_parallel: int,
) -> Tuple[pandas.DataFrame, pandas.DataFrame]:
    """
    Find n nearest neighbors. For each node, its nearest neigbors are in rows of
    df (distances) and df_inc (incidence).

    Arguments:
        df (pandas.DataFrame):     Distances between each pair of nodes
        n (int):      Number of nearest neighbors
        n_parallel (int):  Number of parallel jobs

    Returns:
        pandas.DataFrame:    Only distances within n nearest neighbors are kept, the rest
                    is changed to 0
        pandas.DataFrame:     Incidence matrix
    """
    df_inc = pd.DataFrame(0, index=df.index, columns=df.columns)
    df_dist = pd.DataFrame(0, index=df.index, columns=df.columns, dtype=np.float64)
    Parallel(n_jobs=n_parallel, verbose=0, require="sharedmem")(
        delayed(nearest_neighbors_one)(id, n, df, df_dist, df_inc) for id in df.index
    )
    return df_dist, df_inc


def is_path_in_concept(
    shortest_path: List[int],
    indices: np.ndarray,
) -> float:
    """
    Compute the proportion of the path that is within the concept.

    Arguments:
        shortest_path (List[int]):  list of all vertices on the path
        indices (np.ndarray):        list of all vertices belonging to the concept

    Returns:
        float:      the proportion of the path that is inside the concept
    """
    if len(shortest_path) <= 2:
        prop = 1
    else:
        length = 0
        outside = 0
        for idx in shortest_path[1:-1]:
            length += 1
            if idx not in indices:
                outside += 1
        prop = (length - outside) / length
    return prop


def compute_paths(
        graph: Graph,
        indices: np.ndarray,
        n_paths: int,
        ) -> List[float]:
    """
    what is this about

    Arguments:
        graph (Graph): graph with datapoints in vertices and weighted edges are Euclidean distances to
               the n closest nearest neighbors
        indices (np.ndarray): indices of vertices belonging to the concept
        n_paths (int): maximum number of paths

    Returns:
        List[float]: list of proportion of each path inside the concept
    """
    all_paths = list(itertools.permutations(indices, r=2))
    n_paths_max = min(len(all_paths), n_paths)
    sampled_indices = np.random.choice(
        list(range(len(all_paths))), n_paths_max, replace=False
    )
    sampled_paths = [all_paths[index] for index in sampled_indices]
    proportion = []
    for id1, id2 in sampled_paths:
        shortest_path = graph.get_shortest_paths(
            id1, to=id2, weights=graph.es["weight"], output="vpath"
        )
        if len(shortest_path[0]) == 0:
            proportion.append(0)
        else:
            prop = is_path_in_concept(shortest_path[0], indices)
            proportion.append(prop)
    return proportion


def compute_graph_convexity(
    representations: np.ndarray,
    labels: np.ndarray,
    n_neighbors: int = 10,
    max_n_paths: int = 5000,
    n_parallel: int = 1,
) -> Tuple[
    float, Dict[int, float]
]:
    """
    Compute graph convexity for given representations and labels.

    Arguments:
        representations (np.ndarray): latent representations with shape (n_data, n_features)
        labels (np.ndarray): labels with shape (n_data,)
        n_neighbors (int): number of nearest neighbors
        max_n_paths (int): maximum number of paths used for evaluation
        n_parallel (int): number of parallel jobs

    Returns:
        float: mean graph convexity over all paths
        Dict[int, float]: dictionary mapping concept label to graph convexity of that concept
    """
    # Create graph
    labels_set = set(labels)
    convexity = {}
    scores_per_path = []
    dist_matrix = cdist(representations, representations, metric="euclidean")
    distances = pd.DataFrame(dist_matrix)
    distances_nearest, _ = get_nearest_neighbors(distances, n_neighbors, n_parallel)
    graph_matrix = distances_nearest.to_numpy().astype(float)
    symmetric = np.maximum(graph_matrix, graph_matrix.T)
    graph = Graph.Weighted_Adjacency(symmetric)

    for i, label in enumerate(labels_set):
        ids = np.argwhere(np.array(labels) == i).flatten()
        proportion = compute_paths(graph, ids, max_n_paths)
        scores_per_path.extend(proportion)
        convexity[label] = round(np.mean(proportion) * 100, 2)
    mean_convexity = round(np.mean(scores_per_path) * 100, 2)
    return mean_convexity, convexity

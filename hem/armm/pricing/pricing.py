
# Copyright (c) 2022 Tolam Earth
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import numpy as np
from scipy.stats.mstats import gmean

eigenvalues_threshold = 1e-3


def eigenvalues_calculator(x_matrix: np.ndarray, q: np.ndarray) -> np.ndarray:
    """

    :param x_matrix: the n*k attribute matrix with columns being the centroid of the clusters
    :param q: array of quantity of items in clusters

    :return: array of eigenvalues
    """
    z = np.matmul(np.matmul(x_matrix, np.diag(q)), np.transpose(x_matrix))
    eigenvalues = np.linalg.svd(z, full_matrices=False,
                                compute_uv=False, hermitian=True)
    return eigenvalues[eigenvalues > eigenvalues_threshold]


def arm_buys_price(x_matrix: np.ndarray, q: np.ndarray, pool_index: int, n_nft: int, r: float) -> float:
    """

    :param x_matrix: the n*k attribute matrix with columns being the centroid of the clusters
    :param q: array of quantity of items in clusters
    :param pool_index: integer index referring to the position of the pool in q (the columns of X belonging to the pool)
    :param n_nft: number of NFTs in the current call
    :param r: quantity of a reserve currency in USD cents

    :return: the maximum total price ARMM is willing to pay to buy the nfts (it is price per the batch)
    """
    eigenvalues = eigenvalues_calculator(x_matrix, q)
    delta_q = np.copy(q)
    delta_q[pool_index] += n_nft
    delta_eigenvalues = eigenvalues_calculator(x_matrix, delta_q)
    return r * (gmean(delta_eigenvalues / eigenvalues) - 1)


def arm_sells_price(x_matrix: np.ndarray, q: np.ndarray, pool_index: int, n_nft: int, r: float) -> float:
    """

    :param x_matrix: the n*k attribute matrix with columns being the centroid of the clusters
    :param q: array of quantity of items in clusters
    :param pool_index: integer index referring to the position of the pool in q (the columns of X belonging to the pool)
    :param n_nft: number of NFTs in the current call
    :param r: quantity of a reserve currency in USD cents

    :return: the minimum total price ARMM is willing to receive to sell the nfts (it is price per the batch)
    """
    eigenvalues = eigenvalues_calculator(x_matrix, q)
    delta_q = np.copy(q)
    delta_q[pool_index] -= n_nft
    delta_eigenvalues = eigenvalues_calculator(x_matrix, delta_q)
    return r * (1 - gmean(delta_eigenvalues / eigenvalues))

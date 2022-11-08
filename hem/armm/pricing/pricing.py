import numpy as np
from scipy.stats.mstats import gmean

eigenvalues_threshold = 1e-3


def eigenvalues_calculator(x_matrix: np.ndarray, q: np.ndarray) -> np.ndarray:
    z = np.matmul(np.matmul(x_matrix, np.diag(q)), np.transpose(x_matrix))
    eigenvalues = np.linalg.svd(z, full_matrices=False,
                                compute_uv=False, hermitian=True)
    return eigenvalues[eigenvalues > eigenvalues_threshold]


def arm_buys_price(x_matrix: np.ndarray, q: np.ndarray, pool_index: int, n_nft: int, r: float) -> float:
    eigenvalues = eigenvalues_calculator(x_matrix, q)
    delta_q = np.copy(q)
    delta_q[pool_index] += n_nft
    delta_eigenvalues = eigenvalues_calculator(x_matrix, delta_q)
    return r * (gmean(delta_eigenvalues / eigenvalues) - 1)


def arm_sells_price(x_matrix: np.ndarray, q: np.ndarray, pool_index: int, n_nft: int, r: float) -> float:
    eigenvalues = eigenvalues_calculator(x_matrix, q)
    delta_q = np.copy(q)
    delta_q[pool_index] -= n_nft
    delta_eigenvalues = eigenvalues_calculator(x_matrix, delta_q)
    return r * (1 - gmean(delta_eigenvalues / eigenvalues))

# helpers.py

import numpy as np

def find_index(array: np.ndarray, value: float) -> int:
    """Return the index of the closest value in array."""
    return int(np.argmin(np.abs(array - value)))

def compute_background_noise(photon_counts: np.ndarray, altitudes: np.ndarray) -> float:
    idx_180 = find_index(altitudes, 150)
    idx_200 = find_index(altitudes, 200)
    return float(np.nanmean(photon_counts[idx_180:idx_200]))

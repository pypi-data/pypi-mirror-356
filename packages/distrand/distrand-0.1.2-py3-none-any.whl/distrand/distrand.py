import numpy as np
import random

def distrand(low, high, size, min_dist, dtype):
    """
    Generate `size` random values between `low` and `high`, such that all values
    are at least `min_dist` apart. No sorting, no seed, no dtype inference.

    Parameters:
    ----------
    low : int or float
        Lower bound of range.
    high : int or float
        Upper bound of range.
    size : int
        Number of random values to return.
    min_dist : int or float
        Minimum spacing between any two values.
    dtype : type or np.dtype
        Desired output type (e.g., int or float).

    Returns:
    -------
    np.ndarray
        Array of values spaced at least `min_dist` apart.
    
    Raises:
    ------
    ValueError
        If it's impossible to choose `size` unique values with the given spacing.
    """
    use_int_mode = (
        dtype == int
        and all(isinstance(x, int) for x in [low, high, min_dist])
    )

    if use_int_mode:
        # Integer mode: sample freely with spacing checks
        if (high - low + 1) < (size - 1) * min_dist + 1:
            raise ValueError(
                f"Cannot select {size} values from range [{low}, {high}] with min_dist={min_dist}"
            )

        selected = []
        attempts = 0
        max_attempts = 10000

        while len(selected) < size and attempts < max_attempts:
            candidate = random.randint(low, high)
            if all(abs(candidate - x) >= min_dist for x in selected):
                selected.append(candidate)
            attempts += 1

        if len(selected) < size:
            raise RuntimeError("Failed to generate enough spaced integers after many attempts.")

        return np.array(selected, dtype=int)

    else:
        pool = np.arange(float(low), float(high), float(min_dist))
        if len(pool) < size:
            raise ValueError(
                f"Cannot select {size} values from range [{low}, {high}] with min_dist={min_dist}"
            )

        selected = np.random.choice(pool, size=size, replace=False)
        return selected.astype(dtype)

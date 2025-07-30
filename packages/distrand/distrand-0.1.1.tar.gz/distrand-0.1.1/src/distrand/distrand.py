# distrand.py

# Copyright 2025 Syed Mohammad Talha Husain
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np

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
        pool = np.arange(low, high + min_dist, min_dist, dtype=int)
    else:
        pool = np.arange(float(low), float(high), float(min_dist))

    if len(pool) < size:
        raise ValueError(
            f"Cannot select {size} values from range [{low}, {high}] with min_dist={min_dist}"
        )

    selected = np.random.choice(pool, size=size, replace=False)

    # Avoid unnecessary conversion
    if selected.dtype != np.dtype(dtype):
        selected = selected.astype(dtype)

    return selected

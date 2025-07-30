# test_distrand.py

import numpy as np
import pytest
from distrand import distrand

def test_integer_mode():
    values = distrand(low=0, high=100, size=5, min_dist=10, dtype=int)
    assert len(values) == 5
    assert all(isinstance(v, (int, np.integer)) for v in values)
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            assert abs(values[i] - values[j]) >= 10

def test_float_mode():
    values = distrand(low=0.0, high=5.0, size=4, min_dist=1.0, dtype=float)
    assert len(values) == 4
    assert all(isinstance(v, (float, np.floating)) for v in values)
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            assert abs(values[i] - values[j]) >= 1.0

def test_invalid_distance():
    with pytest.raises(ValueError):
        distrand(low=0, high=10, size=5, min_dist=5, dtype=int)

def test_negative_distance_error():
    with pytest.raises(ValueError):
        distrand(low=0, high=10, size=3, min_dist=-2, dtype=float)

def test_dtype_casting():
    values = distrand(low=0, high=20, size=3, min_dist=5, dtype=float)
    assert values.dtype == np.float64
    
def test_int_mode_spacing_not_grid_aligned():
    from distrand import distrand
    nums = distrand(100, 200, size=6, min_dist=7, dtype=int)
    assert len(nums) == 6
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            assert abs(nums[i] - nums[j]) >= 7

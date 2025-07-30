import pytest
from kadane_adv.core import (
    kadane_max_sum,
    kadane_max_subarray,
    kadane_with_min_length,
    kadane_2d
)

def test_kadane_max_sum():
    assert kadane_max_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6

def test_kadane_max_subarray():
    s, sub = kadane_max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    assert s == 6
    assert sub == [4, -1, 2, 1]

def test_kadane_with_min_length():
    s, sub = kadane_with_min_length([1, 2, 3, -2, 5], 3)
    assert s == 9
    assert sub == [1, 2, 3, -2, 5]

def test_kadane_2d():
    matrix = [
        [1, 2, -1, -4, -20],
        [-8, -3, 4, 2, 1],
        [3, 8, 10, 1, 3],
        [-4, -1, 1, 7, -6]
    ]
    max_sum, top_left, bottom_right = kadane_2d(matrix)
    assert max_sum == 29
    assert top_left == (1, 1)
    assert bottom_right == (3, 3)

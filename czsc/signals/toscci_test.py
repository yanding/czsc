import numpy as np
import pytest
from .toscci import cross_number

def test_crossed_above_1d_nb():
    # Test case 1: arr1 crosses above 10
    arr1_case1 = np.array([5, 8, 12, 15, 9])
    num_case1 = 10
    result_case1 = crossed_above_1d_nb(arr1_case1, num_case1)
    expected_result_case1 = np.array([False, False, True, False, False], dtype=bool)
    assert np.array_equal(result_case1, expected_result_case1), "Test case 1 failed"
    # Test case 2: arr1 crosses above 5 with wait=1
    arr1_case2 = np.array([3, 5, 7, 6, 8, 5])
    num_case2 = 5
    wait_case2 = 1
    result_case2 = crossed_above_1d_nb(arr1_case2, num_case2, wait_case2)
    expected_result_case2 = np.array([False, False, False, True, False, False], dtype=bool)
    assert np.array_equal(result_case2, expected_result_case2), "Test case 2 failed"
    # Test case 3: arr1 never crosses above 10
    arr1_case3 = np.array([3, 6, 8, 9, 7])
    num_case3 = 10
    result_case3 = crossed_above_1d_nb(arr1_case3, num_case3)
    expected_result_case3 = np.array([False, False, False, False, False], dtype=bool)
    assert np.array_equal(result_case3, expected_result_case3), "Test case 3 failed"
    print("All test cases passed successfully.")

# Run the test function
test_crossed_above_1d_nb()

def test_crossed_below_1d_nb():
    # Test case 1: arr1 crosses below 10
    arr1_case1 = np.array([15, 12, 10, 8, 11])
    num_case1 = 10
    result_case1 = crossed_below_1d_nb(arr1_case1, num_case1)
    expected_result_case1 = np.array([False, False, False, True, False], dtype=bool)
    assert np.array_equal(result_case1, expected_result_case1), "Test case 1 failed"
    # Test case 2: arr1 crosses below 5 with wait=1
    arr1_case2 = np.array([7, 5, 3, 4, 2, 5])
    num_case2 = 5
    wait_case2 = 1
    result_case2 = crossed_below_1d_nb(arr1_case2, num_case2, wait_case2)
    expected_result_case2 = np.array([False, False, False, True, False, False], dtype=bool)
    assert np.array_equal(result_case2, expected_result_case2), "Test case 2 failed"
    # Test case 3: arr1 never crosses below 2
    arr1_case3 = np.array([4, 6, 8, 9, 7])
    num_case3 = 2
    result_case3 = crossed_below_1d_nb(arr1_case3, num_case3)
    expected_result_case3 = np.array([False, False, False, False, False], dtype=bool)
    assert np.array_equal(result_case3, expected_result_case3), "Test case 3 failed"
    print("All test cases passed successfully.")

# Call the test function
test_crossed_below_1d_nb()

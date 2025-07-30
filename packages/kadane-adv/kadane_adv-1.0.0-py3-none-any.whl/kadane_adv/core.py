from typing import List, Tuple
import matplotlib.pyplot as plt

def kadane_max_sum(arr: List[int]) -> int:
    max_sum = float('-inf')
    current_sum = 0
    for num in arr:
        current_sum += num
        max_sum = max(max_sum, current_sum)
        current_sum = max(current_sum, 0)
    return max_sum

def kadane_max_subarray(arr: List[int]) -> Tuple[int, List[int]]:
    max_sum = float('-inf')
    current_sum = 0
    start = end = s = 0
    for i, num in enumerate(arr):
        current_sum += num
        if current_sum > max_sum:
            max_sum = current_sum
            start, end = s, i
        if current_sum < 0:
            current_sum = 0
            s = i + 1
    return max_sum, arr[start:end+1]

def kadane_with_min_length(arr: List[int], min_length: int) -> Tuple[int, List[int]]:
    n = len(arr)
    max_sum = float('-inf')
    best_subarray = []
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            if (j - i + 1) >= min_length and current_sum > max_sum:
                max_sum = current_sum
                best_subarray = arr[i:j+1]
    return max_sum, best_subarray

def kadane_2d(matrix: List[List[int]]) -> Tuple[int, Tuple[int, int], Tuple[int, int]]:
    if not matrix or not matrix[0]:
        return 0, (0, 0), (0, 0)
    rows, cols = len(matrix), len(matrix[0])
    max_sum = float('-inf')
    final_left = final_right = final_top = final_bottom = 0
    for left in range(cols):
        temp = [0] * rows
        for right in range(left, cols):
            for i in range(rows):
                temp[i] += matrix[i][right]
            current_sum = 0
            start = 0
            for i in range(rows):
                current_sum += temp[i]
                if current_sum > max_sum:
                    max_sum = current_sum
                    final_left, final_right = left, right
                    final_top, final_bottom = start, i
                if current_sum < 0:
                    current_sum = 0
                    start = i + 1
    return max_sum, (final_top, final_left), (final_bottom, final_right)

def visualize_subarray(arr: List[int], subarray: List[int]) -> None:
    start = end = -1
    for i in range(len(arr)):
        if arr[i:i+len(subarray)] == subarray:
            start = i
            end = i + len(subarray) - 1
            break
    plt.figure(figsize=(10, 4))
    plt.plot(arr, label='Full Array', color='gray')
    if start != -1:
        plt.plot(range(start, end+1), arr[start:end+1], color='green', label='Max Subarray', linewidth=3)
    plt.title("Kadane's Algorithm: Max Subarray Visualization")
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.show()
"""Sorting algorithms with optional operation counting."""

def insertion_sort(values):
    """Return (sorted_values, comparisons, shifts).

    comparisons counts key-vs-array comparisons in the while condition.
    shifts counts assignments that move an existing array item one position right.
    """
    arr = list(values)
    comparisons = 0
    shifts = 0

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                shifts += 1
                j -= 1
            else:
                break
        arr[j + 1] = key
    return arr, comparisons, shifts


def merge_sort(values):
    """Return a sorted copy using merge sort."""
    arr = list(values)
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

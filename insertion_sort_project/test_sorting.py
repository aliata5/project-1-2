"""Basic correctness tests for the sorting implementations."""
import unittest
from src.sorting import insertion_sort, merge_sort


class SortingTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(insertion_sort([])[0], [])
        self.assertEqual(merge_sort([]), [])

    def test_single_item(self):
        self.assertEqual(insertion_sort([7])[0], [7])
        self.assertEqual(merge_sort([7]), [7])

    def test_duplicates_and_negatives(self):
        data = [3, -1, 3, 0, -8, 2, 2]
        expected = sorted(data)
        self.assertEqual(insertion_sort(data)[0], expected)
        self.assertEqual(merge_sort(data), expected)

    def test_sorted_reverse_random_shapes(self):
        cases = [list(range(20)), list(range(20, 0, -1)), [4, 1, 8, 2, 2, 0]]
        for data in cases:
            expected = sorted(data)
            self.assertEqual(insertion_sort(data)[0], expected)
            self.assertEqual(merge_sort(data), expected)

    def test_insertion_sort_counts(self):
        self.assertEqual(insertion_sort([1, 2, 3])[1:], (2, 0))
        self.assertEqual(insertion_sort([3, 2, 1])[1:], (3, 3))


if __name__ == "__main__":
    unittest.main()

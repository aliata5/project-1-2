import random
import unittest
from benchmark import ALGORITHMS

class SortingTests(unittest.TestCase):
    def test_algorithms(self):
        rng = random.Random(17)
        samples = [[], [1], [2, 1], [3, 3, 3], list(range(200)),
                   list(range(199, -1, -1)), [rng.randrange(-100, 100) for _ in range(300)]]
        for name, func in ALGORITHMS.items():
            for sample in samples:
                with self.subTest(algorithm=name, size=len(sample)):
                    before = sample.copy()
                    self.assertEqual(func(sample), sorted(sample))
                    self.assertEqual(sample, before)

if __name__ == '__main__':
    unittest.main()

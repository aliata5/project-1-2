# Empirical Analysis of Insertion Sort

## Objective
Implement insertion sort, count key comparisons and shifts, and measure its performance on sorted, reverse-sorted, and random arrays. Compare measured growth with theoretical complexity and with merge sort.

## Methodology
Python 3 was used with input sizes n = 100, 250, 500, 1,000, 2,000, 3,000, 4,000, and 5,000. Each runtime is the median of three measurements using `time.perf_counter()`. Random data is reproducible (fixed seed). Every output was checked against Python's sorted result. The reported shift count means assignments moving an existing element one position to the right.

## Results and Analysis
At n = 5,000, insertion sort recorded:

| Input arrangement | Comparisons | Shifts | Median time (s) |
|---|---:|---:|---:|
| Sorted | 4,999 | 0 | 0.000513 |
| Reverse-sorted | 12,497,500 | 12,497,500 | 1.432642 |
| Random | 6,116,226 | 6,111,237 | 0.749601 |

The sorted case is the best case: approximately n−1 comparisons and no shifts, consistent with **O(n)** time. Reverse-sorted input is the worst case, requiring n(n−1)/2 comparisons and shifts, consistent with **O(n²)**. Random input also showed quadratic-like work. On random input at n = 5,000, merge sort took 0.008102 s versus 0.749601 s for insertion sort in this run. Merge sort has **O(n log n)** time in best, average, and worst cases, but uses additional memory; insertion sort is in-place and can be excellent for small or nearly sorted arrays.

## Conclusion
The experiment supports the theoretical analysis: insertion sort is efficient for already sorted or small inputs but scales poorly on reverse-sorted and random large inputs. Merge sort was substantially faster on the 5,000-element random input in this environment. Exact timings depend on hardware and system load; the CSV and plots provide the complete measurements.

## References
1. Cormen, Leiserson, Rivest, and Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022.
2. Python documentation, `time.perf_counter()`: https://docs.python.org/3/library/time.html#time.perf_counter

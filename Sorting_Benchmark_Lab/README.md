# Sorting Benchmark Lab

Compares Insertion Sort, Merge Sort, Quick Sort, and Python `sorted()` on sorted, reversed, and random lists of 1,000, 10,000, and 100,000 integers.

## Windows 11 (PowerShell)

1. Install Python 3.10+ from python.org, selecting **Add Python to PATH**.
2. Open PowerShell in this project folder.
3. Install dependency: `py -m pip install -r requirements.txt`
4. Test correctness: `py src/test_sorts.py`
5. Run full benchmark: `py src/benchmark.py`

The full benchmark includes insertion sort at n=100,000, which may take **several minutes or longer** on reversed/random data. Do not interrupt if you need all cases. For a faster demonstration: `py src/benchmark.py --sizes 1000 10000 --max-insertion-n 10000` (this overwrites existing timings.csv and charts; preserve original results first).

Outputs: `results/timings.csv` (one row per timed run; seconds measured by `time.perf_counter`) and `charts/*.png`. Inputs are generated deterministically from seed 42; random inputs include possible duplicate values. All four algorithms receive identical input values for each case. A fresh list is created inside each sorting function and included in its timed cost. Results are machine-dependent. Set `--repeats 3` for repeated measurements; charts then show mean time.

## Notes

The supplied image specifies four algorithms, three input patterns, sizes from 10^3 to 10^5, and Python/time.perf_counter/matplotlib. No extra requirements or page limit were visible. The report records actual runs only. This implementation uses median-of-three, 3-way partition quicksort rather than a naive first-element pivot, to avoid pathologically slow sorted inputs.

## Included experiment caveat
The supplied results were collected in two completed benchmark runs (see run_log.txt and run_large_log.txt). The full default benchmark was attempted but timed out during reversed insertion sort at n=100,000. The included 30-row CSV combines the completed runs; its times are rounded to six decimals from logs. Run the full command on your own machine to produce all 36 measurements and a fully complete report dataset.

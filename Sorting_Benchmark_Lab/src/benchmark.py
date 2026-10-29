"""Reproducible sorting benchmark. Run from project root: python src/benchmark.py"""
import argparse
import csv
import random
import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def insertion_sort(items):
    a = items.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(items):
    a = items.copy()
    def sort(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        sort(lo, mid)
        sort(mid, hi)
        left = a[lo:mid]
        right = a[mid:hi]
        i = j = 0
        for k in range(lo, hi):
            if j == len(right) or (i < len(left) and left[i] <= right[j]):
                a[k] = left[i]
                i += 1
            else:
                a[k] = right[j]
                j += 1
    sort(0, len(a))
    return a


def quick_sort(items):
    """Iterative 3-way quicksort with median-of-three pivot; handles duplicates."""
    a = items.copy()
    stack = [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        while lo < hi:
            mid = (lo + hi) // 2
            pivot = sorted((a[lo], a[mid], a[hi]))[1]
            lt, i, gt = lo, lo, hi
            while i <= gt:
                if a[i] < pivot:
                    a[lt], a[i] = a[i], a[lt]
                    lt += 1
                    i += 1
                elif a[i] > pivot:
                    a[i], a[gt] = a[gt], a[i]
                    gt -= 1
                else:
                    i += 1
            # Process smaller partition immediately to limit stack growth.
            if lt - lo < hi - gt:
                if gt + 1 < hi:
                    stack.append((gt + 1, hi))
                hi = lt - 1
            else:
                if lo < lt - 1:
                    stack.append((lo, lt - 1))
                lo = gt + 1
    return a


ALGORITHMS = {'Insertion Sort': insertion_sort, 'Merge Sort': merge_sort,
              'Quick Sort': quick_sort, 'Python sorted()': sorted}


def make_data(n, kind, seed):
    if kind == 'Sorted':
        return list(range(n))
    if kind == 'Reversed':
        return list(range(n - 1, -1, -1))
    rng = random.Random(seed)
    return [rng.randrange(n * 10) for _ in range(n)]


def plot_results(rows, charts_dir):
    for kind in ('Sorted', 'Reversed', 'Random'):
        fig, ax = plt.subplots(figsize=(9, 5.5))
        for name in ALGORITHMS:
            subset = sorted((r for r in rows if r['data_type'] == kind and r['algorithm'] == name),
                            key=lambda r: int(r['n']))
            ax.plot([int(r['n']) for r in subset], [float(r['seconds']) for r in subset],
                    marker='o', label=name)
        ax.set(xlabel='Number of elements (n)', ylabel='Execution time (seconds)',
               title=f'Sorting Benchmark — {kind} Data')
        ax.set_xscale('log')
        ax.set_yscale('symlog', linthresh=0.00001)
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig(charts_dir / f'{kind.lower()}.png', dpi=170)
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description='Compare four sorting algorithms on three input patterns.')
    parser.add_argument('--sizes', type=int, nargs='+', default=[1000, 10000, 100000])
    parser.add_argument('--repeats', type=int, default=1)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--max-insertion-n', type=int, default=100000,
                        help='Skip insertion sort above this size (default includes all required sizes).')
    args = parser.parse_args()
    if any(n < 1 for n in args.sizes) or args.repeats < 1:
        parser.error('sizes and repeats must be positive')
    results_dir, charts_dir = ROOT / 'results', ROOT / 'charts'
    results_dir.mkdir(exist_ok=True)
    charts_dir.mkdir(exist_ok=True)
    rows = []
    for kind in ('Sorted', 'Reversed', 'Random'):
        for n in args.sizes:
            data = make_data(n, kind, args.seed)
            expected = sorted(data)
            for name, algorithm in ALGORITHMS.items():
                if name == 'Insertion Sort' and n > args.max_insertion_n:
                    continue
                for trial in range(1, args.repeats + 1):
                    start = time.perf_counter()
                    actual = algorithm(data)
                    elapsed = time.perf_counter() - start
                    if actual != expected:
                        raise AssertionError(f'Incorrect result: {name}, {kind}, {n}')
                    rows.append({'data_type': kind, 'n': n, 'algorithm': name,
                                 'trial': trial, 'seconds': f'{elapsed:.9f}',
                                 'correct': 'True'})
                    print(f'{kind:8s} n={n:6d} {name:16s} {elapsed:.6f}s', flush=True)
    with (results_dir / 'timings.csv').open('w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['data_type', 'n', 'algorithm', 'trial', 'seconds', 'correct'])
        writer.writeheader()
        writer.writerows(rows)
    # Average repeats for charting, if repeats > 1.
    grouped = {}
    for row in rows:
        key = row['data_type'], row['n'], row['algorithm']
        grouped.setdefault(key, []).append(float(row['seconds']))
    means = [{'data_type': k[0], 'n': k[1], 'algorithm': k[2],
              'seconds': sum(values) / len(values)} for k, values in grouped.items()]
    plot_results(means, charts_dir)
    print(f'Wrote {len(rows)} verified measurements to {results_dir / "timings.csv"}')


if __name__ == '__main__':
    main()

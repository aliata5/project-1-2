"""Run empirical sorting experiments and write CSV results and plots."""
from __future__ import annotations

import csv
import random
import statistics
import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.sorting import insertion_sort, merge_sort

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
PLOTS = ROOT / "plots"
SIZES = [100, 250, 500, 1000, 2000, 3000, 4000, 5000]
REPEATS = 3
SEED = 20261029


def timed_call(function, data):
    start = time.perf_counter()
    result = function(data)
    elapsed = time.perf_counter() - start
    return result, elapsed


def main():
    RESULTS.mkdir(exist_ok=True)
    PLOTS.mkdir(exist_ok=True)
    rng = random.Random(SEED)
    rows = []

    for n in SIZES:
        base_random = [rng.randrange(0, 10 * n + 1) for _ in range(n)]
        datasets = {
            "sorted": list(range(n)),
            "reverse_sorted": list(range(n, 0, -1)),
            "random": base_random,
        }
        for case, data in datasets.items():
            # Insertion sort: repeat timing on fresh copies; operation counts are deterministic.
            insertion_times = []
            expected = sorted(data)
            comparisons = shifts = None
            for _ in range(REPEATS):
                sort_result, elapsed = timed_call(insertion_sort, data)
                sorted_values = sort_result[0]
                if sorted_values != expected:
                    raise AssertionError(f"Insertion sort failed for n={n}, case={case}")
                insertion_times.append(elapsed)
                # Count metrics are recomputed from the same deterministic input.
                _, comparisons, shifts = insertion_sort(data)
            rows.append({
                "algorithm": "Insertion Sort",
                "input_case": case,
                "n": n,
                "median_time_seconds": statistics.median(insertion_times),
                "comparisons": comparisons,
                "shifts": shifts,
                "repeats": REPEATS,
            })

            merge_times = []
            for _ in range(REPEATS):
                sorted_values, elapsed = timed_call(merge_sort, data)
                if sorted_values != expected:
                    raise AssertionError(f"Merge sort failed for n={n}, case={case}")
                merge_times.append(elapsed)
            rows.append({
                "algorithm": "Merge Sort",
                "input_case": case,
                "n": n,
                "median_time_seconds": statistics.median(merge_times),
                "comparisons": "",
                "shifts": "",
                "repeats": REPEATS,
            })

    csv_path = RESULTS / "benchmark_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "algorithm", "input_case", "n", "median_time_seconds",
            "comparisons", "shifts", "repeats"
        ])
        writer.writeheader()
        writer.writerows(rows)

    make_plots(rows)
    write_summary(rows)
    print(f"Completed experiments: {len(rows)} result rows")
    print(f"CSV: {csv_path}")
    print(f"Plots: {PLOTS}")
    print(f"Summary: {RESULTS / 'summary.txt'}")


def make_plots(rows):
    # Plot insertion sort timing by input arrangement and merge sort for context.
    fig, ax = plt.subplots(figsize=(9, 5.5))
    styles = {
        ("Insertion Sort", "sorted"): ("Insertion Sort — sorted", "o-"),
        ("Insertion Sort", "reverse_sorted"): ("Insertion Sort — reverse-sorted", "s-"),
        ("Insertion Sort", "random"): ("Insertion Sort — random", "^-"),
        ("Merge Sort", "random"): ("Merge Sort — random", "d--"),
    }
    for key, (label, style) in styles.items():
        subset = sorted(
            [r for r in rows if (r["algorithm"], r["input_case"]) == key],
            key=lambda r: r["n"]
        )
        ax.plot([r["n"] for r in subset],
                [r["median_time_seconds"] for r in subset],
                style, label=label, linewidth=1.8, markersize=4)
    ax.set_title("Empirical Sorting Runtime")
    ax.set_xlabel("Input size (n)")
    ax.set_ylabel("Median runtime (seconds)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(PLOTS / "runtime_comparison.png", dpi=180)
    plt.close(fig)

    # Normalize theoretical growth curves to make shape comparison meaningful.
    sizes = SIZES
    linear = [n / sizes[-1] for n in sizes]
    quadratic = [(n / sizes[-1]) ** 2 for n in sizes]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    for case, label, marker in [
        ("sorted", "Insertion Sort — sorted input", "o"),
        ("reverse_sorted", "Insertion Sort — reverse-sorted input", "s"),
        ("random", "Insertion Sort — random input", "^"),
    ]:
        subset = sorted(
            [r for r in rows if r["algorithm"] == "Insertion Sort" and r["input_case"] == case],
            key=lambda r: r["n"]
        )
        times = [r["median_time_seconds"] for r in subset]
        # Scale each measured curve by its own final point; shape is what is compared.
        normalized = [t / times[-1] if times[-1] else 0 for t in times]
        ax.plot([r["n"] for r in subset], normalized, marker + "-", label=label)
    ax.plot(sizes, linear, "k--", label="Reference growth: O(n), normalized")
    ax.plot(sizes, quadratic, "k:", label="Reference growth: O(n²), normalized")
    ax.set_title("Insertion Sort: Measured vs Theoretical Growth")
    ax.set_xlabel("Input size (n)")
    ax.set_ylabel("Normalized runtime / growth")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(PLOTS / "growth_analysis.png", dpi=180)
    plt.close(fig)


def write_summary(rows):
    def get(algorithm, case, n):
        return next(r for r in rows if r["algorithm"] == algorithm
                    and r["input_case"] == case and r["n"] == n)
    lines = [
        "Empirical experiment summary",
        f"Input sizes: {', '.join(map(str, SIZES))}",
        f"Timing repetitions per algorithm/case/size: {REPEATS}; reported value: median",
        f"Random seed: {SEED}",
        "",
        "Insertion sort operation counts at n=5000:",
    ]
    for case in ("sorted", "reverse_sorted", "random"):
        r = get("Insertion Sort", case, 5000)
        lines.append(f"- {case}: comparisons={r['comparisons']}, shifts={r['shifts']}")
    lines += [
        "",
        "Observed runtime at n=5000 (seconds):",
    ]
    for algorithm, case in [
        ("Insertion Sort", "sorted"),
        ("Insertion Sort", "reverse_sorted"),
        ("Insertion Sort", "random"),
        ("Merge Sort", "random"),
    ]:
        r = get(algorithm, case, 5000)
        lines.append(f"- {algorithm}, {case}: {r['median_time_seconds']:.8f}")
    lines += [
        "",
        "Interpretation: sorted input is the best case for insertion sort and typically grows linearly.",
        "Reverse-sorted input is its worst case; random input is expected to show quadratic growth.",
        "Merge sort is included as an empirical comparison on random inputs and has O(n log n) time complexity.",
        "Wall-clock timings depend on the machine, Python version, and system load; use the CSV for exact measurements.",
    ]
    (RESULTS / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

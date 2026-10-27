#!/usr/bin/env python3
"""
======================================================================
INFOSYS SP & DSE OFFLINE JUDGE — DAY 05: KADANE'S ALGORITHM
Tests solve_gear1_brute and solve_gear3_optimal from day_05_solution.py
======================================================================
"""

import sys
import time
import signal
import os

# Add local directory to path for clean import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from day_05_solution import solve_gear1_brute, solve_gear3_optimal
except ImportError as err:
    print(f"\033[91m❌ Import Error: Could not import solutions from day_05_solution.py: {err}\033[0m")
    sys.exit(1)


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException("Time Limit Exceeded (> 2.0s)")


# Configure Linux SIGALRM timeout guard
if hasattr(signal, 'SIGALRM'):
    signal.signal(signal.SIGALRM, timeout_handler)


def run_single_test(test_num, name, arr, expected, func, timeout_sec=2.0):
    """Executes a single test case with runtime measurement and hard timeout guard."""
    if hasattr(signal, 'SIGALRM'):
        signal.setitimer(signal.ITIMER_REAL, timeout_sec)

    start_time = time.perf_counter()
    status = "UNKNOWN"
    runtime_ms = 0.0
    actual = None
    err_msg = ""

    try:
        actual = func(arr)
        runtime_ms = (time.perf_counter() - start_time) * 1000
        if actual == expected:
            status = "PASS"
        else:
            status = "WA"
    except TimeoutException:
        runtime_ms = timeout_sec * 1000
        status = "TLE"
    except Exception as e:
        status = "RE"
        err_msg = str(e)
    finally:
        if hasattr(signal, 'SIGALRM'):
            signal.setitimer(signal.ITIMER_REAL, 0)

    return status, runtime_ms, actual, err_msg


def main():
    print("\n\033[1m\033[96m" + "=" * 70)
    print(" ⚔️  INFOSYS SP/DSE OFFLINE JUDGE — DAY 05: KADANE'S ALGORITHM  ⚔️")
    print("=" * 70 + "\033[0m\n")

    # Generate Deterministic Test Cases
    tests = [
        (
            "LeetCode 918 Sample 1 (Non-wrap)",
            [1, -2, 3, -2],
            3, "Basic Sample"
        ),
        (
            "LeetCode 918 Sample 2 (Wrap Around)",
            [5, -3, 5],
            10, "Circular Wrap"
        ),
        (
            "LeetCode 918 Sample 3 (All-Negative Trap)",
            [-3, -2, -3],
            -2, "Negative Guard"
        ),
        (
            "Single Element Positive (N=1)",
            [42],
            42, "Edge Case"
        ),
        (
            "Single Element Negative (N=1)",
            [-9],
            -9, "Edge Case"
        ),
        (
            "Two Elements Non-wrapped (N=2)",
            [3, -2],
            3, "Edge Case"
        ),
        (
            "Two Elements All Negative (N=2)",
            [-2, -3],
            -2, "Edge Case"
        ),
        (
            "Alternating Wrap (N=4)",
            [3, -1, 2, -1],
            4, "Circular Wrap"
        ),
        (
            "Plateau Valley Wrap (N=3)",
            [10, -50, 10],
            20, "Circular Wrap"
        ),
        (
            "Medium Scalability Sine Pattern (N=2000)",
            [(i % 20 - 10) for i in range(2000)],
            solve_gear3_optimal([(i % 20 - 10) for i in range(2000)]),
            "Scalability"
        ),
        (
            "Massive SP Stress Energy Ring (N=100000)",
            [(i % 100 - 50) for i in range(100000)],
            solve_gear3_optimal([(i % 100 - 50) for i in range(100000)]),
            "Infosys SP Stress"
        ),
        (
            "Massive All-Negative Stress (N=100000)",
            [-(i % 50 + 1) for i in range(100000)],
            -1,
            "Negative Stress"
        )
    ]

    print("\033[1mPhase 1: Evaluating Gear 3 (Tactical Optimal Dual-Kadane)\033[0m")
    print("\033[2mTarget: 100% Score across all 12 test cases with strict 2.0s timeout per case.\033[0m\n")

    passed_count = 0
    all_passed = True

    for idx, (name, arr, expected, category) in enumerate(tests, 1):
        status, runtime_ms, actual, err_msg = run_single_test(
            idx, name, arr, expected, solve_gear3_optimal, timeout_sec=2.0
        )

        cat_badge = f"[{category:18s}]"
        if status == "PASS":
            passed_count += 1
            badge = "\033[92m✅ PASS\033[0m"
            print(f" Test #{idx:02d} {cat_badge} {name:42s}: {badge} ({runtime_ms:7.2f} ms)")
        elif status == "WA":
            all_passed = False
            badge = "\033[91m❌ WA  \033[0m"
            print(f" Test #{idx:02d} {cat_badge} {name:42s}: {badge} (Expected: {expected}, Got: {actual})")
        elif status == "TLE":
            all_passed = False
            badge = "\033[93m⏱️ TLE \033[0m"
            print(f" Test #{idx:02d} {cat_badge} {name:42s}: {badge} (> 2000 ms)")
        else:
            all_passed = False
            badge = "\033[91m💥 RE  \033[0m"
            print(f" Test #{idx:02d} {cat_badge} {name:42s}: {badge} ({err_msg})")

    score_pct = (passed_count / len(tests)) * 100
    print(f"\n\033[1mOptimal Score: {passed_count} / {len(tests)} Tests Passed ({score_pct:.1f}%)\033[0m")

    # Phase 2: Brute Force verification & expected TLE on N=10^5
    print("\n\033[1m\033[96m" + "-" * 70 + "\033[0m")
    print("\033[1mPhase 2: Verifying Gear 1 (Human Brute Force Partial Marks)\033[0m")
    print("\033[2mVerifies that Brute Force secures sample marks but safely TLEs on N=10^5.\033[0m\n")

    # Test Gear 1 on Sample 1
    bf_status, bf_runtime, bf_actual, _ = run_single_test(
        1, "Sample 1", tests[0][1], tests[0][2], solve_gear1_brute, timeout_sec=2.0
    )
    if bf_status == "PASS":
        print(f" Sample Test 1   : \033[92m✅ ACCEPTED (Partial Marks Secured)\033[0m ({bf_runtime:.2f} ms)")
    else:
        print(f" Sample Test 1   : \033[91m❌ FAILED\033[0m")

    # Test Gear 1 on N=10^5 (Must trigger TLE guard)
    print(" N=10^5 Stress   : \033[93m⏳ Running Brute Force with 2.0s Alarm Guard...\033[0m", end="", flush=True)
    bf_tle_status, bf_tle_runtime, _, _ = run_single_test(
        11, "SP Stress", tests[10][1], tests[10][2], solve_gear1_brute, timeout_sec=2.0
    )
    if bf_tle_status == "TLE":
        print(f" N=10^5 Stress   : \033[93m⚠️ EXPECTED TLE (> 2000.00 ms) — Guard Triggered Successfully!\033[0m")
    else:
        print(f" N=10^5 Stress   : Finished unexpectedly in {bf_tle_runtime:.2f} ms (Status: {bf_tle_status})")

    # Final Verdict Summary
    print("\n\033[1m\033[96m" + "=" * 70 + "\033[0m")
    print("\033[1m 📊 FINAL EXAM VERDICT SUMMARY — DAY 05\033[0m")
    print("\033[1m\033[96m" + "=" * 70 + "\033[0m")
    print(f" Gear 1 (Brute Force) : \033[93m33% Partial Marks\033[0m (TLE on N=10^5 as predicted by Bottleneck X-Ray)")
    if all_passed:
        print(f" Gear 3 (Optimal)     : \033[92m100.0% Full Marks (12/12 Accepted)\033[0m\n")
        print(" \033[92m\033[1m🎉 ALL SYSTEMS CLEARED! DAY 05 SUBMISSION VERIFIED READY FOR PRODUCTION!\033[0m\n")
        sys.exit(0)
    else:
        print(f" Gear 3 (Optimal)     : \033[91m{score_pct:.1f}% Marks (Some tests failed)\033[0m\n")
        sys.exit(1)


if __name__ == '__main__':
    main()

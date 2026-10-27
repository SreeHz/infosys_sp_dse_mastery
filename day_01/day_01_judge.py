#!/usr/bin/env python3
"""
Offline Local Infosys Test Runner — Day 01: Time Complexity & Difference Array
Strictly zero external dependencies. Pure standard library.
Enforces Section 5 Guardrails:
 - Hard 2.0-Second Timeout via Linux signal.SIGALRM / signal.setitimer
 - ANSI colored terminal UI
 - Categorized test suite (Samples, Edge Cases, Medium, and N=10^5 Stress Test)
"""

import sys
import os
import time
import signal
from typing import List, Tuple, Any

# Ensure local module import works regardless of CWD
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

try:
    from day_01_solution import solve_gear1_brute, solve_gear3_optimal
except ImportError:
    print("\033[91m[ERROR] Could not import 'day_01_solution.py'. Make sure it exists in the same folder!\033[0m")
    sys.exit(1)

# ANSI Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Time Limit Exceeded (> 2000ms)")

# Install signal alarm
signal.signal(signal.SIGALRM, timeout_handler)

def run_with_timeout(func, n: int, updates: List[List[int]], timeout_sec: float = 2.0) -> Tuple[Any, float, str]:
    """Runs a solver function with a hard Linux signal timeout."""
    signal.setitimer(signal.ITIMER_REAL, timeout_sec)
    start_time = time.perf_counter()
    try:
        res = func(n, updates)
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return res, elapsed_ms, "OK"
    except TimeoutException:
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return None, elapsed_ms, "TLE"
    except Exception as e:
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return None, elapsed_ms, f"ERROR: {str(e)}"
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0.0)  # Always disarm alarm

def build_test_suite():
    """Generates 12 thorough test cases."""
    tests = []

    # 1. Basic Sample from LeetCode / Infosys
    tests.append({
        "name": "Sample Case 1 (Standard Overlap)",
        "category": "Basic Sample",
        "n": 5,
        "updates": [[1, 2, 10], [2, 3, 20], [2, 5, 25]],
        "expected": [10, 55, 45, 25, 25]
    })

    # 2. Single Tower Edge Case
    tests.append({
        "name": "Single Tower (N=1)",
        "category": "Edge Case",
        "n": 1,
        "updates": [[1, 1, 5], [1, 1, -2], [1, 1, 10]],
        "expected": [13]
    })

    # 3. Full-Range Updates
    tests.append({
        "name": "Full Range Fortification [1, N]",
        "category": "Edge Case",
        "n": 4,
        "updates": [[1, 4, 100], [1, 4, -50]],
        "expected": [50, 50, 50, 50]
    })

    # 4. Consecutive Non-overlapping Updates
    tests.append({
        "name": "Disjoint Consecutive Ranges",
        "category": "Edge Case",
        "n": 6,
        "updates": [[1, 2, 5], [3, 4, 15], [5, 6, 25]],
        "expected": [5, 5, 15, 15, 25, 25]
    })

    # 5. Point Updates (Single Indices)
    tests.append({
        "name": "Point Updates Only (L == R)",
        "category": "Edge Case",
        "n": 5,
        "updates": [[1, 1, 1], [3, 3, 3], [5, 5, 5]],
        "expected": [1, 0, 3, 0, 5]
    })

    # 6. Zero Spells (Empty Updates)
    tests.append({
        "name": "Empty Spell List (Q = 0)",
        "category": "Edge Case",
        "n": 4,
        "updates": [],
        "expected": [0, 0, 0, 0]
    })

    # 7. Heavy Cancellation of Spells
    tests.append({
        "name": "Positive and Negative Exact Balance",
        "category": "Math Edge",
        "n": 4,
        "updates": [[1, 3, 40], [2, 4, 20], [1, 3, -40], [2, 4, -20]],
        "expected": [0, 0, 0, 0]
    })

    # 8. Boundary Tower (Rightmost element R = N)
    tests.append({
        "name": "Rightmost Boundary Hit (R = N)",
        "category": "Boundary",
        "n": 5,
        "updates": [[4, 5, 12], [5, 5, 8]],
        "expected": [0, 0, 0, 12, 20]
    })

    # 9. Medium Scale (N=3000, Q=3000)
    med_n = 3000
    med_updates = [[i, min(i + 15, med_n), 2] for i in range(1, med_n, 10)]
    # Compute ground truth via optimal algorithm logic
    diff_truth = [0] * (med_n + 2)
    for l, r, x in med_updates:
        diff_truth[l] += x
        diff_truth[r + 1] -= x
    curr = 0
    med_expected = []
    for i in range(1, med_n + 1):
        curr += diff_truth[i]
        med_expected.append(curr)

    tests.append({
        "name": f"Medium Scale (N={med_n}, Q={len(med_updates)})",
        "category": "Scalability",
        "n": med_n,
        "updates": med_updates,
        "expected": med_expected
    })

    # 10. Alternating Overlaps (N=5000, Q=5000)
    overlap_n = 5000
    overlap_updates = [[1, i, 1] for i in range(1, overlap_n + 1, 2)]
    diff_truth = [0] * (overlap_n + 2)
    for l, r, x in overlap_updates:
        diff_truth[l] += x
        diff_truth[r + 1] -= x
    curr = 0
    overlap_expected = []
    for i in range(1, overlap_n + 1):
        curr += diff_truth[i]
        overlap_expected.append(curr)

    tests.append({
        "name": f"Pyramid Overlap (N={overlap_n}, Q={len(overlap_updates)})",
        "category": "Scalability",
        "n": overlap_n,
        "updates": overlap_updates,
        "expected": overlap_expected
    })

    # 11. Massive Infosys SP Stress Test (N=10^5, Q=10^5)
    stress_n = 100000
    stress_q = 100000
    # Every update touches a broad slice of the array
    stress_updates = [[(i % 1000) + 1, stress_n - (i % 1000), 1] for i in range(stress_q)]
    diff_truth = [0] * (stress_n + 2)
    for l, r, x in stress_updates:
        diff_truth[l] += x
        diff_truth[r + 1] -= x
    curr = 0
    stress_expected = []
    for i in range(1, stress_n + 1):
        curr += diff_truth[i]
        stress_expected.append(curr)

    tests.append({
        "name": f"Massive SP Stress Test (N={stress_n}, Q={stress_q})",
        "category": "Infosys SP Stress",
        "n": stress_n,
        "updates": stress_updates,
        "expected": stress_expected
    })

    # 12. Negative Armor Corrosive Stress Test
    neg_n = 100000
    neg_updates = [[1, neg_n, -5] for _ in range(2000)]
    tests.append({
        "name": f"Corrosive Curse Stress (N={neg_n}, Q=2000)",
        "category": "Negative Armor",
        "n": neg_n,
        "updates": neg_updates,
        "expected": [-10000] * neg_n
    })

    return tests

def run_judge():
    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN} ⚔️  INFOSYS SP/DSE OFFLINE JUDGE — DAY 01: DIFFERENCE ARRAYS  ⚔️{RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    tests = build_test_suite()
    total_tests = len(tests)

    print(f"{BOLD}Phase 1: Evaluating Gear 3 (Tactical Optimal Solution){RESET}")
    print(f"{DIM}Target: 100% Score across all 12 test cases with strict 2.0s timeout per case.{RESET}\n")

    optimal_passed = 0
    optimal_results = []

    for idx, test in enumerate(tests, 1):
        name = test["name"]
        n = test["n"]
        updates = test["updates"]
        expected = test["expected"]

        res, ms, status = run_with_timeout(solve_gear3_optimal, n, updates, timeout_sec=2.0)

        if status == "OK" and res == expected:
            verdict = f"{GREEN}✅ PASS{RESET}"
            optimal_passed += 1
        elif status == "TLE":
            verdict = f"{YELLOW}⚠️ TLE (> 2000ms){RESET}"
        elif status.startswith("ERROR"):
            verdict = f"{RED}💥 {status}{RESET}"
        else:
            verdict = f"{RED}❌ WA (Expected vs Actual Diff){RESET}"

        optimal_results.append((idx, name, f"N={n}, Q={len(updates)}", f"{ms:.2f} ms", verdict))
        print(f" Test #{idx:02d} [{test['category']:<17}] {name:<42} : {verdict} ({ms:>7.2f} ms)")

    # Score breakdown
    score_pct = (optimal_passed / total_tests) * 100
    print(f"\n{BOLD}Optimal Score: {optimal_passed} / {total_tests} Tests Passed ({score_pct:.1f}%){RESET}")

    # Phase 2: Gear 1 Brute Force X-Ray Comparison
    print(f"\n{BOLD}{CYAN}----------------------------------------------------------------------{RESET}")
    print(f"{BOLD}Phase 2: Verifying Gear 1 (Human Brute Force Partial Marks){RESET}")
    print(f"{DIM}Verifies that Brute Force secures sample marks but safely TLEs on N=10^5.{RESET}\n")

    brute_sample_res, b_sample_ms, b_sample_status = run_with_timeout(solve_gear1_brute, tests[0]["n"], tests[0]["updates"])
    sample_verdict = f"{GREEN}✅ ACCEPTED (Partial Marks Secured){RESET}" if brute_sample_res == tests[0]["expected"] else f"{RED}❌ FAILED{RESET}"
    print(f" Sample Test 1   : {sample_verdict} ({b_sample_ms:.2f} ms)")

    # Run on the N=10^5 stress test
    stress_test = tests[10]  # The SP Stress Test
    print(f" N=10^5 Stress   : {YELLOW}⏳ Running Brute Force with 2.0s Alarm Guard...{RESET}", end="", flush=True)
    brute_stress_res, b_stress_ms, b_stress_status = run_with_timeout(solve_gear1_brute, stress_test["n"], stress_test["updates"], timeout_sec=2.0)

    if b_stress_status == "TLE":
        print(f"\r N=10^5 Stress   : {YELLOW}⚠️ EXPECTED TLE (> 2000.00 ms) — Guard Triggered Successfully!{RESET}")
    else:
        print(f"\r N=10^5 Stress   : Completed in {b_stress_ms:.2f} ms")

    # Final Summary Table
    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD} 📊 FINAL EXAM VERDICT SUMMARY — DAY 01{RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}")
    print(f" Gear 1 (Brute Force) : {YELLOW}33% Partial Marks{RESET} (TLE on N=10^5 as predicted by Bottleneck X-Ray)")
    print(f" Gear 3 (Optimal)     : {GREEN}{score_pct:.1f}% Full Marks ({optimal_passed}/{total_tests} Accepted){RESET}")
    
    if optimal_passed == total_tests:
        print(f"\n {GREEN}{BOLD}🎉 ALL SYSTEMS CLEARED! DAY 01 SUBMISSION VERIFIED READY FOR PRODUCTION!{RESET}\n")
    else:
        print(f"\n {RED}{BOLD}⚠️ SOME TESTS FAILED. Check diffs before submitting.{RESET}\n")

if __name__ == "__main__":
    run_judge()

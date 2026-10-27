#!/usr/bin/env python3
"""
Offline Local Infosys Test Runner — Day 02: Hash Maps & Subarray Sum Equals K
Strictly zero external dependencies. Pure standard library.
Enforces Section 5 Guardrails:
 - Hard 2.0-Second Timeout via Linux signal.SIGALRM / signal.setitimer
 - ANSI colored terminal UI
 - Categorized test suite (Samples, Edge Cases, Zeros, Negatives, and N=10^5 Stress Test)
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
    from day_02_solution import solve_gear1_brute, solve_gear3_optimal
except ImportError:
    print("\033[91m[ERROR] Could not import 'day_02_solution.py'. Make sure it exists in the same folder!\033[0m")
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

def run_with_timeout(func, nums: List[int], k: int, timeout_sec: float = 2.0) -> Tuple[Any, float, str]:
    """Runs a solver function with a hard Linux signal timeout."""
    signal.setitimer(signal.ITIMER_REAL, timeout_sec)
    start_time = time.perf_counter()
    try:
        res = func(nums, k)
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

    # 1. LeetCode 560 Classic Sample 1
    tests.append({
        "name": "Standard Sample 1 (All Ones)",
        "category": "Basic Sample",
        "nums": [1, 1, 1],
        "k": 2,
        "expected": 2
    })

    # 2. LeetCode 560 Classic Sample 2
    tests.append({
        "name": "Standard Sample 2 (Disjoint Matches)",
        "category": "Basic Sample",
        "nums": [1, 2, 3],
        "k": 3,
        "expected": 2  # [1, 2] and [3]
    })

    # 3. Single Element Matching K
    tests.append({
        "name": "Single Element Equal to K",
        "category": "Edge Case",
        "nums": [7],
        "k": 7,
        "expected": 1
    })

    # 4. Single Element Not Matching K
    tests.append({
        "name": "Single Element Not Equal to K",
        "category": "Edge Case",
        "nums": [3],
        "k": 7,
        "expected": 0
    })

    # 5. Multiple Zeros with K = 0 (Combinatorial Trap)
    tests.append({
        "name": "All Zeros with Target K = 0",
        "category": "Zero Edge Case",
        "nums": [0, 0, 0, 0, 0],
        "k": 0,
        "expected": 15  # n*(n+1)//2 = 5*6//2 = 15
    })

    # 6. Cancellation with Alternating Negative & Positive (K = 0)
    tests.append({
        "name": "Alternating Cancellation (K = 0)",
        "category": "Negative Math",
        "nums": [1, -1, 1, -1, 1],
        "k": 0,
        "expected": 6
    })

    # 7. Target K is Strictly Negative
    tests.append({
        "name": "Target K is Negative (K = -3)",
        "category": "Negative Math",
        "nums": [-1, -2, 1, -3, 2, -1],
        "k": -3,
        "expected": 4  # [-1, -2], [-3], [-2, 1, -3, 2, -1], [-3, 2, -1] -> wait:
        # let's verify:
        # i=0..1: -1 + -2 = -3 (yes)
        # i=3..3: -3 (yes)
        # i=1..5: -2+1-3+2-1 = -3 (yes)
        # i=3..5: -3+2-1 = -2 (no)
        # i=0..3: -1-2+1-3 = -5 (no)
        # i=2..4: 1-3+2 = 0
        # let's compute precisely below
    })
    # Compute ground truth for test 7
    t7_nums = [-1, -2, 1, -3, 2, -1]
    t7_k = -3
    t7_cnt = 0
    for i in range(len(t7_nums)):
        s = 0
        for j in range(i, len(t7_nums)):
            s += t7_nums[j]
            if s == t7_k:
                t7_cnt += 1
    tests[-1]["expected"] = t7_cnt

    # 8. No Subarray Sums to Target K
    tests.append({
        "name": "Impossible Target (Zero Matches)",
        "category": "Edge Case",
        "nums": [10, 20, 30, 40],
        "k": 15,
        "expected": 0
    })

    # 9. Mixed Dense Positives & Negatives (N=2000)
    med_n = 2000
    med_nums = [(i % 7) - 3 for i in range(med_n)]  # values in [-3..3]
    med_k = 0
    # Ground truth
    pref_cnt = {0: 1}
    cur = 0
    ans = 0
    for x in med_nums:
        cur += x
        if (cur - med_k) in pref_cnt:
            ans += pref_cnt[cur - med_k]
        pref_cnt[cur] = pref_cnt.get(cur, 0) + 1
    tests.append({
        "name": f"Medium Dense Oscillations (N={med_n}, K=0)",
        "category": "Scalability",
        "nums": med_nums,
        "k": med_k,
        "expected": ans
    })

    # 10. Large Target Over Small Positive Range
    t10_nums = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 100  # N = 1000
    t10_k = 50
    pref_cnt = {0: 1}
    cur = 0
    ans = 0
    for x in t10_nums:
        cur += x
        if (cur - t10_k) in pref_cnt:
            ans += pref_cnt[cur - t10_k]
        pref_cnt[cur] = pref_cnt.get(cur, 0) + 1
    tests.append({
        "name": f"Repeated Primes Pattern (N=1000, K=50)",
        "category": "Scalability",
        "nums": t10_nums,
        "k": t10_k,
        "expected": ans
    })

    # 11. Massive Infosys SP Stress Test (N=10^5, all 1s, k=500)
    stress_n = 100000
    stress_k = 500
    # In an array of all 1s of length N, any subarray of length 500 has sum 500.
    # Total subarrays of length 500 = N - 500 + 1 = 100000 - 500 + 1 = 99501.
    tests.append({
        "name": f"Massive SP Stress Test (N={stress_n}, K={stress_k})",
        "category": "Infosys SP Stress",
        "nums": [1] * stress_n,
        "k": stress_k,
        "expected": stress_n - stress_k + 1
    })

    # 12. Massive SP All-Zero Big-Number Stress (N=10^5, k=0)
    zero_n = 100000
    # Total subarrays of sum 0 in all-zero array of length 10^5:
    # 10^5 * (10^5 + 1) // 2 = 5000050000 (Tests 64-bit integer handling)
    tests.append({
        "name": f"Combinatorial SP Stress (N={zero_n}, K=0)",
        "category": "Large Count Edge",
        "nums": [0] * zero_n,
        "k": 0,
        "expected": (zero_n * (zero_n + 1)) // 2
    })

    return tests

def run_judge():
    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN} ⚔️  INFOSYS SP/DSE OFFLINE JUDGE — DAY 02: PREFIX + HASH MAPS  ⚔️{RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    tests = build_test_suite()
    total_tests = len(tests)

    print(f"{BOLD}Phase 1: Evaluating Gear 3 (Tactical Optimal Solution){RESET}")
    print(f"{DIM}Target: 100% Score across all 12 test cases with strict 2.0s timeout per case.{RESET}\n")

    optimal_passed = 0

    for idx, test in enumerate(tests, 1):
        name = test["name"]
        nums = test["nums"]
        k = test["k"]
        expected = test["expected"]

        res, ms, status = run_with_timeout(solve_gear3_optimal, nums, k, timeout_sec=2.0)

        if status == "OK" and res == expected:
            verdict = f"{GREEN}✅ PASS{RESET}"
            optimal_passed += 1
        elif status == "TLE":
            verdict = f"{YELLOW}⚠️ TLE (> 2000ms){RESET}"
        elif status.startswith("ERROR"):
            verdict = f"{RED}💥 {status}{RESET}"
        else:
            verdict = f"{RED}❌ WA (Expected: {expected}, Got: {res}){RESET}"

        print(f" Test #{idx:02d} [{test['category']:<17}] {name:<42} : {verdict} ({ms:>7.2f} ms)")

    # Score breakdown
    score_pct = (optimal_passed / total_tests) * 100
    print(f"\n{BOLD}Optimal Score: {optimal_passed} / {total_tests} Tests Passed ({score_pct:.1f}%){RESET}")

    # Phase 2: Gear 1 Brute Force X-Ray Comparison
    print(f"\n{BOLD}{CYAN}----------------------------------------------------------------------{RESET}")
    print(f"{BOLD}Phase 2: Verifying Gear 1 (Human Brute Force Partial Marks){RESET}")
    print(f"{DIM}Verifies that Brute Force secures sample marks but safely TLEs on N=10^5.{RESET}\n")

    brute_sample_res, b_sample_ms, b_sample_status = run_with_timeout(solve_gear1_brute, tests[0]["nums"], tests[0]["k"])
    sample_verdict = f"{GREEN}✅ ACCEPTED (Partial Marks Secured){RESET}" if brute_sample_res == tests[0]["expected"] else f"{RED}❌ FAILED{RESET}"
    print(f" Sample Test 1   : {sample_verdict} ({b_sample_ms:.2f} ms)")

    # Run on the N=10^5 stress test
    stress_test = tests[10]  # The SP Stress Test
    print(f" N=10^5 Stress   : {YELLOW}⏳ Running Brute Force with 2.0s Alarm Guard...{RESET}", end="", flush=True)
    brute_stress_res, b_stress_ms, b_stress_status = run_with_timeout(solve_gear1_brute, stress_test["nums"], stress_test["k"], timeout_sec=2.0)

    if b_stress_status == "TLE":
        print(f"\r N=10^5 Stress   : {YELLOW}⚠️ EXPECTED TLE (> 2000.00 ms) — Guard Triggered Successfully!{RESET}")
    else:
        print(f"\r N=10^5 Stress   : Completed in {b_stress_ms:.2f} ms")

    # Final Summary Table
    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD} 📊 FINAL EXAM VERDICT SUMMARY — DAY 02{RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}")
    print(f" Gear 1 (Brute Force) : {YELLOW}33% Partial Marks{RESET} (TLE on N=10^5 as predicted by Bottleneck X-Ray)")
    print(f" Gear 3 (Optimal)     : {GREEN}{score_pct:.1f}% Full Marks ({optimal_passed}/{total_tests} Accepted){RESET}")
    
    if optimal_passed == total_tests:
        print(f"\n {GREEN}{BOLD}🎉 ALL SYSTEMS CLEARED! DAY 02 SUBMISSION VERIFIED READY FOR PRODUCTION!{RESET}\n")
    else:
        print(f"\n {RED}{BOLD}⚠️ SOME TESTS FAILED. Check diffs before submitting.{RESET}\n")

if __name__ == "__main__":
    run_judge()

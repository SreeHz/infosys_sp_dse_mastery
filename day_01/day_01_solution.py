"""
Day 01: Time Complexity, Fast I/O & Prefix Sums
Problem: The Grand Kingdom Tower Defense (Difference Array & Prefix Accumulation)
Target Roles: Infosys DSE (100-150 Marks) & Specialist Programmer (SP Foundation)

Problem Statement:
The Kingdom of Valoria has a defensive line of N fortress towers numbered 1 to N, all initially starting with 0 armor.
The High Mage casts Q magical fortification spells. Each spell is described as [L, R, X], which adds X units of armor
to every fortress tower from tower L to tower R (1-indexed, inclusive).

Your task:
Calculate the final armor value of every tower from 1 to N after all Q spells have been cast.

Constraints:
1 <= N <= 10^5 (Number of towers)
1 <= Q <= 10^5 (Number of fortification spells)
1 <= L <= R <= N
-10^4 <= X <= 10^4 (Armor change can be positive fortification or negative corrosive curse)
"""

from typing import List
from itertools import accumulate


def solve_gear1_brute(n: int, updates: List[List[int]]) -> List[int]:
    """
    Gear 1: Human Brute Force Template (30% - 40% Partial Testcase Marks)
    
    Approach:
    Direct simulation. For every spell [L, R, X], loop from index L-1 to R-1 and add X directly.
    
    Time Complexity: O(Q * N) -> For N=10^5, Q=10^5, total operations ≈ 10^10, triggering TLE > 2.0s.
    Space Complexity: O(N) auxiliary array for result.
    """
    # 0-indexed armor array of length N initialized to 0
    armor = [0] * n
    
    # Process each spell one-by-one with a nested loop
    for update in updates:
        l, r, x = update
        # Convert 1-based indexing [L, R] to 0-based [L-1, R-1]
        for idx in range(l - 1, r):
            armor[idx] += x
            
    return armor


def solve_gear3_optimal(n: int, updates: List[List[int]]) -> List[int]:
    """
    Gear 3: Tactical Optimal Difference Array Blueprint (100% Full Marks)
    
    Approach:
    Instead of looping across [L, R] for each spell (which takes O(R - L + 1) time),
    we record the CHANGE in armor at the boundaries using a Difference Array in O(1):
      - diff[L] += X     (Armor increases by X starting at tower L)
      - diff[R + 1] -= X (The effect of the spell ends after tower R)
      
    After recording all Q spells in O(Q) time, a single prefix sum sweep from 1 to N
    reconstructs the exact final armor at every tower in O(N) time.
    
    Time Complexity: O(N + Q) -> For N=10^5, Q=10^5, total operations ≈ 2 * 10^5 (< 0.08s in Python).
    Space Complexity: O(N) for the difference array.
    """
    # Allocate difference array of size N + 2 to safely handle 1-indexed R + 1 without index errors
    diff = [0] * (n + 2)
    
    # Step 1: Record all range changes in O(1) time per spell
    for update in updates:
        l, r, x = update
        diff[l] += x
        diff[r + 1] -= x
        
    # Step 2: Accumulate running sum using C-optimized itertools.accumulate
    # diff[1:n+1] slices the relevant 1-indexed towers
    final_armor = list(accumulate(diff[1:n + 1]))
    
    return final_armor


# =====================================================================
# Infosys Online Exam Fast I/O Boilerplate (Muscle Memory Template)
# =====================================================================
# In the actual Infosys online coding platform (Hackerearth / Mettl):
# If inputs are huge (N, Q >= 10^5), avoid calling input() inside loops.
# Copy-paste this standard parser:
#
# if __name__ == "__main__":
#     import sys
#     input_tokens = sys.stdin.read().split()
#     if input_tokens:
#         n = int(input_tokens[0])
#         q = int(input_tokens[1])
#         ptr = 2
#         updates = []
#         for _ in range(q):
#             l = int(input_tokens[ptr])
#             r = int(input_tokens[ptr + 1])
#             x = int(input_tokens[ptr + 2])
#             updates.append([l, r, x])
#             ptr += 3
#         result = solve_gear3_optimal(n, updates)
#         print(*(result))

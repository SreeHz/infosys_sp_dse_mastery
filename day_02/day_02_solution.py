"""
Day 02: Hash Maps, Frequency Engines & Prefix+Hash Patterns
Problem: The Magical Mana Crystal Vine (Subarray Sum Equals K)
Target Roles: Infosys DSE (100-150 Marks) & Specialist Programmer (SP Core Pattern)

Problem Statement:
A mystical glowing vine in the Whispering Forest contains N mana crystals in a straight sequence.
Each crystal 'i' holds an integer mana charge crystals[i] (which can be positive, zero, or negative).
A High Alchemist wishes to harvest continuous clusters of crystals whose combined mana charge
equals exactly K (the resonance threshold).

Your task:
Calculate the total number of continuous sub-segments of crystals whose total sum equals K.

Constraints:
1 <= N <= 10^5 (Number of mana crystals)
-10^4 <= crystals[i] <= 10^4 (Mana energy per crystal)
-10^9 <= K <= 10^9 (Target resonance threshold)
"""

from typing import List
from collections import defaultdict


def solve_gear1_brute(nums: List[int], k: int) -> int:
    """
    Gear 1: Human Brute Force Template (30% - 40% Partial Testcase Marks)
    
    Approach:
    Direct nested loop over all possible start and end points (i, j).
    Maintain a running sum from i to j. If sum == k, increment count.
    
    Time Complexity: O(N^2) -> For N=10^5, total operations ≈ 5 * 10^9, triggering TLE > 2.0s.
    Space Complexity: O(1) auxiliary memory.
    """
    n = len(nums)
    count = 0
    
    for i in range(n):
        running_sum = 0
        for j in range(i, n):
            running_sum += nums[j]
            if running_sum == k:
                count += 1
                
    return count


def solve_gear3_optimal(nums: List[int], k: int) -> int:
    """
    Gear 3: Tactical Optimal Prefix+Hash Frequency Blueprint (100% Full Marks)
    
    Approach:
    Mathematical insight:
      If a subarray from index (i+1) to j sums to K:
      prefix_sum[j] - prefix_sum[i] = K
      ==> prefix_sum[i] = prefix_sum[j] - K
      
    As we iterate through nums:
      1. Add the current number to curr_sum (representing prefix_sum[j]).
      2. Check if (curr_sum - k) exists in our frequency hash map.
         If it does, every previous index where that prefix sum occurred forms a valid
         subarray ending at our current position! Add its frequency to our answer.
      3. Record curr_sum in the hash map for future elements to use.
      
    CRITICAL BASE CASE:
      prefix_counts = {0: 1}
      An empty prefix has sum 0 occurring once. Without this, any subarray starting
      from index 0 where curr_sum == k will NOT be counted!
      
    Time Complexity: O(N) -> Single pass over N elements with O(1) hash lookups (< 0.03s for N=10^5).
    Space Complexity: O(N) in the worst case where all prefix sums are unique.
    """
    # Base case: A prefix sum of 0 has appeared 1 time before starting the array
    prefix_counts = {0: 1}
    
    curr_sum = 0
    total_subarrays = 0
    
    for num in nums:
        curr_sum += num
        need = curr_sum - k
        
        # If the complement prefix sum has been seen before, add all its occurrences
        if need in prefix_counts:
            total_subarrays += prefix_counts[need]
            
        # Record the current prefix sum in our frequency map
        prefix_counts[curr_sum] = prefix_counts.get(curr_sum, 0) + 1
        
    return total_subarrays


# =====================================================================
# Infosys Online Exam Fast I/O Boilerplate (Muscle Memory Template)
# =====================================================================
# If input is large (N >= 10^5), avoid calling input() inside loops.
# Standard Infosys competitive parsing template:
#
# if __name__ == "__main__":
#     import sys
#     input_tokens = sys.stdin.read().split()
#     if input_tokens:
#         n = int(input_tokens[0])
#         k = int(input_tokens[1])
#         nums = [int(x) for x in input_tokens[2:n+2]]
#         result = solve_gear3_optimal(nums, k)
#         print(result)

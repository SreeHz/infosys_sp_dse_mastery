"""
Day 03: Two Pointers (Opposite & Same Direction) & Elevation Math
Problem: The Grand Aqueduct Reservoir of the High Citadel (Container With Most Water)
Target Roles: Infosys DSE (100-150 Marks) & Specialist Programmer (SP Core Pattern)

Problem Statement:
The royal engineers of the High Citadel have built N vertical stone floodgates along a mountain aqueduct.
Each gate 'i' has a height given by height[i].
During the rainy season, water is collected between any two distinct floodgates i and j (where i < j).
The width between the gates is (j - i), and the effective water depth is limited by the shorter of the two gates:
    water_volume = (j - i) * min(height[i], height[j])

Your task:
Find the maximum volume of water the reservoir can store between any two floodgates.

Constraints:
2 <= N <= 10^5 (Number of floodgates)
0 <= height[i] <= 10^4 (Height of each floodgate)
"""

from typing import List


def solve_gear1_brute(height: List[int]) -> int:
    """
    Gear 1: Human Brute Force Template (30% - 40% Partial Testcase Marks)
    
    Approach:
    Check every possible pair of floodgates (i, j) using two nested loops.
    Compute the water capacity for each pair and track the maximum.
    
    Time Complexity: O(N^2) -> For N=10^5, total operations ≈ 5 * 10^9, triggering TLE > 2.0s.
    Space Complexity: O(1) auxiliary memory.
    """
    n = len(height)
    max_water = 0
    
    for i in range(n):
        for j in range(i + 1, n):
            width = j - i
            current_water = width * min(height[i], height[j])
            if current_water > max_water:
                max_water = current_water
                
    return max_water


def solve_gear3_optimal(height: List[int]) -> int:
    """
    Gear 3: Tactical Optimal Two-Pointer Blueprint (100% Full Marks)
    
    Approach (Greedy Height Law):
    1. Start with the widest possible container: left = 0, right = N - 1.
    2. The area is width * min(height[left], height[right]).
    3. Which pointer do we move inward?
       - The height of the water is constrained by the SHORTER of the two gates.
       - If we move the taller gate inward, width decreases by 1, and the height
         remains bounded by the same shorter gate (or worse, an even shorter gate).
         Therefore, moving the taller gate CANNOT possibly increase the area!
       - The only chance to find a larger area is to move the SHORTER gate inward,
         hoping to discover a much taller floodgate that compensates for the lost width.
    4. Terminate when left >= right.
    
    Time Complexity: O(N) -> Each step moves either left or right inward; exactly N-1 iterations (< 0.02s for N=10^5).
    Space Complexity: O(1) auxiliary memory (in-place register tracking).
    """
    left = 0
    right = len(height) - 1
    max_water = 0
    
    while left < right:
        width = right - left
        h_left = height[left]
        h_right = height[right]
        
        if h_left < h_right:
            current_water = width * h_left
            left += 1
        else:
            current_water = width * h_right
            right -= 1
            
        if current_water > max_water:
            max_water = current_water
            
    return max_water


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
#         height = [int(x) for x in input_tokens[1:n+1]]
#         result = solve_gear3_optimal(height)
#         print(result)

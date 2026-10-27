# GEMINI.md — Master System Specification: Infosys SP & DSE 37-Day Tactical Web-Lab Engine

## 1. USER PROFILE, MAIN GOAL & ANTI-BURNOUT DIRECTIVES (CRITICAL CONTEXT)
- **Target Exam:** Infosys Online Coding Round for **Specialist Programmer (SP)** and **Digital Specialist Engineer (DSE)** roles.
- **Exam Structure:** 3 to 4 coding questions in 3 hours:
  - **Q1 (Easy-Medium | 100 Marks):** Arrays, Strings, Hash Maps, Prefix Sums, Two Pointers, Sliding Window.
  - **Q2 (Medium-Hard | 150 Marks):** Greedy Algorithms (custom sorting, monster/RPG quest patterns, intervals, heaps) or Graph/Tree BFS/DFS.
  - **Q3 & Q4 (Hard / Complex | 200+ Marks):** Dynamic Programming (1D/2D Memoization, Knapsack, LIS/LCS, Grid DP, Bitmask/Partition DP), Advanced Graphs, Monotonic Stacks/Deques, and Partial-Testcase Harvesting.
- **Timeline:** **37 Days Full-Time** — Starting **Day 01 on October 16** through **Day 37 on November 22** (Exam Day).
- **Primary Language:** **Python 3**.
- **Coding Level & Calibration:** The user is **not a seasoned competitive programmer**. Every daily module MUST start with a **"Touch of Basics" Python Cushion** (explaining memory, syntax, and simple loop intuition) before escalating smoothly through **Intermediate** to **Tough Advanced / SP-Level tactics**.
- **The "FYI" Anti-Burnout Mandate:** The user has attempted traditional DSA prep for over a year but repeatedly stalled due to dry theory, blank-editor paralysis, and losing momentum when stuck. Therefore:
  1. **Zero Dry Walls of Text:** Everything must be visual, interactive, and story-stripped.
  2. **The 3-Gear Escalator:** Always start from **Gear 1 (Simple Beginner Brute Force)** so the user can always write working code in 5 minutes, then visually show **Gear 2 (Why it TLEs)**, and upgrade a few lines into **Gear 3 (Optimal Pythonic Solution)**.
  3. **The 15-Minute Rule:** Provide 3-tier progressive Hint Drawers for every practice problem so the user never stays stuck for more than 15 minutes.
  4. **Gamified Daily Checklist:** Every daily dashboard must include an interactive progress tracker that saves completion state in `localStorage`.

---

## 2. STRICT TWO-STEP EXECUTION PROTOCOL (PERMISSION GATE)

Whenever the user starts a session or mentions a day (e.g., `"Day 01"`, `"Start Day 01"`, `"What is the plan for Day 05?"`), you **MUST NOT** generate the final website immediately. You must follow this exact **2-Phase Gate**:

### PHASE A: Internet Research, Daily Briefing & Permission Request
When the user initiates a day (without saying `"Generate Day XX"`):
1. **Lookup the Topic:** Check Section 4 of this file for the exact `Day XX` topic and subtopics.
2. **Search the Internet (Mandatory):** Run live web searches to gather:
   - Recent Infosys SP / DSE / HackWithInfy problem variations for today's topic.
   - Python-specific speed hacks, library shortcuts (`collections`, `heapq`, `bisect`, `functools`, `itertools`), and common TLE / edge-case traps.
   - 3 verified LeetCode problem URLs matching today's pattern (1 Warmup Easy, 1 DSE Medium, 1 SP Hard/Complex).
3. **Present the Daily Tactical Briefing:** Show the user:
   - **Today's Daily Checklist** (the exact 5 tasks they will complete today).
   - **What "Touch of Basics" Python concepts** will be covered first.
   - **What Interactive Visual Simulator** will be built.
   - **Which Infosys Disguised Story Problem** & **3 LeetCode Problems** were selected from the search.
   - **Top 3 Topic Hacks/Traps** discovered.
4. **Ask Permission to Customize or Generate:** End Phase A by asking:
   > *"Here is your researched tactical plan for Day XX. Would you like to customize any part of this, or should I go ahead? Reply **'Generate Day XX'** when you are ready for me to build the full Interactive Website and Offline Compiler Suite."*

### PHASE B: Full Package Generation (Triggered ONLY by `"Generate Day XX"`)
**ONLY** when the user explicitly commands **`"Generate Day XX"`** (or explicitly approves generation after Phase A), execute high-effort generation to create these **3 files** in the workspace folder `day_XX/`:
1. `day_XX/day_XX_dashboard.html` — Complete, self-contained, single-page interactive dark-mode learning website (HTML5 + Tailwind/Custom CSS + Vanilla JS + embedded Pyodide in-browser Python runner). **No placeholders or stubbed functions allowed.**
2. `day_XX/day_XX_solution.py` — Clean starter file containing Gear 1 (Brute Force template) and Gear 3 (Optimal template) with detailed beginner-friendly comments where the user writes their solution.
3. `day_XX/day_XX_judge.py` — 100% Offline Local Infosys Test Runner that imports `day_XX_solution.py`, runs 10+ automated test cases (Sample Cases + Edge Cases + a massive $N = 10^5$ Stress Test), measures runtime in milliseconds, and prints colored terminal verdicts (`✅ ACCEPTED`, `⚠️ PARTIAL MARKS (Brute Force TLE on Large N)`, or `❌ WRONG ANSWER` with expected vs. actual diff).

---

## 3. MANDATORY BLUEPRINT FOR `day_XX_dashboard.html` (THE 7 INTERACTIVE MODULES)

Every `day_XX_dashboard.html` must be a rich, interactive web application containing these **7 distinct sections**:

1. **Header & Interactive Daily Task Checklist (Saved in `localStorage`):**
   - Displays Current Day (`Day XX / 37`), Countdown to Nov 22, XP Progress Bar, and 5 clickable checkboxes for today's daily tasks:
     - `[ ] Task 1: Complete 10-Min "Touch of Basics" Python Cushion`
     - `[ ] Task 2: Step through the Interactive Visual Simulator`
     - `[ ] Task 3: Master the 3-Gear Code Escalator & Story-Stripper`
     - `[ ] Task 4: Pass the Offline Judge (`day_XX_judge.py`) on Local Machine`
     - `[ ] Task 5: Solve the 3 LeetCode Arena Matches (Easy + DSE Medium + SP Hard)`
2. **Module 1 — "Touch of Basics" Python Cushion (Beginner-Friendly Foundation):**
   - Visual memory boxes explaining the exact Python syntax, data structures, and indexing needed today (e.g., how `dict` hashing makes lookups $O(1)$ vs list scan $O(N)$, how list slicing or recursion frames work in RAM).
   - Interactive 3-question micro-quiz to verify basic intuition before moving to intermediate/advanced patterns.
3. **Module 2 — Interactive Algorithm Visual Simulator:**
   - A working HTML5/JS visual stage with **`[⏮ Reset]`**, **`[◀ Prev Step]`**, **`[▶ Next Step]`**, **`[⏯ Auto-Play]`**, Speed Slider, and **`[Custom Input Box]`**.
   - Visually animates array indices, moving pointers (`L`, `R`, `mid`, `i`), sliding windows, hash map state tables, greedy sorting swaps, or recursion/DP tree nodes with live narration of *why* each step happens.
4. **Module 3 — The "3-Gear Code Escalator" (Brute Force → Bottleneck X-Ray → Optimal):**
   - Interactive 3-tab code viewer:
     - **Tab 1 (Gear 1 — Human Brute Force):** Simple nested-loop Python code anyone can write in 5 minutes to secure 30%–40% partial marks.
     - **Tab 2 (Gear 2 — The Bottleneck X-Ray):** Visual diagram showing the exact redundant operations causing `TLE` when $N = 10^5$.
     - **Tab 3 (Gear 3 — Tactical Optimal Blueprint):** The upgraded Intermediate/Advanced Python template with line-by-line hover explanations and Big-O complexity comparison meter.
5. **Module 4 — The Infosys "Story-Stripper" & Constraint Decoder:**
   - Displays a realistic, lengthy 300-word Infosys SP/DSE problem statement (involving monsters, kingdoms, servers, or magical arrays).
   - Includes an interactive **`[⚡ Strip the Story Fluff]`** toggle button that visually strikes out 85% of the distracting narrative, highlights the core mathematical goal and input constraint ($N$), and shows the exact 60-second mapping from Constraint $\rightarrow$ Algorithm Blueprint.
6. **Module 5 — Embedded Python Code Playground & Test Runner:**
   - An interactive code editor inside the webpage pre-loaded with today's Infosys problem, powered by **Pyodide (in-browser Python)** with an automatic JS fallback verifier, plus one-click copy buttons to test in the local offline `day_XX_judge.py`.
7. **Module 6 & 7 — LeetCode Live Arena (With 15-Min Hint Drawers) + Tactical Hacks Vault:**
   - **3 Direct LeetCode Cards:** Card 1 (Warmup Easy), Card 2 (DSE Core Medium), Card 3 (SP Boss Hard). Each card has a direct clickable link to LeetCode AND 3 collapsible accordions:
     - *Drawer 1: Visual Pattern Clue (Use after 15 mins stuck)*
     - *Drawer 2: Dry-Run & Transition Logic*
     - *Drawer 3: Full Annotated Python Solution (Gear 1 + Gear 3)*
   - **Tactical Hacks & Partial-Marks Vault:** Topic-specific Python cheat codes (`@lru_cache(None)`, `bisect`, `heapq`, `Counter`, `sys.setrecursionlimit(200000)`, modulo `(10**9 + 7)` rules) and how to harvest partial test cases in the last 10 minutes of the exam.

---

## 4. COMPLETE 37-DAY CURRICULUM (OCT 16 – NOV 22)

### Phase 1: Python Speed Foundations, Arrays, Strings & Hashing (Days 01–08)
| Day | Date | Core Topic | "Touch of Basics" Cushion | Intermediate to Advanced Infosys SP/DSE Tactics |
|---|---|---|---|---|
| **Day 01** | Oct 16 | **Time Complexity, Fast I/O & Prefix Sums** | Python lists in memory, loop counting, `sys.stdin.read`, 1D running sums | 1D/2D Prefix Sums, Difference Arrays (Range Updates in $O(1)$), Constraint-to-Big-O Decoder |
| **Day 02** | Oct 17 | **Hash Maps, Frequency Engines & Prefix+Hash** | Python `dict`, `set`, `get()`, `defaultdict(int)`, `Counter` | Subarray Sum Equals $K$, Divisible Subarrays (Modulo Prefix Trick), Longest Balanced Subarray |
| **Day 03** | Oct 18 | **Two Pointers (Opposite & Same Direction)** | Array indexing from both ends (`left = 0`, `right = n-1`), in-place swaps | 3Sum/K-Sum variants, Container With Most Water, Trapping Rain Water, Dutch National Flag Partitioning |
| **Day 04** | Oct 19 | **Fixed & Variable Sliding Window** | Subarray slicing vs. adding right element & dropping left element | Longest Substring with $K$ Distinct, Minimum Window Substring, Count of Subarrays (`atMost(K) - atMost(K-1)` hack) |
| **Day 05** | Oct 20 | **Kadane’s Algorithm & Subarray Maximization** | Tracking `current_sum` vs `best_sum` in a single loop | Maximum Subarray Sum, Maximum Circular Subarray, Maximum Product Subarray, K-Concatenation Max Sum |
| **Day 06** | Oct 21 | **String Manipulation & Palindrome Engines** | Strings immutability, `ord()`, `chr()`, `"".join()`, frequency tuples | Expand-Around-Center Palindromes, String Anagram Grouping, Lexicographically Smallest String Greedy |
| **Day 07** | Oct 22 | **2D Matrices, Grid Traversals & Coordinate Math** | Nested loops over `grid[r][c]`, 4-directional `dr, dc` arrays | Spiral/Diagonal Traversals, In-Place Matrix Rotation, Search in Sorted 2D Matrix, Manhattan Distance Tricks |
| **Day 08** | Oct 23 | **Phase 1 Consolidation & Infosys Q1 Speed-Run** | Review of `dict`, `Counter`, Prefix Sums, and Sliding Window templates | Timed 3-Problem Infosys Q1/Q2 Set + Decision Tree for Array/String Problem Identification |

### Phase 2: Custom Sorting, Binary Search, Stacks, Heaps & The Greedy Goldmine (Days 09–17)
| Day | Date | Core Topic | "Touch of Basics" Cushion | Intermediate to Advanced Infosys SP/DSE Tactics |
|---|---|---|---|---|
| **Day 09** | Oct 24 | **Custom Lambda Sorting & Infosys Monster Greedy** | `sort()` vs `sorted()`, tuple sorting, `key=lambda x: (x[0], -x[1])` | Classic Infosys RPG Monster Power/Bonus Greedy, Exchange Argument Intuition, Two-City/Cost Ratio Sorting |
| **Day 10** | Oct 25 | **Interval Greedy & Line Sweep Technique** | Representing `[start, end]` pairs and checking overlap `a[1] >= b[0]` | Merge Intervals, Non-Overlapping Intervals (Sort by End Time), Minimum Platforms / Meeting Rooms (Line Sweep) |
| **Day 11** | Oct 26 | **Binary Search & Python `bisect` Module Hacks** | Why sorted arrays cut search space in half; `bisect_left` vs `bisect_right` | First/Last Occurrence, Search in Rotated Sorted Array, Counting Elements in Range in $O(\log N)$ |
| **Day 12** | Oct 27 | **Binary Search on Answer (Monotonic Predicate)** | Turning a question into a `can_we_achieve(mid)` True/False helper | Koko Eating Bananas, Aggressive Cows / Magnetic Balls, Split Array Largest Sum (Minimize the Maximum) |
| **Day 13** | Oct 28 | **Stacks & Monotonic Stack Blueprint** | Python list as LIFO stack (`append`, `pop`, `stack[-1]`) | Next Greater/Smaller Element, Daily Temperatures, Largest Rectangle in Histogram, Sum of Subarray Minimums |
| **Day 14** | Oct 29 | **Queues, `deque` & Monotonic Deque** | Why `list.pop(0)` is $O(N)$ TLE and `collections.deque.popleft()` is $O(1)$ | Sliding Window Maximum in $O(N)$, Shortest Subarray with Sum at Least $K$, Jump Game with Deque |
| **Day 15** | Oct 30 | **Priority Queues & `heapq` (Min/Max Heap Hacks)** | How binary heaps keep the smallest item at `heap[0]`; `-val` trick for Max-Heap | Kth Largest Element, Merge K Sorted Lists, Find Median from Data Stream (Two-Heap Pattern) |
| **Day 16** | Oct 31 | **Advanced Greedy + Heap Hybrids (Regret Greedy)** | Combining `sort()` with a live `heapq` to undo bad greedy choices | IPO / Maximize Capital, Minimum Number of Refueling Stops, Course Schedule III, Task Scheduler |
| **Day 17** | Nov 01 | **Phase 2 Consolidation & Infosys Q2 Greedy Mock** | Rapid drill on `bisect`, `heapq`, and Monotonic Stack templates | Full Infosys Q1 + Q2 Timed Simulation focusing on Greedy & Binary Search on Answer |

### Phase 3: Recursion, Backtracking, Trees & Graph Conquest (Days 18–25)
| Day | Date | Core Topic | "Touch of Basics" Cushion | Intermediate to Advanced Infosys SP/DSE Tactics |
|---|---|---|---|---|
| **Day 18** | Nov 02 | **Visual Recursion Call Stack & Backtracking** | Base case vs recursive step, call stack frames, `sys.setrecursionlimit` | Subsets, Permutations, Combination Sum, N-Queens / Grid Word Search with Pruning |
| **Day 19** | Nov 03 | **Binary Tree DFS (Bottom-Up Info Passing)** | `TreeNode` class, Preorder/Inorder/Postorder traversal visuals | Tree Height & Diameter, Binary Tree Maximum Path Sum, Lowest Common Ancestor (LCA), House Robber on Trees |
| **Day 20** | Nov 04 | **Tree BFS (Level Order) & BST Properties** | Using `deque` to process a tree level-by-level | Zigzag/Right-Side View, Distance K in Binary Tree (Parent Map Trick), Validate & Kth Smallest in BST |
| **Day 21** | Nov 05 | **Graph Representations, DFS & Connected Components** | Converting edge lists `[[u, v]]` into `defaultdict(list)` adjacency lists + `visited` set | Number of Islands, Flood Fill, Max Area of Island, Bipartite Graph Coloring |
| **Day 22** | Nov 06 | **Multi-Source BFS & Unweighted Shortest Paths** | Pushing all starting nodes into `deque` at `time = 0` | Rotting Oranges, 01 Matrix, Shortest Bridge, Word Ladder / Minimum Genetic Mutation |
| **Day 23** | Nov 07 | **Directed Graphs, Cycle Detection & Topological Sort** | Indegree counting (`indegree[v] += 1`) and dependency ordering | Course Schedule I & II (Kahn’s BFS Algorithm), Find Eventual Safe States, Longest Path in a DAG |
| **Day 24** | Nov 08 | **Dijkstra’s Algorithm & State-Space Shortest Path** | Replacing `deque` with `heapq` `(cost, node)` for weighted graphs | Network Delay Time, Path With Minimum Effort, Cheapest Flights Within K Stops, Modified Dijkstra for SP |
| **Day 25** | Nov 09 | **Disjoint Set Union (DSU) Copy-Paste Blueprint** | Parent array `parent[i] = i` and `find()` with path compression | Number of Provinces, Redundant Connection, Accounts Merge, Kruskal’s Minimum Spanning Tree |

### Phase 4: The "No-Fear" Dynamic Programming & Advanced SP Hacks (Days 26–34)
| Day | Date | Core Topic | "Touch of Basics" Cushion | Intermediate to Advanced Infosys SP/DSE Tactics |
|---|---|---|---|---|
| **Day 26** | Nov 10 | **The `@lru_cache(None)` DP Miracle (1D Choice Trees)** | How memoization caches function calls `(index)` to kill repeated tree branches | Climbing Stairs, House Robber I & II, Decode Ways, Minimum Cost For Tickets (Top-Down + Bottom-Up) |
| **Day 27** | Nov 11 | **0/1 Knapsack & Subset Sum Blueprints** | The universal `pick` vs `skip` choice diagram with `(index, remaining_capacity)` | Partition Equal Subset Sum, Target Sum, Ones and Zeroes, Last Stone Weight II |
| **Day 28** | Nov 12 | **Unbounded Knapsack & Coin Change Patterns** | Staying at the *same* `index` after picking an item (`solve(i, cap - w)`) | Coin Change (Min Coins & Total Ways), Rod Cutting, Perfect Squares, Integer Break |
| **Day 29** | Nov 13 | **Two-String DP (LCS, Edit Distance & Palindromes)** | Two pointers `(i, j)` moving across `str1` and `str2` with `@lru_cache` | Longest Common Subsequence (LCS), Longest Palindromic Subsequence, Edit Distance, Distinct Subsequences |
| **Day 30** | Nov 14 | **Longest Increasing Subsequence (LIS) & `bisect` DP** | $O(N^2)$ `prev_index` DP vs $O(N \log N)$ Patience Sorting with `bisect_left` | Classic LIS in $O(N \log N)$, Russian Doll Envelopes, Largest Divisible Subset, Number of LIS |
| **Day 31** | Nov 15 | **2D Grid DP & Multi-Path Optimization** | Moving `(r, c)` on a grid and caching best path from destination | Unique Paths with Obstacles, Minimum Path Sum, Triangle, Dungeon Game / Cherry Pickup |
| **Day 32** | Nov 16 | **State-Machine DP & Partition / Interval DP** | Adding a state flag `(day, holding_stock, transactions_left)` | Best Time to Buy and Sell Stock (Cooldown / K Transactions), Burst Balloons, Partition Array for Max Sum |
| **Day 33** | Nov 17 | **Bit Manipulation, XOR Tricks & Bitmask DP** | Binary representation, `&`, `|`, `^`, `<<`, checking/setting the $k$-th bit | Single Number XOR hacks, Maximum XOR of Two Numbers, Bitmask DP for Infosys SP Q4 ($N \le 18$) |
| **Day 34** | Nov 18 | **Infosys SP Math, Number Theory & Combinatorics** | Modulo rules `(a * b) % MOD`, `math.gcd`, Prime Sieve of Eratosthenes | Fast Modular Exponentiation `pow(a, b, MOD)`, Prime Factorization Queries, nCr Modulo $10^9+7$, Game Theory |

### Phase 5: Full Infosys SP/DSE War-Room Simulations & Exam Triage (Days 35–37)
| Day | Date | Core Topic | Daily Simulation Focus |
|---|---|---|---|
| **Day 35** | Nov 19 | **Infosys DSE/SP Mock Simulation #1** | Full 3-Hour, 3-Question Mock (Q1 Sliding Window + Q2 Greedy Monster/Heap + Q3 Knapsack DP) + Partial-Testcase Triage |
| **Day 36** | Nov 20 | **Infosys SP Hard Mock Simulation #2** | Full 3-Hour, 4-Question Mock (Q1 Prefix/Hash + Q2 Graph/BFS + Q3 Tree/Grid DP + Q4 Bitmask/Partial Score Harvester) |
| **Day 37** | Nov 21–22 | **Master Cheatsheet & Exam-Day Execution** | Interactive 14-Blueprint Visual Cheatsheet Dashboard, 5-Minute Brute-Force Fallback Drill, and Exam-Day Mental Checklist |
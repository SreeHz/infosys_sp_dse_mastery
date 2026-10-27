# PROJECT ARCHITECT & EXECUTION BLUEPRINT
**Infosys Specialist Programmer (SP) & Digital Specialist Engineer (DSE) 37-Day Web-Lab Engine**

---

## 1. Laptop Environment Verification (Audited 2026-10-15)

| Component | Status | Details |
|---|---|---|
| **Python Runtime** | ✅ **Ready** | Python 3.12.3 installed at `/usr/bin/python3` |
| **CP Standard Library** | ✅ **Verified** | `collections`, `heapq`, `bisect`, `functools`, `itertools`, `sys`, `math`, `time`, `json` |
| **External Dependencies** | ℹ️ **Zero Needed** | Pure standard library used for `day_XX_judge.py` and `day_XX_solution.py` (no `pip` needed) |
| **Browser Environment** | ✅ **Ready** | Google Chrome installed at `/usr/bin/google-chrome` |
| **CDNs for Dashboards** | ✅ **Accessible** | Tailwind CSS (`cdn.tailwindcss.com`) and Pyodide Wasm (`cdn.jsdelivr.net/pyodide/v0.26.1`) verified 200/302 |
| **Offline Fallback** | ✅ **Built-in** | Dashboards include native JS test runners so dashboards run seamlessly even with flaky Wi-Fi |

---

## 2. Daily Artifact Specifications

Each day `day_XX` contains three tightly-coupled components:

### A. `day_XX/day_XX_dashboard.html`
- **Theme:** Modern dark aesthetic (Background `#0b0f19`, Surface `#111827`, Borders `#1f293d`, Neon Accents: Cyan `#06b6d4`, Emerald `#10b981`, Amber `#f59e0b`, Rose `#f43f5e`).
- **Typography:** Inter / JetBrains Mono (with clean sans-serif system fallbacks).
- **The 7 Modules:**
  1. Header with Countdown, XP Bar, and LocalStorage Checkbox Checklist (`infosys_day_XX_progress`).
  2. "Touch of Basics" visual memory cards + 3-question instant diagnostic quiz.
  3. Interactive Algorithm Visualizer with Step-by-Step pointer tracking, slider speed, play/pause, custom inputs.
  4. 3-Gear Escalator (Gear 1 Brute Force, Gear 2 TLE X-Ray, Gear 3 Optimal Template + Line-by-line hover breakdown).
  5. Infosys Story Stripper & Constraint-to-Complexity Decoder.
  6. In-browser Python Playground (Pyodide Wasm + Instant JS Fallback) with "Copy for Local Judge" button.
  7. LeetCode Arena (3 direct cards with 15-min Hint Drawers) + Tactical Hacks & Partial-Testcase Harvester.

### B. `day_XX/day_XX_solution.py`
- Executable, clean starter template:
  - `solve_gear1_brute(input_data)`: Simple loops, partial mark earner.
  - `solve_gear3_optimal(input_data)`: Optimal Big-O solution.
  - Docstrings explaining variable states, time/space complexity, and common traps.

### C. `day_XX/day_XX_judge.py`
- Standalone zero-dependency terminal judge:
  - ANSI colored terminal output (`[PASS]`, `[TLE]`, `[FAIL]`, `[PARTIAL]`).
  - 10+ categorized test cases: Basic Samples, Edge Cases (empty, single element, negative numbers, duplicates), and $N = 10^5$ Stress Test.
  - High-precision runtime measurement (`time.perf_counter()`).
  - Score summary table with percentage calculation.

---

## 3. Curriculum Tracking Matrix (37 Days)

| Day | Date | Topic | Phase A (Briefed) | Phase B (Generated) | Judge Passed |
|:---:|:---:|:---|:---:|:---:|:---:|
| **01** | Oct 16 | Time Complexity, Fast I/O & Prefix Sums | ✅ Done | ✅ Done | ✅ 12/12 Passed |
| **02** | Oct 17 | Hash Maps, Frequency Engines & Prefix+Hash | ✅ Done | ✅ Done | ✅ 12/12 Passed |
| **03** | Oct 18 | Two Pointers (Opposite & Same Direction) | ✅ Done | ✅ Done | ✅ 12/12 Passed |
| **04** | Oct 19 | Fixed & Variable Sliding Window | ✅ Done | ✅ Done | ✅ 12/12 Passed |
| **05** | Oct 20 | Kadane’s Algorithm & Subarray Maximization | ✅ Done | ✅ Done | ✅ 12/12 Passed |
| **06** | Oct 21 | String Manipulation & Palindrome Engines | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **07** | Oct 22 | 2D Matrices, Grid Traversals & Coordinate Math | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **08** | Oct 23 | Phase 1 Consolidation & Infosys Q1 Speed-Run | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **09** | Oct 24 | Custom Lambda Sorting & Monster Greedy | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **10** | Oct 25 | Interval Greedy & Line Sweep Technique | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **11** | Oct 26 | Binary Search & Python `bisect` Hacks | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **12** | Oct 27 | Binary Search on Answer (Predicate) | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **13** | Oct 28 | Stacks & Monotonic Stack Blueprint | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **14** | Oct 29 | Queues, `deque` & Monotonic Deque | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **15** | Oct 30 | Priority Queues & `heapq` Hacks | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **16** | Oct 31 | Advanced Greedy + Heap Hybrids (Regret) | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **17** | Nov 01 | Phase 2 Consolidation & Infosys Q2 Mock | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **18** | Nov 02 | Recursion Call Stack & Backtracking | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **19** | Nov 03 | Binary Tree DFS (Bottom-Up Info Passing) | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **20** | Nov 04 | Tree BFS (Level Order) & BST Properties | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **21** | Nov 05 | Graph Representations, DFS & Components | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **22** | Nov 06 | Multi-Source BFS & Shortest Paths | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **23** | Nov 07 | Directed Graphs, Cycles & Topological Sort | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **24** | Nov 08 | Dijkstra’s Algorithm & State-Space Path | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **25** | Nov 09 | Disjoint Set Union (DSU) Blueprint | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **26** | Nov 10 | `@lru_cache(None)` DP Miracle (1D Trees) | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **27** | Nov 11 | 0/1 Knapsack & Subset Sum Blueprints | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **28** | Nov 12 | Unbounded Knapsack & Coin Change Patterns | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **29** | Nov 13 | Two-String DP (LCS, Edit Distance) | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **30** | Nov 14 | Longest Increasing Subsequence & `bisect` DP | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **31** | Nov 15 | 2D Grid DP & Multi-Path Optimization | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **32** | Nov 16 | State-Machine DP & Partition/Interval DP | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **33** | Nov 17 | Bit Manipulation, XOR & Bitmask DP | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **34** | Nov 18 | Infosys SP Math, Number Theory & Combinatorics | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **35** | Nov 19 | Infosys DSE/SP Mock Simulation #1 | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **36** | Nov 20 | Infosys SP Hard Mock Simulation #2 | ⏳ Pending | ⏳ Pending | ⏳ Pending |
| **37** | Nov 21–22 | Master Cheatsheet & Exam-Day Execution | ⏳ Pending | ⏳ Pending | ⏳ Pending |

---

## 4. Master Command Center Concept (`index.html`)

A unified portal in the root workspace to:
- Dynamically display the 37-day roadmap with progress rings.
- Aggregate all daily task checkboxes from `localStorage` into an overall percentage bar.
- Provide quick links to open any day's dashboard in Chrome.
- Provide quick terminal commands to run judges.

---

## 5. Strict Engineering Guardrails & Execution Rules (Finalized)

1. **Hard 2.0-Second Timeout in `day_XX_judge.py`:**
   - Never let `solve_gear1_brute` freeze the terminal on the $N = 10^5$ Stress Test.
   - Use Linux `signal.SIGALRM` / `signal.setitimer(signal.ITIMER_REAL, 2.0)` around each test execution so any function exceeding 2000ms is immediately terminated and marked `[TLE > 2000ms — Partial Marks Only]`.
2. **Real Unpacked Function Signatures + Infosys `stdin` Parser:**
   - Instead of generic `input_data`, use explicit typed arguments (e.g., `def solve_gear3_optimal(n: int, arr: list[int], k: int) -> int:`) matching LeetCode/Infosys signatures.
   - Include a commented-out `sys.stdin.read().split()` parser template at the bottom of `day_XX_solution.py` so the user builds muscle memory for Infosys standard input.
3. **Localhost Origin for `localStorage` & Pyodide (`index.html` Sync):**
   - Standardize the `localStorage` JSON schema across all 37 days as:
     `localStorage.setItem("infosys_day_XX_progress", JSON.stringify({ tasks: [bool, bool, bool, bool, bool], xp: number, completed: bool }))`
   - Provide a 1-line helper command (`python3 -m http.server 8080`) in `index.html` instructions so `index.html` and all `day_XX/day_XX_dashboard.html` share the exact same `http://localhost:8080` origin.
4. **Spaced-Repetition Flashback (Day 02+):**
   - In Module 2 ("Touch of Basics" 3-question quiz), Question 3 must always be a 30-second flashback pattern check from a previous day's topic so earlier blueprints are never forgotten.
5. **Zero-Placeholder Mandate & Matrix Auto-Update:**
   - Never use `// TODO` or truncated HTML/JS in `day_XX_dashboard.html`. Every button, visualizer step, hint drawer, and quiz option must be 100% functional.
   - Automatically update Section 3 (Curriculum Tracking Matrix) in `PROJECT_ARCHITECT.md` from `⏳ Pending` to `✅ Done` whenever Phase A, Phase B, or Judge verification completes.

---

## 6. Vertex AI "Self-Mutating Web-Lab" Integration (₹28,000 GCP Credit Engine)

### A. Local Vertex AI Bridge Server (`vertex_lab_server.py`)
- Build a lightweight local Python server (`vertex_lab_server.py` running on `http://localhost:8080`) using the `google-genai` / Vertex AI SDK authenticated with the user's Google Cloud project (`₹28,000 Free Trial Credit`).
- **Model Router Support:** Support a selectable model dropdown in the UI featuring **`gemini-4-argon`** (primary frontier coding/visual model) with automatic fallback to **`gemini-3.8-flash`** (high-thinking mode) and **`gemini-3.1-pro-preview`** so API calls never fail due to trial tier gates.
- **Endpoints to Provide:**
  1. `POST /api/ask-doubt`: Accepts `{ day, module_id, current_module_html, user_doubt, user_code }`. Returns `{ explanation_markdown, python_code, proposed_html_js_patch }`.
  2. `POST /api/mutate-website`: Executes ONLY after explicit user permission. Supports 3 modes:
     - `"replace_section"`: Safely backs up `day_XX_dashboard.html` to `.bak` and replaces the target `<section id="module-X">` on disk and in the live DOM.
     - `"append_new_section"`: Injects a new interactive visual/code card right below the target section in `day_XX_dashboard.html` and saves it to disk.
     - `"create_new_page"`: Creates a standalone custom sub-dashboard `day_XX/day_XX_doubt_YY.html` and returns the link.
  3. `POST /api/undo-mutation`: Restores the previous snapshot of `day_XX_dashboard.html` in one click.
  4. `POST /api/run-judge`: Executes `day_XX_judge.py` directly from the browser and returns the JSON test-case results table so the user never even has to switch to the terminal unless they want to.

### B. In-Dashboard "Vertex AI Co-Pilot & UI Mutator" Drawer (Embedded in `day_XX_dashboard.html`)
- Every module (`#module-1` through `#module-7`) in `day_XX_dashboard.html` must have a **`[⚡ Ask AI / Redesign This Section]`** button.
- Clicking it opens the slide-out **Vertex AI Architect Drawer** where the user can ask any doubt in plain English.
- Whenever the AI proposes a new visual diagram, interactive simulator, or simplified code walkthrough, it **MUST NOT** overwrite the webpage automatically. It must display a **Permission Prompt**:
  > *"I generated a custom interactive visual & explanation for your doubt. How would you like to apply it?"*
  - **`[🔄 Redesign & Replace Current Section]`**
  - **`[➕ Insert as a New Custom Section Below]`**
  - **`[🆕 Open as a Separate Mini-Lab Page]`**
  - **`[💬 Keep in Chat Only]`**
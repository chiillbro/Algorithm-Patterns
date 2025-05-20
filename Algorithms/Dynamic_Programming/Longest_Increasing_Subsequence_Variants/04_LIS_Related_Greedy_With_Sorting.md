**Pattern 4: LIS-Related - Greedy Choice with Strategic Sorting**

- **Problem Statement:** Some problems, while appearing to seek a "longest chain" or "maximum set" with ordering constraints, can be solved optimally using a greedy approach _after_ a specific, careful sorting of the input items. The choice of sorting key is critical.
- **Keywords:** "longest chain", "maximum number of non-overlapping intervals" (can be similar), problems where picking an item influences future choices based on its end points/values.
- **Core Idea:**
  1.  **Identify the "ending" property:** Determine which part of an item dictates when the _next_ item can start (e.g., the second element of a pair, the end time of an interval).
  2.  **Sort by this "ending" property:** Sorting the items by this critical ending property often allows a greedy strategy to work.
  3.  **Greedy Selection:** Iterate through the sorted items. Maintain the "end" of the current chain/set. If the current item can validly start after the current chain's end, select it and update the chain's end.

---

**Template: Greedy for Maximum Length of Pair Chain (LeetCode 646)**

- **Problem:** Given `pairs[i] = [left_i, right_i]`. A pair `[c, d]` can follow `[a, b]` if `b < c`. Find the length of the longest chain.

```python
def find_longest_chain_greedy(pairs: list[list[int]]) -> int:
    if not pairs:
        return 0 # Why: No pairs, no chain.

    # 1. Sort by the *second* element (the 'right_i' or end of the pair).
    #    Why sort by the second element?
    #    Consider pairs A=[1,100], B=[2,3], C=[4,5].
    #    If sorted by first: A, B, C. Pick A. Can't pick B or C. Chain=1. (Suboptimal)
    #    If sorted by second: B, C, A.
    #       - Pick B ([2,3]). current_chain_end = 3. Count = 1.
    #       - Next is C ([4,5]). C's start (4) > current_chain_end (3). Pick C. current_chain_end = 5. Count = 2.
    #       - Next is A ([1,100]). A's start (1) is NOT > current_chain_end (5). Skip A.
    #    Chain = 2 (B, C). This is optimal.
    #    Sorting by the end point allows us to greedily pick the pair that "finishes earliest".
    #    This leaves the maximum possible room for subsequent pairs. This is a common
    #    greedy strategy, similar to Activity Selection Problem.
    pairs.sort(key=lambda x: x[1])

    current_chain_end = float('-inf') # Why: Initialize so the first valid pair can always be chosen.
    chain_length = 0

    # 2. Iterate and make greedy choices.
    for left, right in pairs:
        # If the current pair's start ('left') is greater than the end of the
        # last pair added to our chain ('current_chain_end').
        if left > current_chain_end:
            # This pair can extend the chain.
            chain_length += 1
            # Update the end of our current chain to this pair's end.
            current_chain_end = right
            # Why update to 'right'? Because the next pair must start after this 'right'.

    return chain_length
```

**Explanation of `find_longest_chain_greedy`:**

- `pairs.sort(key=lambda x: x[1])`:
  - **Why `x[1]`?** This sorts the pairs based on their _second element_ (the "end" of the pair). The intuition is that by picking a pair that finishes as early as possible, we leave more "room" or opportunity for subsequent pairs to be added to the chain. This is a hallmark of greedy algorithms for interval-like problems (e.g., Activity Selection).
- `current_chain_end = float('-inf')`:
  - **Why `float('-inf')`?** We initialize the end of our "current chain" to a very small number. This ensures that the very first pair we consider (after sorting) whose `left` value will be greater than `float('-inf')` can be selected to start the chain.
- `chain_length = 0`: To count the number of pairs in the longest chain.
- `for left, right in pairs:`: Iterate through the pairs, which are now sorted by their end points.
- `if left > current_chain_end:`:
  - **Why this condition?** This is the problem's definition of a valid chain: the start of the current pair (`left`) must be strictly greater than the end of the previously selected pair in the chain (`current_chain_end`).
  - If true, we can add this current pair to our chain.
- `chain_length += 1`: Increment the count.
- `current_chain_end = right`: **Crucial greedy step.** We update `current_chain_end` to the end point (`right`) of the _current pair we just added_. We don't look ahead. We greedily commit to this pair and set the new requirement for the _next_ pair in the chain.

---

- **Example Problems:**
  - [LeetCode 646: Maximum Length of Pair Chain](https://leetcode.com/problems/maximum-length-of-pair-chain/)
  - Activity Selection Problem (Classic greedy problem)
- **Complexity:**
  - Time: O(N log N) - Dominated by the sorting step. The iteration is O(N).
  - Space: O(1) or O(N) - O(1) if sorting is in-place and we don't count input storage. O(N) if sorting requires extra space (like Timsort in Python might use for slices).
- **Important Considerations:**
  - The correctness of greedy algorithms often relies on proving a "greedy choice property" (making a locally optimal choice leads to a global optimum) and "optimal substructure." For Pair Chain, sorting by the second element enables this.
  - Not all LIS-like problems can be solved greedily. This pattern applies when a specific sorting order makes the greedy choice safe.

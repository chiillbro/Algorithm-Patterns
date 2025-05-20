**Pattern 2: LIS - Path Reconstruction (Finding the Actual Subsequence)**

- **Problem Statement:** Given an array of integers, find not just the length, but one actual longest increasing subsequence.
- **Keywords:** "find the longest increasing subsequence", "construct LIS".
- **Core Idea:** Extend the O(N^2) DP approach. While calculating `dp[i]` (length of LIS ending at `nums[i]`), also store the index of the element `nums[j]` that preceded `nums[i]` in this LIS. After computing all `dp` values, find the maximum `dp` value, which gives the end of an LIS. Then, backtrack using the predecessor indices to reconstruct the subsequence.

---

**Template: O(N^2) DP Approach with Path Reconstruction**

```python
def longest_increasing_subsequence_with_path(nums: list[int]) -> list[int]:
    n = len(nums)
    if n == 0:
        return [] # Why: Empty array, no subsequence.

    # dp[i] stores the length of the LIS ending at nums[i].
    dp = [1] * n
    # prev_indices[i] stores the index of the element that comes *before* nums[i]
    # in the LIS ending at nums[i]. Initialize with -1 to indicate no predecessor.
    prev_indices = [-1] * n

    # To find the end of the overall LIS for reconstruction.
    max_len = 1       # Why: Minimum LIS length is 1.
    last_idx = 0      # Why: Index of the last element of the LIS found so far. Initialize to 0 assuming first element is LIS of length 1.

    for i in range(n):
        for j in range(i):
            if nums[i] > nums[j]:
                # If extending LIS ending at nums[j] gives a longer LIS for nums[i]
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    prev_indices[i] = j # Why: Record that nums[j] is the predecessor of nums[i].

        # Check if the LIS ending at nums[i] is the longest found so far.
        if dp[i] > max_len:
            max_len = dp[i]
            last_idx = i # Why: Update the end point of the overall LIS.

    # Reconstruct the LIS path
    lis = []
    current_idx = last_idx # Why: Start backtracking from the end of the longest LIS.
    while current_idx != -1:
        lis.append(nums[current_idx]) # Why: Add the element to our result.
        current_idx = prev_indices[current_idx] # Why: Move to its predecessor.

    return lis[::-1] # Why: The LIS is reconstructed in reverse order, so reverse it.

```

**Explanation of `longest_increasing_subsequence_with_path`:**

- `dp = [1] * n`: Same as basic LIS length; `dp[i]` is the length of LIS ending at `nums[i]`.
- `prev_indices = [-1] * n`:
  - **Why `prev_indices`?** This array is key for reconstruction. `prev_indices[i]` stores the index `j` such that `nums[j]` is the element immediately preceding `nums[i]` in the LIS of length `dp[i]` that ends at `nums[i]`.
  - **Why initialize to `-1`?** Indicates that, by default, an element `nums[i]` (forming an LIS of length 1 by itself) has no predecessor in that specific LIS.
- `max_len = 1`, `last_idx = 0`:
  - **Why `max_len` and `last_idx`?** Unlike just finding the length (where we can `max(dp)` at the end), for reconstruction, we need to know _where_ one such longest subsequence ends. These variables track the length and ending index of the longest LIS found _so far_ during the iteration.
- `for i in range(n): ... for j in range(i): ...`: Standard O(N^2) LIS calculation.
- `if nums[i] > nums[j]:`: Check if `nums[i]` can extend an LIS ending at `nums[j]`.
- `if dp[j] + 1 > dp[i]:`:
  - **Why `> dp[i]` and not `>= dp[i]`?** If it's equal, we could potentially have multiple LIS of the same length ending at `nums[i]`. For just one path, `>` is fine. If you need all paths or specific criteria for ties, this logic might change. Here, we are just updating if we find a _strictly longer_ way to form an LIS ending at `nums[i]`.
  - `dp[i] = dp[j] + 1`: Update the length.
  - `prev_indices[i] = j`: **Crucial for reconstruction.** Record that `nums[j]` is the element that allowed us to achieve this `dp[i]`.
- `if dp[i] > max_len: ...`: After processing all `j` for a given `i`, if the LIS ending at `nums[i]` is longer than any LIS found before, update `max_len` and `last_idx` (the index where this current longest LIS ends).
- **Reconstruction Phase:**
  - `lis = []`: Initialize an empty list to store the LIS elements.
  - `current_idx = last_idx`: Start from the `last_idx` we identified as the end of an overall LIS.
  - `while current_idx != -1:`: Loop until we reach an element that had no predecessor (the start of this particular LIS).
  - `lis.append(nums[current_idx])`: Add the element at the current index to our result.
  - `current_idx = prev_indices[current_idx]`: Move to the predecessor of the current element using the `prev_indices` array.
  - `return lis[::-1]`: The elements are added from end to start, so the `lis` list needs to be reversed to get the correct order.

---

- **Example Problem (Direct LIS with path):**
  - Standard LIS problem but asking for the subsequence itself (often a follow-up).
- **Example Problem (Variation using this pattern - Largest Divisible Subset):**

  - [LeetCode 368: Largest Divisible Subset](https://leetcode.com/problems/largest-divisible-subset/)
  - **Adaptation:**
    1.  Sort the input `nums`.
    2.  The condition `nums[i] > nums[j]` becomes `nums[i] % nums[j] == 0`.
    3.  The rest of the DP logic (calculating lengths `dp[i]` for subset ending with `nums[i]`, storing `prev_indices[i]`, and reconstructing) is analogous.

  ```python
  # Solution for LeetCode 368: Largest Divisible Subset (provided by user, fits this pattern)
  def largestDivisibleSubset(self, nums: list[int]) -> list[int]:
      n = len(nums)
      if n == 0:
          return []

      nums.sort() # Why: Sorting simplifies the divisibility check (only need to check nums[i] % nums[j] if j < i)
                  # and ensures that if nums[j] divides nums[i], then nums[j] <= nums[i].

      dp = [1] * n      # dp[i] = length of largest divisible subset ending with nums[i]
      prev = [-1] * n   # prev[i] = index of previous element in the LDS ending with nums[i]

      max_len_idx = 0   # Index of the element where the overall longest divisible subset ends

      for i in range(n):
          for j in range(i):
              # If nums[i] is divisible by nums[j], nums[i] can extend the subset ending at nums[j]
              if nums[i] % nums[j] == 0:
                  if dp[j] + 1 > dp[i]:
                      dp[i] = dp[j] + 1
                      prev[i] = j # Record nums[j] as the predecessor

          # Update the index of the element that ends the longest subset found so far
          if dp[i] > dp[max_len_idx]:
              max_len_idx = i

      # Reconstruct the largest divisible subset
      res = []
      curr_idx = max_len_idx
      while curr_idx != -1:
          res.append(nums[curr_idx])
          curr_idx = prev[curr_idx]

      return res[::-1] # Return in increasing order
  ```

- **Complexity:**
  - Time: O(N^2) - For filling `dp` and `prev_indices` arrays. Sorting (if needed, like for Largest Divisible Subset) takes O(N log N). Reconstruction takes O(N) in the worst case (LIS length is N). Overall dominated by O(N^2).
  - Space: O(N) - For `dp` and `prev_indices` arrays. The result list also takes O(N).
- **Important Considerations:**
  - The O(N log N) LIS length algorithm is harder to adapt directly for path reconstruction. While possible (e.g., by storing pointers or multiple lists), it adds significant complexity. For path reconstruction, the O(N^2) approach is more straightforward.
  - If multiple LIS of the same maximum length exist, this template finds one of them. To find all, the logic would need to be more complex (e.g., `prev_indices[i]` could be a list of predecessors).

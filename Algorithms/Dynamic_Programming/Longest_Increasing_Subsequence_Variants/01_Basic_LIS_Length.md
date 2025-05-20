**Pattern 1: Basic LIS - Finding the Length**

- **Problem Statement:** Given an array of integers, find the length of the longest increasing subsequence.
- **Keywords:** "longest increasing subsequence", "length of LIS".
- **Core Idea:**
  1.  **O(N^2) Approach:** For each element `nums[i]`, find the length of the LIS ending with `nums[i]`. This is `1 + max(length of LIS ending at nums[j])` for all `j < i` where `nums[j] < nums[i]`.
  2.  **O(N log N) Approach:** Maintain a sorted list of the smallest tail elements for all active increasing subsequences of varying lengths. For each number, either extend the longest current LIS or replace an existing tail to get a shorter LIS with a smaller end (better for future).

---

**Template 1: O(N^2) DP Approach (Tabulation)**

```python
def length_of_lis_n_squared(nums: list[int]) -> int:
    n = len(nums)
    if n == 0:
        return 0  # Why: An empty array has no subsequence, so length is 0.

    # dp[i] will store the length of the Longest Increasing Subsequence
    # that *ends* with the element nums[i].
    dp = [1] * n  # Why: Initialize with 1 because each element itself is an LIS of length 1.

    # Iterate through each element of the array, considering it as a potential end of an LIS.
    for i in range(n):
        # For the current element nums[i], iterate through all previous elements nums[j] (where j < i).
        for j in range(i):
            # If nums[i] is greater than nums[j], it means nums[i] can potentially
            # extend the LIS that ends at nums[j].
            if nums[i] > nums[j]:
                # The new LIS ending at nums[i] would be (LIS ending at nums[j]) + nums[i].
                # Its length would be dp[j] + 1.
                # We want the *longest* such LIS, so we take the maximum.
                dp[i] = max(dp[i], dp[j] + 1)

    # The length of the LIS for the entire array is the maximum value in the dp array,
    # because the LIS can end at any element.
    return max(dp) if dp else 0 # Handle case where dp might be empty if n=0 was not checked initially.

```

**Explanation of `length_of_lis_n_squared`:**

- `n = len(nums)`: Get the number of elements.
- `if n == 0: return 0`: Base case for an empty input.
- `dp = [1] * n`:
  - **Why `dp` array?** This array stores the intermediate results of our subproblems.
  - **Why `dp[i]`?** `dp[i]` represents the length of the longest increasing subsequence that _must end with `nums[i]`_. This definition is crucial.
  - **Why initialize with `1`?** Any single element `nums[i]` by itself forms an increasing subsequence of length 1. This is our base case for each `dp[i]`.
- `for i in range(n):`: This outer loop iterates through each element `nums[i]`. We are trying to calculate `dp[i]` (the LIS length ending at `nums[i]`).
- `for j in range(i):`: This inner loop iterates through all elements `nums[j]` that come _before_ `nums[i]` in the array.
  - **Why `j < i`?** Subsequences must maintain the relative order of elements from the original array.
- `if nums[i] > nums[j]:`: This is the "increasing" condition. If `nums[i]` is greater than a previous element `nums[j]`, then `nums[i]` can potentially follow `nums[j]` in an increasing subsequence.
- `dp[i] = max(dp[i], dp[j] + 1)`:
  - **Why `dp[j] + 1`?** If `nums[i]` extends an LIS ending at `nums[j]` (which has length `dp[j]`), the new LIS ending at `nums[i]` has length `dp[j] + 1`.
  - **Why `max(dp[i], ...)`?** We consider all possible `nums[j]` that `nums[i]` can follow. We want the one that gives the _longest_ LIS ending at `nums[i]`. `dp[i]` initially holds `1` (for `nums[i]` itself) or the result from a previous `j`.
- `return max(dp) if dp else 0`: The LIS of the entire array doesn't necessarily end at `nums[n-1]`. It can end at _any_ `nums[i]`. So, the overall LIS length is the maximum value found in the `dp` array. The `if dp else 0` handles the `n=0` case gracefully if not handled at the start.

---

**Template 2: O(N log N) "Patience Sorting" / Binary Search Approach**

```python
from bisect import bisect_left

def length_of_lis_n_log_n(nums: list[int]) -> int:
    n = len(nums)
    if n == 0:
        return 0 # Why: Empty array, LIS length is 0.

    # 'tails' is a list where tails[i] is the smallest tail of all
    # increasing subsequences of length i+1.
    # This list is always kept sorted.
    tails = []

    for num in nums:
        # If 'tails' is empty or 'num' is greater than the largest tail,
        # 'num' can extend the longest increasing subsequence found so far.
        if not tails or num > tails[-1]:
            tails.append(num) # Why: Start a new, longer LIS or extend the current longest.
        else:
            # Find the smallest tail element that is >= 'num'.
            # We want to replace this tail with 'num' because 'num' can form an
            # increasing subsequence of the same length but with a smaller tail element.
            # A smaller tail element is better as it allows more future elements to extend it.
            # bisect_left finds the insertion point to maintain sort order.
            # If num is already in tails, it finds the index of the first occurrence.
            # If num is not in tails, it finds the index where num could be inserted
            # to maintain order, which corresponds to the first element > num.
            idx_to_replace = bisect_left(tails, num) # Why: Efficiently find where 'num' fits.

            tails[idx_to_replace] = num # Why: Replace to get a potentially "better" LIS of same length.

    # The length of the 'tails' list is the length of the LIS.
    return len(tails) # Why: Each element added to 'tails' (either by append or replace) effectively signifies finding or improving an LIS of a certain length. The final size of 'tails' reflects the max length achieved.
```

**Explanation of `length_of_lis_n_log_n`:**

- `tails = []`:
  - **Why `tails`?** This list doesn't store an LIS itself. Instead, `tails[i]` stores the smallest ending element of an increasing subsequence of length `i+1`.
  - **Why is it kept sorted?** This property is crucial for using binary search (`bisect_left`) and is maintained by the logic.
- `for num in nums:`: Iterate through each number in the input.
- `if not tails or num > tails[-1]:`:
  - **Why this condition?** If `tails` is empty, `num` starts the first LIS of length 1. If `num` is greater than the current largest tail (`tails[-1]`), it means `num` can extend the longest LIS found so far, increasing its length by 1.
  - `tails.append(num)`: Add `num` to `tails`. The length of `tails` increases by 1, signifying that we've found an LIS that is one element longer.
- `else:`: This means `num <= tails[-1]`. So, `num` cannot extend the current _longest_ LIS. However, it might help form an LIS of some existing length `k` but with a _smaller ending element_ than what `tails[k-1]` currently holds.
- `idx_to_replace = bisect_left(tails, num)`:
  - **Why `bisect_left`?** `bisect_left(a, x)` returns an insertion point which comes before (to the left of) any existing entries of `x` in `a` and after (to the right of) any existing entries of `x` in `a` that are less than `x`. In a sorted list `tails`, this finds the index of the smallest element in `tails` that is greater than or equal to `num`.
- `tails[idx_to_replace] = num`:
  - **Why replace?** We are replacing `tails[idx_to_replace]` (which was `>= num`) with `num`. This means we found an increasing subsequence of length `idx_to_replace + 1` that ends with `num` (which is smaller or equal to the previous `tails[idx_to_replace]`). A smaller ending element for an LIS of a given length is always preferable because it provides more opportunities for future elements to extend it.
- `return len(tails)`:
  - **Why `len(tails)`?** The size of the `tails` array at the end correctly gives the length of the LIS. Each time we `append`, the LIS length increases. When we replace, the LIS length (represented by the position `idx_to_replace`) doesn't change for that particular length, but we've made it "better" (smaller tail). The overall maximum length achieved is tracked by the size of `tails`.

---

- **Example Problems:**
  - [LeetCode 300: Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/)
- **Complexity:**
  - **O(N^2) DP Approach:**
    - Time: O(N^2) - Two nested loops.
    - Space: O(N) - For the `dp` array.
  - **O(N log N) Approach:**
    - Time: O(N log N) - Outer loop runs N times, `bisect_left` takes O(log N) or O(log K) where K is current size of `tails` (K <= N).
    - Space: O(N) - In the worst case (e.g., sorted array), `tails` can store up to N elements.
- **Important Considerations:**
  - The O(N log N) approach is generally preferred for its better time complexity.
  - The O(N^2) approach is often simpler to understand initially and adapt for variations like path reconstruction or counting LIS.
  - Non-decreasing subsequence: Change `nums[i] > nums[j]` to `nums[i] >= nums[j]` and `num > tails[-1]` to `num >= tails[-1]`, and use `bisect_right` for the replacement logic if you want to allow duplicates to form sequences of the same length. For strictly increasing, `bisect_left` is correct.

**Pattern 5: LIS - Counting Variations (e.g., Number of LIS)**

- **Problem Statement:** Instead of just the length of the LIS, or one instance of an LIS, we need to count _how many distinct_ LIS of the maximum possible length exist.
- **Keywords:** "number of longest increasing subsequences", "count distinct LIS".
- **Core Idea:**
  1.  Use two DP arrays:
      - `lengths[i]`: Stores the length of the LIS ending with `nums[i]` (standard LIS).
      - `counts[i]`: Stores the number of distinct LIS that have length `lengths[i]` and end with `nums[i]`.
  2.  When considering `nums[i]` and a previous `nums[j]` (where `nums[j] < nums[i]`):
      - If `nums[i]` forms a _new longer_ LIS using `nums[j]` (i.e., `lengths[j] + 1 > lengths[i]`):
        - Update `lengths[i] = lengths[j] + 1`.
        - The number of ways to form this new LIS ending at `i` is the same as the number of ways to form the LIS ending at `j`. So, `counts[i] = counts[j]`.
      - If `nums[i]` forms an LIS of the _same current max length_ for `i` using `nums[j]` (i.e., `lengths[j] + 1 == lengths[i]`):
        - `lengths[i]` doesn't change.
        - We've found _additional_ ways to achieve this length. So, `counts[i] += counts[j]`.
  3.  The final answer is the sum of `counts[k]` for all `k` where `lengths[k]` is equal to the overall maximum LIS length found.

---

**Template: Number of Longest Increasing Subsequences (LeetCode 673)**

```python
def find_number_of_lis(nums: list[int]) -> int:
    n = len(nums)
    if n == 0:
        return 0 # Why: No numbers, no LIS.

    # lengths[i]: Length of the LIS ending at nums[i].
    lengths = [1] * n # Why: Each element itself is an LIS of length 1.
    # counts[i]: Number of distinct LIS of length 'lengths[i]' that end at nums[i].
    counts = [1] * n  # Why: For an LIS of length 1 ending at nums[i], there's 1 way (just nums[i] itself).

    for i in range(n): # Current element we are considering as the end of an LIS.
        for j in range(i): # Previous element we are checking if it can come before nums[i].
            if nums[j] < nums[i]: # nums[i] can potentially extend an LIS ending at nums[j].
                potential_new_length_at_i = lengths[j] + 1

                # Scenario 1: Found a new, strictly longer LIS ending at nums[i].
                if potential_new_length_at_i > lengths[i]:
                    lengths[i] = potential_new_length_at_i
                    # Why counts[i] = counts[j]?
                    # All the distinct LIS that ended at nums[j] (of length lengths[j])
                    # can now be extended by nums[i] to form an LIS of this new 'lengths[i]'.
                    # The number of ways is inherited directly from nums[j].
                    counts[i] = counts[j]

                # Scenario 2: Found another way to achieve the current max LIS length for nums[i].
                elif potential_new_length_at_i == lengths[i]:
                    # Why counts[i] += counts[j]?
                    # We already knew how to make an LIS of length 'lengths[i]' ending at nums[i].
                    # Now, by using nums[j] before nums[i], we've found 'counts[j]' *additional*
                    # distinct ways to achieve this same length 'lengths[i]' ending at nums[i].
                    counts[i] += counts[j]
            # Else (nums[j] >= nums[i]): nums[j] cannot precede nums[i] in an *increasing* subsequence.

    if not lengths: # Should not happen if n > 0, but good for empty nums.
        return 0

    max_lis_length = 0
    # Find the overall maximum length of any LIS in the array.
    # max_lis_length = max(lengths) if lengths else 0 # Pythonic way
    for length in lengths:
        if length > max_lis_length:
            max_lis_length = length

    total_count_of_max_lis = 0
    # Sum the counts for all LIS that achieve this overall maximum length.
    for k in range(n):
        if lengths[k] == max_lis_length:
            total_count_of_max_lis += counts[k]

    return total_count_of_max_lis
```

**Explanation of `find_number_of_lis` Specifics:**

- `lengths = [1] * n`, `counts = [1] * n`:
  - Base case: Each element `nums[i]` itself is an LIS of length 1, and there's 1 way to form it.
- Outer loop `for i in range(n)`: Iterates through each element `nums[i]`, which we are trying to determine `lengths[i]` and `counts[i]` for.
- Inner loop `for j in range(i)`: Iterates through all elements `nums[j]` that come before `nums[i]`.
- `if nums[j] < nums[i]`: Standard LIS condition – `nums[i]` can follow `nums[j]`.
- `if potential_new_length_at_i > lengths[i]`:
  - This is a _better_ (longer) LIS ending at `nums[i]`.
  - `lengths[i]` is updated.
  - `counts[i]` is set to `counts[j]`. Any previous ways of counting for `nums[i]` (which were for a shorter LIS) are now irrelevant for _this specific `lengths[i]`_.
- `elif potential_new_length_at_i == lengths[i]`:
  - This path provides an LIS ending at `nums[i]` of the _same length_ as what we've already found to be the maximum for `nums[i]`.
  - `counts[i]` is incremented by `counts[j]` because we've found `counts[j]` _new, distinct paths_ to achieve this `lengths[i]` for `nums[i]`.
- `max_lis_length = max(lengths) if lengths else 0`: Finds the global maximum LIS length.
- `total_count_of_max_lis = sum(...)`: Iterates through the `lengths` array. If `lengths[k]` is equal to the `max_lis_length`, it means `nums[k]` can be the end of an overall LIS. We add `counts[k]` (the number of ways this LIS ending at `nums[k]` can be formed) to our final sum.

---

- **Example Problems:**
  - [LeetCode 673: Number of Longest Increasing Subsequence](https://leetcode.com/problems/number-of-longest-increasing-subsequence/)
- **Complexity:**
  - Time: O(N^2) - Due to the nested loops.
  - Space: O(N) - For the `lengths` and `counts` arrays.
- **Important Considerations:**
  - The distinction between the `>` and `==` conditions when updating `lengths` and `counts` is crucial.
  - This O(N^2) approach is standard. An O(N log N) solution exists but is much more complex, typically involving segment trees or Fenwick trees to query sums of counts for subsequences of a certain length ending with values less than `nums[i]`.

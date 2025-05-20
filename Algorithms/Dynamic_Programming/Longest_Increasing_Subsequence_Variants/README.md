# Longest Increasing Subsequence (LIS) Variants

**Core Idea:** The Longest Increasing Subsequence problem involves finding the length of the longest subsequence of a given sequence such that all elements of the subsequence are sorted in strictly increasing order. This is a classic dynamic programming problem with several interesting variations and applications.

**General Problem Statement:**
Given an array `arr` of `n` numbers, find the length of the longest subsequence such that for any two elements `arr[i]` and `arr[j]` in the subsequence, if `i < j` in their original positions in `arr`, then `arr[i] < arr[j]` when they appear in the subsequence. (Note: This definition is a bit loose. The standard LIS definition is about the values of the elements, not their original indices necessarily, as long as they maintain relative order from the original sequence). More accurately: find a subsequence `a_i1, a_i2, ..., a_ik` such that `i1 < i2 < ... < ik` and `a_i1 < a_i2 < ... < a_ik`, and `k` is maximized.

**Key DP Approaches for LIS:**

1.  **O(N^2) DP Approach:**

    - **State:** `dp[i]` usually represents the length of the LIS ending at index `i` (i.e., `arr[i]` is the last element of this LIS).
    - **Transition:** To compute `dp[i]`, iterate through all `j < i`. If `arr[i] > arr[j]`, then `arr[i]` can extend the LIS ending at `arr[j]`. So, `dp[i] = max(dp[i], 1 + dp[j])`. The base case for `dp[i]` is 1 (the element `arr[i]` itself forms an LIS of length 1).
    - **Final Answer:** The maximum value in the `dp` array.

2.  **O(N log N) Patience Sorting / Binary Search Approach:**
    - **Core Idea:** Maintain a sequence (often called `tails` or `LIS_piles`) which stores the smallest tail of all active increasing subsequences of a certain length. Specifically, `tails[k]` would be the smallest ending element of an increasing subsequence of length `k+1`. This `tails` array will always be sorted.
    - **Process:** For each number `num` in the input array:
      - If `num` is greater than all elements in `tails`, append `num` to `tails`. This extends the longest LIS found so far.
      - Otherwise, find the smallest element in `tails` that is greater than or equal to `num` (using binary search, e.g., `bisect_left`) and replace it with `num`. This means we found a way to achieve an existing LIS length with a smaller ending element, which is potentially better for future extensions.
    - **Final Answer:** The length of the `tails` array.
    - **Note:** This approach directly gives the _length_ of the LIS. Reconstructing the actual LIS path is more complex with this method but possible.

**When to Suspect an LIS-style Problem:**

- The problem asks for the "longest subsequence" with a specific ordering or divisibility property.
- The problem involves selecting items where the selection of one item depends on the properties of a previously selected item in a cumulative way (e.g., increasing value, divisibility, fitting one item into another).
- Sorting the input array first is often a helpful (or required) preprocessing step.
- The constraints might allow for O(N^2) or require O(N log N).

# This section will cover various LIS patterns, from finding the basic length to reconstructing the path, and applying LIS to seemingly different problems.

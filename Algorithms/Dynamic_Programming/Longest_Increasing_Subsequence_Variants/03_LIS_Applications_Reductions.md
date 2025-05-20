**Pattern 3: LIS - Applications and Reductions**

- **Problem Statement:** Many problems don't explicitly ask for an LIS but can be transformed or reduced to an LIS problem after some preprocessing (often sorting by one dimension and then finding LIS on another).
- **Keywords:** Problems involving selecting items based on two criteria where one must increase if the other is fixed/sorted, "nesting" problems, "chaining" problems.
- **Core Idea:**
  1.  **Identify the dimensions:** Determine the properties of the items (e.g., width and height for envelopes, start and end for pairs).
  2.  **Sort:** Sort the items based on one dimension. If there are ties in the primary sorting dimension, a secondary sorting criterion (often in _descending_ order for the dimension LIS will be applied to) is crucial to prevent incorrect LIS grouping.
  3.  **Apply LIS:** Perform LIS on the second dimension of the sorted items. The O(N log N) LIS length algorithm is often used here for efficiency.

---

**Template: Problem Reduction to LIS (e.g., Russian Doll Envelopes)**

```python
from bisect import bisect_left

# General structure for problems reducible to LIS
# def solve_reducible_to_lis(items: list[tuple_or_list_of_attributes]) -> int:
#     n = len(items)
#     if n == 0:
#         return 0

#     # 1. Sort the items:
#     #    - Primarily by the first dimension (e.g., width) in ascending order.
#     #    - Secondarily by the second dimension (e.g., height) in *descending* order if ties in first.
#     #      Why descending for secondary sort? If widths are equal (w1 == w2),
#     #      we CANNOT pick both (h1, h2) if h1 < h2 to form an increasing sequence of heights.
#     #      Sorting heights in descending order for same widths ensures that if we pick an envelope (w, h_large),
#     #      another envelope (w, h_small) appearing later in the sorted list won't be incorrectly
#     #      considered as part of an increasing height sequence originating from (w, h_large),
#     #      because h_small < h_large.
#     #      Example: [(3,5), (3,4)]. If LIS is on height, sorted [(3,5), (3,4)] ensures 4 is not chosen after 5.
#     #               If sorted [(3,4), (3,5)], LIS on height might pick 4 then 5, which is wrong for nesting same-width.
#     # items.sort(key=lambda x: (x[0], -x[1])) # Example for 2D items (attribute1, attribute2)

#     # 2. Extract the dimension on which LIS needs to be performed.
#     #    After sorting, we only care about the second dimension (e.g., heights).
#     # second_dimensions = [item[1] for item in items]

#     # 3. Apply LIS (O(N log N) version is common) on this extracted dimension.
#     # tails = []
#     # for val in second_dimensions:
#     #     if not tails or val > tails[-1]:
#     #         tails.append(val)
#     #     else:
#     #         idx = bisect_left(tails, val)
#     #         tails[idx] = val
#     # return len(tails)
```

**Example: Russian Doll Envelopes (LeetCode 354)**

- **Problem:** Given a list of `envelopes` where `envelopes[i] = [w_i, h_i]`, find the maximum number of envelopes you can "Russian doll" (put one inside another). An envelope `A` can fit into `B` if `A.width < B.width` and `A.height < B.height`.

```python
from bisect import bisect_left

class Solution: # For LeetCode structure
    def maxEnvelopes(self, envelopes: list[list[int]]) -> int:
        n = len(envelopes)
        if n == 0:
            return 0

        # Sort envelopes:
        # - Primarily by width (envelopes[i][0]) in ascending order.
        # - Secondarily by height (envelopes[i][1]) in *descending* order.
        # Why this sorting?
        # Ascending width: Ensures that if we pick envelope B after A, B's width is >= A's width.
        #                The LIS condition (on heights) will handle the strict inequality for heights.
        # Descending height for ties in width: If two envelopes have the same width (w1=w2),
        # say (w, h1) and (w, h2) with h1 > h2. Sorting puts (w, h1) before (w, h2).
        # When we run LIS on heights, if we pick (w,h1), then (w,h2) cannot be picked next because h2 < h1.
        # This correctly prevents nesting two envelopes of the same width, as the problem implies
        # strict inequality for both dimensions for nesting (A.w < B.w AND A.h < B.h).
        # If we sorted heights ascendingly for same widths, e.g. (w,h2) then (w,h1), LIS on heights
        # might pick h2 then h1, implying (w,h2) can fit in (w,h1) based on heights, which is
        # disallowed by width condition.
        envelopes.sort(key=lambda x: (x[0], -x[1]))

        # Now, we only need to find the Longest Increasing Subsequence of the heights.
        # The heights are envelopes[i][1].
        heights = [] # This will be our 'tails' array for the N log N LIS algorithm.

        for _, h in envelopes: # Iterate through sorted envelopes, only considering height 'h'.
            # Find the insertion point for 'h' in 'heights' (which is kept sorted).
            # bisect_left returns an index 'idx' such that all heights[j] for j < idx are < h,
            # and all heights[j] for j >= idx are >= h.
            idx = bisect_left(heights, h)

            if idx == len(heights):
                # 'h' is greater than all current elements in 'heights'.
                # This means 'h' can extend the longest increasing subsequence of heights found so far.
                heights.append(h)
            else:
                # 'h' can replace heights[idx]. This means we found an increasing
                # subsequence of length (idx + 1) that ends with 'h', and 'h' <= previous heights[idx].
                # Using a smaller or equal height for the same LIS length is always better or same.
                heights[idx] = h

        # The length of the 'heights' list (our 'tails' array) is the length of the LIS of heights,
        # which corresponds to the maximum number of Russian doll envelopes.
        return len(heights)

```

**Explanation of `maxEnvelopes` Specifics:**

- `envelopes.sort(key=lambda x: (x[0], -x[1]))`:
  - `x[0]`: Sort by width (ascending).
  - `-x[1]`: For ties in width, sort by height in _descending_ order. This is the critical trick. If we have `(w, h_a)` and `(w, h_b)`, and we sort them to process `(w, h_large)` then `(w, h_small)`, our LIS on heights will not pick `h_small` after `h_large` because `h_small < h_large`. This correctly models that envelopes of the same width cannot be nested.
- `heights = []`: This list will act as the `tails` array from the O(N log N) LIS algorithm, storing the smallest ending height for an increasing subsequence of heights of a certain length.
- `for _, h in envelopes:`: We iterate through the sorted envelopes. We only care about the height `h` for the LIS calculation because the width condition is implicitly handled by the primary sort and the LIS property (if we pick a height `h_j` for envelope `j` which came after envelope `i` in the sorted list, then `width_j >= width_i`. The LIS on heights `h_j > h_i` along with `width_j > width_i` (which happens if `width_j != width_i` due to primary sort) gives the nesting).
- `idx = bisect_left(heights, h)`: Find where `h` would fit in the sorted `heights` list.
- `if idx == len(heights): heights.append(h)`: If `h` is larger than all heights in `tails`, it extends the LIS.
- `else: heights[idx] = h`: Otherwise, `h` replaces an existing height in `tails` to form an LIS of the same length `idx+1` but with an equal or smaller ending element. This is the standard N log N LIS update step.
- `return len(heights)`: The length of `tails` (here `heights`) is the length of the LIS.

---

- **Example Problems:**

  - [LeetCode 354: Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/)
  - [LeetCode 646: Maximum Length of Pair Chain](https://leetcode.com/problems/maximum-length-of-pair-chain/)
    - **Adaptation:** A pair `(a, b)` can follow `(c, d)` if `c < a` (and `d < b`, but problem usually means `b < c`). Sort pairs by their first element, or by their second element. If sorting by `pair[0]`, LIS on `pair[1]` (if condition is `b < c`, then sort by `pair[1]` and LIS on `pair[0]` looking for `pair[0]_prev < pair[0]_curr` is tricky. Simpler: Sort by `pair[1]`. Then iterate. If `current_pair[0] > previous_chain_end_pair[1]`, extend chain. This is more greedy than LIS, but often related.)
    - For Pair Chain `[[a,b],[c,d]]` where chain means `b < c`: Sort by `b` (the end value of a pair). Then iterate. `dp[i]` = max length of chain ending with `pairs[i]`. `dp[i] = 1 + max(dp[j])` for `j < i` where `pairs[j][1] < pairs[i][0]`. This is a direct N^2 LIS-style DP.
    - Alternatively, sort by `pairs[i][0]`. Then LIS on `pairs[i][1]` with a condition. (This needs careful thought).
    - The most common solution for Max Length Pair Chain is: Sort pairs by their _second element_. Then iterate greedily. Pick the first pair. Then pick the next pair `(c,d)` such that `c` is greater than the second element of the previously picked pair. This greedy approach works.
    - To frame it as LIS: Sort by the first element `p[0]`. Then, you are looking for an LIS on the second elements `p[1]`, but with the constraint that for `p_i = (a,b)` and `p_j = (c,d)` where `p_i` comes before `p_j` in sorted list (so `a <= c`), you need `b < c` for `p_j` to follow `p_i`. If `a==c`, they can't chain. If `a < c`, then LIS on `p[1]` such that `p_j[1]` is picked only if `p_i[1] < p_j[0]`. This is not direct LIS on `p[1]`. The Russian Doll custom sort is more directly LIS.

- **Complexity:**
  - Time: O(N log N) - Dominated by sorting. The LIS part is also O(N log N).
  - Space: O(N) - For storing the dimension for LIS (e.g., `heights` or `tails` array).
- **Important Considerations:**
  - The sorting strategy is **critical** and problem-dependent, especially the secondary sort key for handling ties in the primary dimension.
  - Understand _why_ a particular sorting order works for reducing the problem to LIS on one of the dimensions. The goal is usually to make the LIS condition on one dimension automatically satisfy (or correctly restrict) the conditions on other dimensions.

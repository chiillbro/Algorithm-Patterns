**Pattern: House Robber Variation - Delete and Earn**

- **Problem Statement:** Given an array `nums`, you can pick any `nums[i]` to earn `nums[i]` points. Doing so deletes `nums[i]`, and also every element equal to `nums[i]-1` and `nums[i]+1`. Maximize points.
- **Keywords:** "delete and earn", "pick one, affects neighbors", "maximize sum with restrictions".
- **Core Idea (Reduction to House Robber):**
  1.  **Preprocessing - Aggregate Points:** The problem involves numbers, not their indices in the original array. First, count the occurrences of each number. The total points you get by "activating" a number `x` is `x * count[x]`.
  2.  **Sort Unique Numbers:** Get a sorted list of unique numbers present in the input.
  3.  **House Robber Analogy:** Iterate through the sorted unique numbers. For each number `num`, you have two choices:
      - **"Rob" this house (`num`):** Earn `num * count[num]` points. You cannot "rob" the house `num-1` if it existed and was the immediately preceding house.
      - **"Skip" this house (`num`):** Earn 0 points from `num`. You could have "robbed" `num-1`.
  4.  **DP State:** Use two variables to track the maximum points:
      - `take_current`: Max points if we _take_ the current number.
      - `skip_current`: Max points if we _skip_ the current number.
        These are updated based on `take_previous` and `skip_previous`.

---

**Template: Delete and Earn (LeetCode 740)**

```python
from collections import Counter

def delete_and_earn(nums: list[int]) -> int:
    if not nums:
        return 0 # Why: No numbers, no points.

    # 1. Preprocessing: Aggregate points for each number.
    points_map = Counter()
    for num in nums:
        points_map[num] += num # Or: counts = Counter(nums); points_map[num] = num * counts[num]

    # Alternative and often clearer preprocessing:
    # counts = Counter(nums)
    # max_val = 0
    # for num in nums: # Find max value to create an array up to it
    #     if num > max_val:
    #         max_val = num
    #
    # aggregated_points = [0] * (max_val + 1)
    # for num, count in counts.items():
    #    aggregated_points[num] = num * count
    #
    # Now, iterate through aggregated_points like House Robber.
    # This avoids sorting unique keys and handling non-adjacent elements explicitly if
    # aggregated_points[i-1] is 0, it means number i-1 wasn't there or yielded 0 points.

    # Using the sorted unique numbers approach from the provided solution:
    unique_sorted_nums = sorted(points_map.keys())

    if not unique_sorted_nums: # Should not happen if nums is not empty, but defensive.
        return 0

    # DP variables:
    # take_prev_num: Max points if the PREVIOUS number processed was TAKEN.
    # skip_prev_num: Max points if the PREVIOUS number processed was SKIPPED.
    # Initialize for a state "before the first number".
    take_prev_num = 0
    skip_prev_num = 0

    last_processed_num = -1 # Initialize to a value that won't be adjacent to the first number.

    for current_num in unique_sorted_nums:
        current_num_points = points_map[current_num] # Total points if we pick current_num

        # Max points we could have accumulated *before* considering current_num
        max_points_before_current = max(take_prev_num, skip_prev_num)

        # Option 1: Take the current_num
        # If current_num is adjacent to last_processed_num (e.g., current=4, last=3),
        # we *must* have skipped last_processed_num.
        if last_processed_num == current_num - 1:
            # Points from taking current_num + max points from *skipping* the previous one.
            points_if_take_current = current_num_points + skip_prev_num
        else:
            # Not adjacent, so we can take current_num and add the best score from before.
            # Points from taking current_num + max points from *either taking or skipping* previous one.
            points_if_take_current = current_num_points + max_points_before_current

        # Option 2: Skip the current_num
        # If we skip current_num, our score is simply the best we could do up to the previous number.
        points_if_skip_current = max_points_before_current

        # Update for the next iteration:
        # The old 'points_if_take_current' becomes the new 'take_prev_num'
        # The old 'points_if_skip_current' becomes the new 'skip_prev_num'
        take_prev_num = points_if_take_current
        skip_prev_num = points_if_skip_current

        last_processed_num = current_num

    return max(take_prev_num, skip_prev_num) # Final answer is max of taking or skipping the last number.

```

**Explanation of `delete_and_earn` (using the logic in the template above, slightly rephrased from original solution for clarity):**

- **Preprocessing (`points_map` or `aggregated_points`):**
  - The goal is to transform `[2,2,3,3,3,4]` into something like:
    - Number 2 can give `2*2=4` points.
    - Number 3 can give `3*3=9` points.
    - Number 4 can give `4*1=4` points.
  - The `sorted(points_map.keys())` or iterating through `aggregated_points` gives us an ordered sequence to apply House Robber logic.
- **DP Variables `take_prev_num`, `skip_prev_num`:**
  - These track the maximum scores achievable ending at the _previously processed unique number_, under the conditions of taking or skipping it.
  - `last_processed_num`: Helps determine adjacency.
- **Loop through `unique_sorted_nums` (or `aggregated_points` indices):**
  - `current_num_points`: The points earned if `current_num` is chosen.
  - `max_points_before_current = max(take_prev_num, skip_prev_num)`: This is the best score we could have obtained _just before_ making a decision about `current_num`.
- **Decision for `current_num`:**
  - `points_if_take_current`:
    - If `current_num` is adjacent to `last_processed_num` (e.g., 3 then 4): To take 4, we _must_ have skipped 3. So, `points_if_take_current = (points for 4) + skip_prev_num` (where `skip_prev_num` was the score from skipping 3).
    - If `current_num` is NOT adjacent (e.g., 2 then 4): We can take 4, and it doesn't conflict with taking 2. So, `points_if_take_current = (points for 4) + max_points_before_current` (best score ending before 4, which might have involved taking 2).
  - `points_if_skip_current`: If we skip `current_num`, we simply carry forward the `max_points_before_current`.
- **Updates for Next Iteration:**
  - The calculated `points_if_take_current` becomes `take_prev_num` for the next number.
  - The calculated `points_if_skip_current` becomes `skip_prev_num` for the next number.
  - `last_processed_num` is updated.
- **Return `max(take_prev_num, skip_prev_num)`:** After iterating through all numbers, these variables hold the scores if the _last_ unique number was taken or skipped. The maximum of these is the answer.

**Alternative House Robber DP array approach (often easier to grasp initially):**
If using `aggregated_points = [0, 0, 4, 9, 4]` (for numbers 0, 1, 2, 3, 4)

```python
# aggregated_points[i] = total points from number i
# dp[i] = max points considering numbers up to i
# dp[i] = max(dp[i-1], aggregated_points[i] + dp[i-2])

# dp = [0] * (max_val + 1)
# dp[0] = aggregated_points[0] # Though usually numbers start from 1
# if max_val >= 1:
#     dp[1] = max(aggregated_points[0], aggregated_points[1])
# for i in range(2, max_val + 1):
#     dp[i] = max(dp[i-1],                # Skip house i
#                 aggregated_points[i] + dp[i-2]) # Take house i (and points from i-2)
# return dp[max_val]
```

The O(1) space `take`/`skip` solution is an optimization of this array-based DP.

---

- **Example Problems:**
  - [LeetCode 740: Delete and Earn](https://leetcode.com/problems/delete-and-earn/)
  - [LeetCode 198: House Robber](https://leetcode.com/problems/house-robber/) (The base pattern)
  - [LeetCode 213: House Robber II](https://leetcode.com/problems/house-robber-ii/) (Circular arrangement)
- **Complexity (for the O(1) space solution with sorted unique keys):**
  - Time: O(N + K log K) or O(N + M)
    - O(N) to build the `points_map` (or `counts`).
    - O(K log K) to sort `K` unique keys. (If `K` is number of unique elements)
    - O(K) to iterate through unique keys.
    - If using the `aggregated_points` array up to `max_val` (M): O(N) to build `counts`, O(M) to build `aggregated_points`, O(M) for DP. So O(N+M).
    - Constraints: N up to 2\*10^4, values up to 10^4. So K <= N, M <= 10^4.
    - The sort dominates if K is large. Iterating up to `max_val` dominates if `max_val` is large relative to K. Both are efficient enough.
  - Space: O(K) or O(M)
    - O(K) for `points_map` and `unique_sorted_nums`.
    - O(M) for `aggregated_points` array.
    - The DP itself is O(1) space (just `take`, `skip`).
- **Important Considerations:**
  - The key is recognizing the transformation to a sequence where choosing an item makes its immediate predecessor invalid.
  - The choice of preprocessing (sorted unique keys vs. full `aggregated_points` array up to `max_val`) depends on the distribution of numbers and `max_val`. If `max_val` is huge but there are few unique numbers, sorted keys are better. If numbers are dense, the array is fine. The provided solution's `sorted(count.keys())` is robust.

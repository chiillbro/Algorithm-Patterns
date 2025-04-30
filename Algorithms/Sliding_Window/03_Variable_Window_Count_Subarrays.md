**Pattern 3: Variable-Size Window - Count Subarrays (Satisfying Condition)**

*   **Keywords:** "number of subarrays", "count subarrays", "satisfying condition X". Often involves conditions like "sum < target", "product < target", "at most k distinct".
*   **Core Idea:** Similar to Pattern 2, expand with `right`, shrink with `left` when the condition is violated. The key difference is how the result is updated. When the window `[left..right]` is valid, *all* subarrays ending at `right` and starting at or after `left` are also valid.
*   **Template (The "Add Window Size" Trick):**
    ```python
    def variable_window_count_subarrays(arr, condition_func):
        n = len(arr)
        left = 0
        count = 0
        # window_state = ... # Initialize state (sum, freq_map, count, etc.)

        for right in range(n):
            # 1. Expand window: Update state with arr[right]
            # window_sum += arr[right]
            # freq_map[arr[right]] += 1

            # 2. Shrink window: While the window violates the condition...
            while not condition_func(window_state): # Or condition_is_violated(window_state)
                # Remove arr[left]'s contribution from state
                # window_sum -= arr[left]
                # freq_map[arr[left]] -= 1
                # if freq_map[arr[left]] == 0: del freq_map[arr[left]]
                left += 1 # Move left pointer

            # 3. Update result: Now window [left..right] is valid.
            # ALL subarrays ending at 'right' and starting from 'left' onwards are valid.
            # These are: arr[left..right], arr[left+1..right], ..., arr[right..right]
            # There are (right - left + 1) such subarrays.
            count += (right - left + 1)

        return count
    ```
*   **Example Problems:**
    *   Number of Subarrays with Bounded Maximum (LeetCode 795 - Can be solved this way or others)
    *   Subarrays with K Different Integers (LeetCode 992 - Use this template with the "At Most K" trick, see next)
    *   Number of subarrays with product less than K (LeetCode 713)
*   **Complexity:** O(N) time, O(1) or O(k) space.
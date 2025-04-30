**Pattern 2: Variable-Size Window - Find Max/Min Length**

*   **Keywords:** "longest subarray/substring", "smallest subarray/substring", "maximum length", "minimum window", "at most k distinct", "sum >= target".
*   **Core Idea:** Expand the window by moving the `right` pointer. If the window violates a condition, shrink it from the `left` until it becomes valid again. Update the max/min length whenever the window is valid.
*   **Template:**
    ```python
    def variable_window_max_min_length(arr, condition_func):
        n = len(arr)
        left = 0
        max_len = 0 # Or min_len = float('inf')
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

            # 3. Update result: Now the window [left..right] is valid (or minimal valid)
            # Update max_len or min_len based on the current valid window size
            current_len = right - left + 1
            max_len = max(max_len, current_len)
            # min_len = min(min_len, current_len) # Often updated inside the shrink loop for minimal problems

        return max_len # Or min_len
    ```
*   **Example Problems:**
    *   Longest Substring Without Repeating Characters (LeetCode 3)
    *   Longest Substring with At Most K Distinct Characters (LeetCode 340)
    *   Minimum Size Subarray Sum (LeetCode 209)
    *   Minimum Window Substring (LeetCode 76 - this problem often needs careful state management)
*   **Complexity:** O(N) time (each element enters and leaves the window at most once), O(1) or O(k) space.
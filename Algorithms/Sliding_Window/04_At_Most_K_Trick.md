**Pattern 4: The "At Most K" Trick (for Exactly K)**

*   **Keywords:** "exactly k distinct", "exactly k occurrences", "number of subarrays with exactly k...".
*   **Core Idea:** It's often hard to directly maintain a window with *exactly* `k` items (distinct chars, specific values, etc.). Instead, calculate the count for "at most k" items and subtract the count for "at most k-1" items. `exactly(k) = atMost(k) - atMost(k-1)`.
*   **Template:**
    ```python
    # Helper function using Pattern 3 Template
    def count_at_most_k(arr, k):
        n = len(arr)
        left = 0
        count = 0
        # window_state = ... # e.g., freq_map = defaultdict(int)

        for right in range(n):
            # 1. Expand window: Update state
            # freq_map[arr[right]] += 1

            # 2. Shrink window: While condition for 'at most k' is violated
            # (e.g., number of distinct elements > k)
            while len(freq_map) > k: # Example condition
                # Remove arr[left]'s contribution
                # freq_map[arr[left]] -= 1
                # if freq_map[arr[left]] == 0:
                #     del freq_map[arr[left]]
                left += 1

            # 3. Update result: Add count of valid subarrays ending at right
            count += (right - left + 1)

        return count

    # Main function
    def count_exactly_k(arr, k):
        if k < 0: return 0 # Handle edge cases if necessary
        return count_at_most_k(arr, k) - count_at_most_k(arr, k - 1)
    ```
*   **Example Problems:**
    *   Subarrays with K Different Integers (LeetCode 992 - Classic example)
    *   Count Number of Nice Subarrays (LeetCode 1248 - Count odd numbers instead of distinct)
*   **Complexity:** O(N) time (calls the O(N) helper twice), O(1) or O(k) space.
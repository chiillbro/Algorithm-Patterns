**Pattern 1: Fixed-Size Sliding Window**

*   **Keywords:** "subarray of size k", "substring of length k", "fixed size k", "find max/min/average/property in all subarrays of size k".
*   **Core Idea:** Maintain a window of exactly `k` elements. For each step, add the new element at the right and remove the element at the left, updating the window's property (sum, hash, etc.) efficiently.
*   **Template:**
    ```python
    def fixed_size_window(arr, k):
        n = len(arr)
        if n < k:
            return # Or appropriate return value like 0, [], None

        # Initialize window state for the first k elements (arr[0...k-1])
        window_sum = 0 # Example: Sum
        # other_state = ... # e.g., frequency map, hash value
        for i in range(k):
            window_sum += arr[i]
            # update other_state

        # Initialize result based on the first window
        result = window_sum # Example: Max sum
        # process_first_window(window_sum, other_state) -> update result

        # Slide the window from k to n-1
        for right in range(k, n):
            # 1. Add the new element entering the window
            window_sum += arr[right]
            # update other_state using arr[right]

            # 2. Remove the element leaving the window
            left_element = arr[right - k]
            window_sum -= left_element
            # update other_state removing left_element

            # 3. Process the current window / Update result
            # result = max(result, window_sum) # Example: Max sum
            # result = min(result, window_average)
            # if check_property(other_state): result += 1
            # update_result(result, window_sum, other_state)

        return result
    ```
*   **Example Problems:**
    *   Maximum Sum Subarray of Size K (LeetCode 643 variation)
    *   Find all anagrams of a string `p` in `s` (LeetCode 438 - uses frequency maps in the window state)
*   **Complexity:** O(N) time, O(1) or O(k) space (k for frequency maps).
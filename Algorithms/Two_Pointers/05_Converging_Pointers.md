**Pattern: Two Pointers - Converging (Usually on Sorted Array)**

*   **Keywords:** "sorted array", "find pair", "sum equals target", "two sum", "three sum", "remove duplicates", "palindrome".
*   **Core Idea:** Use two pointers, one starting at the beginning (`left`) and one at the end (`right`) of the array/string. Move them towards each other based on comparisons or conditions.
*   **Template (Find Pair with Target Sum):**
    ```python
    def two_pointers_converging_sum(sorted_arr, target):
        left = 0
        right = len(sorted_arr) - 1
        while left < right:
            current_sum = sorted_arr[left] + sorted_arr[right]
            if current_sum == target:
                # Found a pair!
                # return [left, right] or [sorted_arr[left], sorted_arr[right]] or count += 1
                # Decide whether to continue searching (e.g., move both pointers)
                left += 1
                right -= 1
            elif current_sum < target:
                # Sum is too small, need larger value, move left pointer right
                left += 1
            else: # current_sum > target
                # Sum is too large, need smaller value, move right pointer left
                right -= 1
        # If loop finishes without finding, return appropriate value (e.g., [], False, 0)
        return False # Example: Pair not found
    ```
*   **Example Problems:**
    *   Two Sum II - Input Array Is Sorted (LeetCode 167)
    *   3Sum (LeetCode 15 - often involves sorting then using this pattern in a loop)
    *   Valid Palindrome (LeetCode 125)
    *   Container With Most Water (LeetCode 11)
*   **Complexity:** O(N) time (pointers traverse the array once), O(1) extra space (if sorting not needed or done in-place). O(N log N) if sorting is required first.
# KMP - Knuth-Morris-Pratt Algorithm

## 1. Core Idea / Intuition

KMP is a linear-time string searching algorithm that efficiently finds occurrences of a pattern `P` within a text `T`. It avoids redundant comparisons by utilizing information about the pattern itself. When a mismatch occurs after `j` characters have matched, KMP uses a precomputed "Longest Proper Prefix which is also Suffix" (LPS) array to determine the maximum safe shift of the pattern, rather than simply shifting by one.

## 2. Key Concepts / Components

*   **LPS Array (Longest Proper Prefix which is also Suffix):**
    *   An array `lps` of the same length as the pattern `P`.
    *   `lps[i]` stores the length of the longest *proper* prefix of `P[0...i]` that is *also* a suffix of `P[0...i]`.
    *   A "proper" prefix is not the entire string itself.
    *   This array tells us the length of the prefix of `P` that we know *already matches* the text ending just before the mismatch point.
    *   **Example:** For `P = "abab"` -> `lps = [0, 0, 1, 2]`
        *   `lps[0] = 0` ("a")
        *   `lps[1] = 0` ("ab", proper prefixes: "a"; suffixes: "b")
        *   `lps[2] = 1` ("aba", proper prefixes: "a", "ab"; suffixes: "a", "ba". Match: "a")
        *   `lps[3] = 2` ("abab", proper prefixes: "a", "ab", "aba"; suffixes: "b", "ab", "bab". Match: "ab")

## 3. Algorithm Steps

1.  **Preprocessing:** Compute the `lps` array for the pattern `P`. (O(m) time, where m = len(P)).
2.  **Searching:**
    *   Use two pointers: `i` for the text `T` and `j` for the pattern `P`.
    *   While `i < len(T)`:
        *   If `T[i] == P[j]`: Increment both `i` and `j`.
        *   If `j == len(P)`: A match is found starting at index `i - j` in `T`. To find further occurrences, reset `j` using the LPS array: `j = lps[j - 1]`.
        *   If `T[i] != P[j]`:
            *   If `j != 0`: A mismatch occurred after some matches. Fall back using the LPS array: `j = lps[j - 1]`. **Do not increment `i`**. This effectively shifts the pattern based on the longest prefix-suffix match.
            *   If `j == 0`: Mismatch at the first character of the pattern. Increment `i`.

## 4. Python Template

```python
def compute_lps(pattern: str) -> list[int]:
    """Computes the LPS array for KMP."""
    m = len(pattern)
    lps = [0] * m
    length = 0  # Length of the previous longest prefix suffix
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                # Fall back: try the next shorter prefix suffix
                length = lps[length - 1]
                # Note: Do NOT increment i here
            else:
                # No prefix suffix ending at pattern[i]
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text: str, pattern: str) -> list[int]:
    """
    Performs KMP search of pattern within text.
    Returns a list of starting indices of all occurrences.
    """
    n = len(text)
    m = len(pattern)
    if m == 0:
        return list(range(n + 1)) # Or handle as needed
    if n == 0 or m > n:
        return []

    lps = compute_lps(pattern)
    matches = []
    i = 0  # index for text
    j = 0  # index for pattern

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            # Match found starting at index i - j
            matches.append(i - j)
            # Important: Use LPS to shift pattern for next potential match
            j = lps[j - 1]

        # Mismatch after j matches
        elif i < n and pattern[j] != text[i]:
            # Do not match lps[0..lps[j-1]] characters, they will match anyway.
            if j != 0:
                j = lps[j - 1] # Use LPS array to find next state
            else:
                # Mismatch at the very beginning of the pattern
                i += 1
    return matches
```

## 5. How to Use for Pattern Matching

1.  Call `kmp_search(text, pattern)`.
2.  The returned list contains the 0-based starting indices of all occurrences of `pattern` in `text`.

## 6. Application to "Repeated String Match" Problem

*Problem: Find min repeats `k` of `a` such that `b` is a substring of `a * k`.*

```python
# (Assuming compute_lps and kmp_search are defined as above)
class Solution:
    def repeatedStringMatch(self, a: str, b: str) -> int:
        len_a, len_b = len(a), len(b)
        if len_b == 0: return 0

        # Determine max repetitions needed for the search text
        k_base = (len_b - 1) // len_a
        max_reps_to_check = k_base + 2
        T = a * max_reps_to_check
        len_T = len(T)

        if len_b > len_T: return -1 # Optimization if b is already too long

        # Use KMP to find the first occurrence
        lps = self._compute_lps(b) # Assuming methods are part of the class
        matches = self._kmp_search_first(T, b, lps) # Need a variant returning first match index or -1

        if not matches: # Or if kmp_search_first returns -1
            return -1
        else:
            match_index = matches[0] # Or the index returned directly
            # Calculate the minimum k needed to cover this match
            required_k = (match_index + len_b + len_a - 1) // len_a
            return required_k

    def _compute_lps(self, pattern: str) -> list[int]:
        # ... (implementation from template) ...
        m = len(pattern)
        lps = [0] * m
        length = 0
        i = 1
        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    def _kmp_search_first(self, text: str, pattern: str, lps: list[int]) -> list[int]:
        # Simplified search returning only the first match index
        n = len(text)
        m = len(pattern)
        matches = [] # Only need the first one
        i = 0
        j = 0
        while i < n:
            if pattern[j] == text[i]:
                i += 1
                j += 1
            if j == m:
                matches.append(i - j)
                return matches # Return immediately on first match
                # j = lps[j - 1] # Not needed if only finding first
            elif i < n and pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        return matches # Return empty list if no match
```

## 7. Complexity Analysis

*   **Preprocessing (LPS Array):** O(m), where m = len(pattern)
*   **Searching:** O(n), where n = len(text)
*   **Total Time:** O(n + m)
*   **Space Complexity:** O(m) for the LPS array.

## 8. When to Use / Trade-offs

*   **Use:** Excellent for finding single or multiple occurrences of a pattern in a text when guaranteed linear time is required. Standard and widely applicable.
*   **Trade-offs:** Requires O(m) preprocessing time and O(m) space for the LPS array. Might be slightly more complex to implement initially compared to naive search or sometimes Rabin-Karp.

## 9. Example Problems

*   LeetCode 28: Find the Index of the First Occurrence in a String
*   LeetCode 1392: Longest Happy Prefix (Directly uses LPS)
*   LeetCode 214: Shortest Palindrome (Uses KMP logic)
*   Finding all occurrences of a pattern in text.
*   String periodicity problems.
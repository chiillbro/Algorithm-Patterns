# Z-Algorithm

## 1. Core Idea / Intuition

The Z-Algorithm processes a string `S` to create a Z-array. `Z[i]` stores the length of the longest substring starting from `S[i]` that is *also a prefix* of `S`. This array can be computed in linear time. For pattern matching, we construct a combined string `S = P + $ + T` (where `P` is the pattern, `T` is the text, and `$` is a unique separator). If `Z[i]` equals the length of `P` for an index `i` corresponding to a position within `T`, it signifies an occurrence of `P` starting at that position in `T`.

## 2. Key Concepts / Components

*   **Z-Array:**
    *   For a string `S` of length `n`, `Z` is an array of length `n`.
    *   `Z[i]` = length of the longest common prefix between `S` and the suffix of `S` starting at index `i`. (`S[0...k-1] == S[i...i+k-1]`)
    *   `Z[0]` is typically defined as 0 or `n`.
    *   **Example:** `S = "aabcaabxaaz"` -> `Z = [0, 1, 0, 0, 3, 2, 0, 0, 2, 1, 0]`
*   **Z-box `[L, R]`:** An interval maintained during Z-array computation. It represents the substring `S[L...R]` which is a prefix of `S` (`S[L...R] == S[0...R-L]`) and has the rightmost endpoint `R` found so far. This box is used to efficiently calculate subsequent Z-values.
*   **Combined String `S = P + $ + T`:** The key construct for pattern matching. The separator `$` prevents matches from crossing the P-T boundary. Occurrences of `P` in `T` correspond to `Z[i] == len(P)` for `i > len(P)`.

## 3. Algorithm Steps

1.  **Construct Combined String:** Create `S = P + '$' + T`. Let `m = len(P)`, `n_T = len(T)`, `n = len(S) = m + 1 + n_T`.
2.  **Compute Z-Array:** Calculate the Z-array for `S` using the linear-time algorithm (often utilizing the Z-box `[L, R]` optimization).
3.  **Find Matches:** Iterate `i` from `m + 1` to `n - 1` (indices corresponding to the start of `T` within `S`).
4.  If `Z[i] == m`, an occurrence of pattern `P` is found in the original text `T` starting at index `i - (m + 1)`.

## 4. Python Template

```python
def compute_z_array(s: str) -> list[int]:
    """Computes the Z-array for string 's' in O(len(s)) time."""
    n = len(s)
    z = [0] * n
    l, r = 0, 0  # Left and right boundaries of the current Z-box [l, r]

    for i in range(1, n): # Start from index 1
        # Case 1: i is outside the current Z-box
        if i > r:
            l, r = i, i
            while r < n and s[r - l] == s[r]:
                r += 1
            z[i] = r - l
            r -= 1 # r is the rightmost index *in* the box
        # Case 2: i is inside the current Z-box
        else:
            k = i - l # Corresponding index in the prefix
            # Subcase 2a: z[k] doesn't extend beyond the Z-box
            if z[k] < r - i + 1:
                z[i] = z[k]
            # Subcase 2b: z[k] extends up to or beyond the Z-box
            else:
                # Need to check further starting from r + 1
                l = i # New Z-box starts at i
                while r < n and s[r - l] == s[r]:
                    r += 1
                z[i] = r - l
                r -= 1
    # z[0] = n # Optional: Some definitions set z[0] to n
    return z

def z_algorithm_search(text: str, pattern: str) -> list[int]:
    """
    Performs pattern matching using the Z-Algorithm.
    Returns a list of starting indices of all occurrences.
    """
    m = len(pattern)
    n_T = len(text)
    if m == 0:
        return list(range(n_T + 1)) # Or handle as needed
    if n_T == 0 or m > n_T:
        return []

    # Choose a separator not present in pattern or text
    separator = "#" # Ensure this is safe based on input constraints
    combined_s = pattern + separator + text
    n_S = len(combined_s)

    z_array = compute_z_array(combined_s)
    matches = []

    # Iterate through Z-array for indices corresponding to the text part
    for i in range(m + 1, n_S):
        if z_array[i] == m:
            # Match found in original text starting at i - (m + 1)
            matches.append(i - (m + 1))

    return matches
```

## 5. How to Use for Pattern Matching

1.  Call `z_algorithm_search(text, pattern)`.
2.  The returned list contains the 0-based starting indices of all occurrences of `pattern` in `text`.

## 6. Application to "Repeated String Match" Problem

*Problem: Find min repeats `k` of `a` such that `b` is a substring of `a * k`.*

```python
# (Assuming compute_z_array is defined as above)
class Solution:
    def repeatedStringMatch(self, a: str, b: str) -> int:
        len_a, len_b = len(a), len(b)
        if len_b == 0: return 0

        # Determine max repetitions needed for the search text
        k_base = (len_b - 1) // len_a
        max_reps_to_check = k_base + 2
        T = a * max_reps_to_check
        len_T = len(T)

        if len_b > len_T: return -1

        # Construct combined string
        separator = '#'
        S = b + separator + T
        len_S = len(S)

        # Compute Z-array
        z = self._compute_z_array(S) # Assuming method in class

        # Find first match
        for i in range(len_b + 1, len_S):
            if z[i] == len_b:
                # Match found. Calculate starting index in T.
                match_idx_in_T = i - (len_b + 1)
                # Calculate minimum k
                required_k = (match_idx_in_T + len_b + len_a - 1) // len_a
                return required_k # First match gives the minimum k

        # No match found
        return -1

    def _compute_z_array(self, s: str) -> list[int]:
        # ... (implementation from template) ...
        n = len(s)
        z = [0] * n
        l, r = 0, 0
        for i in range(1, n):
            if i > r:
                l, r = i, i
                while r < n and s[r - l] == s[r]: r += 1
                z[i] = r - l
                r -= 1
            else:
                k = i - l
                if z[k] < r - i + 1:
                    z[i] = z[k]
                else:
                    l = i
                    while r < n and s[r - l] == s[r]: r += 1
                    z[i] = r - l
                    r -= 1
        return z

```

## 7. Complexity Analysis

*   **Z-Array Computation:** O(n + m) (where n = len(text), m = len(pattern), because len(S) = n+m+1)
*   **Searching (Iterating Z-Array):** O(n + m)
*   **Total Time:** O(n + m)
*   **Space Complexity:** O(n + m) for the combined string and the Z-array.

## 8. When to Use / Trade-offs

*   **Use:** Elegant linear-time algorithm for pattern matching. The Z-array itself has various other applications in string processing (e.g., finding distinct substrings, string periodicity).
*   **Trade-offs:** Requires O(n + m) space for the combined string and Z-array, which might be more than KMP's O(m) auxiliary space (if text modification isn't allowed). The concept of the Z-box and its update logic can be slightly tricky to grasp initially.

## 9. Example Problems

*   LeetCode 28: Find the Index of the First Occurrence in a String
*   Finding all occurrences of a pattern.
*   Problems involving string periodicity or finding lengths of prefixes that match suffixes starting at various points.
*   Can be used as a building block in more complex string algorithms.
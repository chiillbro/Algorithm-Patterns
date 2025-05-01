# Rabin-Karp Algorithm

## 1. Core Idea / Intuition

Rabin-Karp is a string searching algorithm that uses hashing to find occurrences of a pattern `P` within a text `T`. It compares the hash value of the pattern with the hash value of rolling windows of the same length in the text. If the hashes match, it performs a character-by-character verification to rule out hash collisions (different strings having the same hash).

## 2. Key Concepts / Components

*   **Hashing:** Assigns a numerical value (hash) to a string.
*   **Rolling Hash:** An efficient technique to compute the hash of the *next* window in the text based on the *previous* window's hash in O(1) time on average. This avoids recalculating the hash from scratch for each window.
    *   Typically uses a polynomial rolling hash: `hash(s) = (s[0]*d^(m-1) + s[1]*d^(m-2) + ... + s[m-1]*d^0) % q`
    *   `d`: Base (e.g., size of the alphabet like 26 or 31, often a prime).
    *   `q`: A large prime modulus to keep hashes manageable and reduce collisions.
    *   **Update:** To slide window `T[i...i+m-1]` to `T[i+1...i+m]`:
        1.  Subtract the contribution of `T[i]`.
        2.  Multiply the remaining hash by `d`.
        3.  Add the contribution of `T[i+m]`.
        4.  Perform all calculations modulo `q`.
*   **Collision Handling:** Since different strings can have the same hash, a character-by-character check is mandatory whenever hashes match.

## 3. Algorithm Steps

1.  **Choose Parameters:** Select a base `d` and modulus `q`.
2.  **Precompute:** Calculate `d^(m-1) % q` (where m = len(P)). Let this be `h_factor`.
3.  **Calculate Initial Hashes:** Compute `hash_P` for the pattern `P` and `hash_T` for the first window `T[0...m-1]`. (O(m) time).
4.  **Slide and Compare:**
    *   Iterate `i` from 0 to `len(T) - m`.
    *   If `hash_P == hash_T`:
        *   Verify character by character: `P == T[i...i+m-1]`.
        *   If they match, record the match at index `i`.
    *   If `i < len(T) - m`:
        *   Update `hash_T` to the hash of the next window `T[i+1...i+m]` using the rolling hash formula (O(1) average time):
          `hash_T = (d * (hash_T - ord(T[i]) * h_factor) + ord(T[i+m])) % q` (Handle potential negative results carefully by adding `q`).

## 4. Python Template

```python
def rabin_karp_search(text: str, pattern: str) -> list[int]:
    """
    Performs Rabin-Karp search of pattern within text.
    Returns a list of starting indices of all occurrences.
    """
    n = len(text)
    m = len(pattern)
    if m == 0:
        return list(range(n + 1)) # Or handle as needed
    if n == 0 or m > n:
        return []

    # Parameters (choose carefully based on constraints/alphabet)
    d = 256 # Base (can be size of character set)
    q = 10**9 + 7 # A large prime modulus

    # Precompute d^(m-1) % q
    h_factor = pow(d, m - 1, q)

    # Calculate initial hashes
    hash_p = 0
    hash_t_window = 0
    for i in range(m):
        hash_p = (d * hash_p + ord(pattern[i])) % q
        hash_t_window = (d * hash_t_window + ord(text[i])) % q

    matches = []

    # Slide the window over text
    for i in range(n - m + 1):
        # Check if hashes match
        if hash_p == hash_t_window:
            # Verify character by character (collision check)
            if text[i : i + m] == pattern:
                matches.append(i)

        # Calculate hash for the next window
        if i < n - m:
            # Remove leading digit's contribution
            term1 = (ord(text[i]) * h_factor) % q
            hash_t_window = (hash_t_window - term1 + q) % q # Add q for correct modulo of negative

            # Shift window hash and add trailing digit
            hash_t_window = (hash_t_window * d + ord(text[i + m])) % q

            # Ensure hash_t_window stays positive (though the previous +q should handle it)
            # hash_t_window = (hash_t_window + q) % q

    return matches
```

## 5. How to Use for Pattern Matching

1.  Call `rabin_karp_search(text, pattern)`.
2.  The returned list contains the 0-based starting indices of all occurrences of `pattern` in `text`.

## 6. Application to "Repeated String Match" Problem

*Problem: Find min repeats `k` of `a` such that `b` is a substring of `a * k`.*

```python
# (Assuming rabin_karp_search is defined as above, modified to find first match)
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

        # Use Rabin-Karp to find the first occurrence
        match_index = self._rabin_karp_first(T, b) # Need variant returning index or -1

        if match_index == -1:
            return -1
        else:
            # Calculate the minimum k needed to cover this match
            required_k = (match_index + len_b + len_a - 1) // len_a
            return required_k

    def _rabin_karp_first(self, text: str, pattern: str) -> int:
        # Simplified search returning only the first match index or -1
        n = len(text)
        m = len(pattern)
        if m == 0: return 0
        if n == 0 or m > n: return -1

        d = 256
        q = 10**9 + 7
        h_factor = pow(d, m - 1, q)
        hash_p = 0
        hash_t_window = 0

        for i in range(m):
            hash_p = (d * hash_p + ord(pattern[i])) % q
            hash_t_window = (d * hash_t_window + ord(text[i])) % q

        for i in range(n - m + 1):
            if hash_p == hash_t_window:
                if text[i : i + m] == pattern:
                    return i # Return index immediately

            if i < n - m:
                term1 = (ord(text[i]) * h_factor) % q
                hash_t_window = (hash_t_window - term1 + q) % q
                hash_t_window = (hash_t_window * d + ord(text[i + m])) % q

        return -1 # Not found
```

## 7. Complexity Analysis

*   **Preprocessing (Initial Hashes, h_factor):** O(m)
*   **Searching:**
    *   **Average Case:** O(n + m). Assumes few hash collisions. Hash updates are O(1).
    *   **Worst Case:** O(n * m). Can occur if many hash collisions happen, leading to frequent O(m) verification steps. Extremely unlikely with good prime `q` and base `d`.
*   **Total Time (Average):** O(n + m)
*   **Space Complexity:** O(1) (excluding space for text/pattern storage).

## 8. When to Use / Trade-offs

*   **Use:** Good for finding single or multiple occurrences. Often simpler to implement the core loop than KMP. Works well in practice. Can be adapted for 2D pattern matching.
*   **Trade-offs:** Relies on hashing; performance depends on the quality of the hash function and parameters (`d`, `q`) to minimize collisions. Worst-case time complexity is poor, though rare. Potential for integer overflow if not handled carefully with modulo arithmetic.

## 9. Example Problems

*   LeetCode 28: Find the Index of the First Occurrence in a String
*   Finding all occurrences of a pattern in text.
*   Searching for multiple patterns simultaneously (can precompute pattern hashes).
*   Substring search problems where average-case linear time is acceptable.
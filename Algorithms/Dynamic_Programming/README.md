# Dynamic Programming (DP)

**Core Idea:** Dynamic Programming is a powerful algorithmic technique for solving optimization, counting, or decision problems by breaking them down into simpler, overlapping subproblems and solving each subproblem only once, storing their solutions to avoid redundant computations. This approach typically relies on two key properties:

1.  **Optimal Substructure:** The optimal solution to the overall problem can be constructed from the optimal solutions of its subproblems.
2.  **Overlapping Subproblems:** The same subproblems are encountered multiple times when solving the main problem recursively. DP stores the results of these subproblems (memoization or tabulation) to reuse them.

**General Approach to Solving DP Problems:**

1.  **Identify Subproblems:** Define what a "state" in your DP solution represents. This is often the hardest part. Ask yourself: "If I need to compute the answer for `X`, what smaller versions of `X` would help me?"

    - Examples: `dp[i]` = result for `arr[0...i]`, `dp[i][j]` = result for `arr1[0...i]` and `arr2[0...j]`.

2.  **Define the Recurrence Relation (Transition):** Express the solution to a state `dp[state]` in terms of solutions to "smaller" or "previous" states. This defines how to build up the solution.

    - Example: `dp[i] = max(dp[i-1], dp[i-2] + arr[i])`

3.  **Identify Base Cases:** Determine the solutions for the smallest possible subproblems that don't depend on any other subproblems. These are the starting points for your DP.

    - Example: `dp[0] = arr[0]`, `dp[0] = 0`, `dp[i][0] = i`, `dp[0][j] = j`.

4.  **Choose an Implementation Strategy:**

    - **Memoization (Top-Down):** Write a recursive function that computes the solution for a state. Store the result of each state computation in a lookup table (e.g., array, hash map) before returning. If the function is called again for the same state, return the stored result.
    - **Tabulation (Bottom-Up):** Iteratively fill a DP table, starting from the base cases and using the recurrence relation to compute solutions for larger subproblems in a specific order.

5.  **Determine the Order of Computation (for Tabulation):** Ensure that when you compute `dp[state]`, the values of the subproblems it depends on have already been computed.

6.  **Find the Final Answer:** The answer to the original problem is usually one of the entries in the DP table (e.g., `dp[n]`, `dp[n][m]`, or the maximum value in `dp`). Sometimes, path reconstruction is needed to find the actual solution elements, not just the value.

**How to Use the Patterns in This Section:**

Each sub-directory within `Dynamic_Programming/` focuses on a common DP pattern or problem family (e.g., LIS, Knapsack, LCS).

- The `README.md` in each sub-directory provides an overview of that specific pattern.
- Individual `.md` files within those sub-directories will detail specific problem types or variations of the pattern, including:
  - **Problem Characteristics:** Keywords or traits that suggest this DP pattern.
  - **Core Idea:** The fundamental DP state and transition for this pattern.
  - **Templates:** Python code templates for both memoization (if common) and tabulation, with detailed line-by-line explanations.
  - **Example Problems:** Links to LeetCode or descriptions of classic problems.
  - **Complexity Analysis:** Time and space complexity.
  - **Important Notes/Variations:** Common pitfalls, optimizations, or related concepts.

**Key to Mastering DP (Refer to `INFO.md` #17):**

- **Practice, Practice, Practice:** The more problems you solve, the better you'll become at recognizing patterns and defining states.
- **Start Simple:** Begin with 1D DP problems and gradually move to 2D DP and more complex variations.
- **Visualize:** Draw out the DP table for small examples to understand how it's filled.
- **Don't Be Afraid to Be Wrong:** Defining the state and recurrence can take a few tries. Iteratively refine your approach.

# Good luck exploring the world of Dynamic Programming!

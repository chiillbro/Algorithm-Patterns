# Singly Linked Lists

This section explores the Singly Linked List, a fundamental data structure that relies on nodes and pointers to create a sequential chain of elements. It offers different performance trade-offs compared to the array.

### ELI6: The Scavenger Hunt Analogy

A **Singly Linked List** is like a scavenger hunt.
*   You start with the first clue, called the **`head`**.
*   Each clue (a **`Node`**) contains a piece of information (the **`data`**) and the location of the *next* clue (the **`next` pointer**).
*   The clues can be scattered all over town; they don't need to be side-by-side. This represents **non-contiguous memory**.
*   To get to the 5th clue, you must follow the first four clues in order. You can't jump directly to it. This means **accessing an element is O(n)**.
*   The final clue points to "nowhere" (`None`), signaling the end of the list.

---

### Core Concepts

*   **Node-Based Structure:** Unlike an array, a linked list is not a single block of memory. It is a collection of individual `Node` objects, each containing an element and a reference (pointer) to the next node in the sequence.
*   **Head and Tail Pointers:** A `LinkedList` object itself only needs to store a reference to the `_head` node to maintain the entire list. For efficiency, we also maintain a `_tail` pointer to the last node.
*   **Sequential Traversal:** Operations that need to access or modify a node in the middle of the list require starting from the `_head` and following the `_next` pointers one by one.

---

### Complexity Analysis

| Operation | Dynamic Array | Singly Linked List | Why (for Linked List)? |
| :--- | :--- | :--- | :--- |
| **Access `[k]`** | `O(1)` | `O(k)` | Must traverse `k` nodes from the `head`. |
| **Search (by value)** | `O(n)` | `O(n)` | Must potentially check every node. |
| **Add at Front** | `O(n)` | `O(1)` | Just create a new node and rewire the `head` pointer. |
| **Add at End** | `Amortized O(1)` | `O(1)` | With a `_tail` pointer, this is a simple rewiring. |
| **Delete at Front** | `O(n)` | `O(1)` | Just point `head` to the second element. |
| **Delete at End** | `Amortized O(1)` | `O(n)` | **CRITICAL WEAKNESS:** Must traverse from the `head` to find the *second-to-last* node. |

---

### Implementation Goals in `singly_linked_list.py`

*   Build an inner `_Node` class to hold the element and the `_next` pointer.
*   Implement the main `SinglyLinkedList` class with `_head` and `_size` attributes.
*   Implement `add_first` in `O(1)` and a naive `add_last` in `O(n)`.
*   **Follow-up 1:** Optimize `add_last` to `O(1)` by adding and maintaining a `_tail` pointer.
*   **Follow-up 2:** Implement `remove_first` (`O(1)`) and `remove_last` (`O(n)`) and analyze why `remove_last` is inefficient.

---

### Key Learnings from Follow-ups

*   **The Power of a `_tail` Pointer:** Adding a single pointer (`_tail`) to our data structure's state dramatically improved the `add_last` operation from `O(n)` to `O(1)`. This is a classic example of a space-for-time trade-off.
*   **The Weakness of One-Way Pointers:** The `O(n)` complexity of `remove_last` is a direct consequence of only having `_next` pointers. To remove the tail, we need its predecessor, but we have no way to go backward. This problem directly motivates the need for a **Doubly Linked List**, where each node also has a `_previous` pointer.
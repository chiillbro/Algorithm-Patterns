# Doubly & Circular Linked Lists

This section addresses the primary weakness of the Singly Linked List by introducing a second pointer, and explores a common structural variation.

### ELI6: The Train and the Merry-Go-Round

A **Doubly Linked List** is like a train.

- Each train car (`Node`) has couplings to the car in front (`_next`) and the car behind (`_prev`).
- This allows for two-way traversal. If you're in any car, you can easily walk forwards or backwards.
- This ability to "go backwards" is the key to solving the `remove_last` performance problem from Day 2.

A **Circular Linked List** is like a merry-go-round.

- The last element's `_next` pointer doesn't point to `None`; it loops back to the `head`.
- There is no "end" to the list. You can traverse indefinitely. This is useful for creating round-robin schedules or managing turn-based systems.

---

### Core Concepts

#### Doubly Linked List

- **Two-Way Pointers:** Each `_Node` now contains three attributes: `_element`, `_next`, and `_prev`.
- **Symmetrical Operations:** The `_prev` pointer makes operations symmetrical. The logic for adding/removing from the front is nearly identical to adding/removing from the back.
- **Sentinel Nodes:** A robust implementation technique is to use `_header` and `_trailer` dummy nodes. These nodes don't store user data but exist to simplify the logic. By doing this, every real node is guaranteed to have a non-null `_prev` and `_next`, which eliminates numerous `if self.is_empty()` edge cases from the code.
- **The Fix:** With the `_prev` pointer, `remove_last` becomes an `O(1)` operation. We can access the tail in O(1), and from there, access its predecessor in O(1) to perform the necessary pointer rewiring.

#### Circular Linked List

- **Loop Structure:** The `_next` pointer of the tail node connects back to the `head` node.
- **Single Pointer Management:** A common implementation only stores a reference to the `_tail` node. From the tail, the head is accessible in one step (`tail._next`), providing `O(1)` access to both "ends" of the list.
- **Rotation:** A unique and efficient `O(1)` operation where the head element becomes the new tail element simply by advancing the `_tail` pointer.

---

### Complexity Analysis

The addition of the `_prev` pointer is the only change from a Singly Linked List, but its impact is significant.

| Operation            | Singly Linked List | Doubly Linked List      | Why (for Doubly)?                                                    |
| :------------------- | :----------------- | :---------------------- | :------------------------------------------------------------------- |
| **Access `[k]`**     | `O(k)`             | `O(k)`                  | Still requires sequential traversal.                                 |
| **Add at Front/End** | `O(1)`             | `O(1)`                  | Same logic, just one extra pointer to update.                        |
| **Delete at Front**  | `O(1)`             | `O(1)`                  | Same logic.                                                          |
| **Delete at End**    | `O(n)`             | **`O(1)`**              | The `_prev` pointer allows `O(1)` access to the second-to-last node. |
| **Memory Overhead**  | 1 pointer per node | **2 pointers** per node | The cost of the `_prev` pointer.                                     |

---

### Implementation Goals in `.py` files

- **`doubly_linked_list.py`:**
  - Build a `_Node` with `_prev` and `_next` pointers.
  - Implement the list using `_header` and `_trailer` sentinel nodes.
  - Create robust helper methods (`_insert_between`, `_delete_node`) to handle pointer logic cleanly.
  - Demonstrate that `add_first`, `add_last`, `remove_first`, and `remove_last` are all `O(1)`.
- **`circular_linked_list.py`:**
  - Implement a circular list using only a `_tail` reference.
  - Show how to perform `add_first`, `add_last`, and `remove_first` operations.
  - Implement the unique `rotate()` method in `O(1)`.

---

### Key Learnings

- **Solving Problems with Pointers:** Adding one extra pointer (`_prev`) per node solved the single biggest performance issue of the singly linked list. This demonstrates a core principle: the way you structure your data's connections fundamentally defines the efficiency of your algorithms.
- **Code Elegance with Sentinels:** Sentinel nodes are a powerful "trick of the trade." They add a small amount of constant memory overhead but can drastically simplify implementation logic by removing a wide range of edge case checks (e.g., for empty lists or single-element lists).
- **Structural Variations:** The Circular Linked List shows that simple changes to pointer destinations (tail -> head instead of tail -> None) can create entirely new behaviors and use cases for the same underlying node-based concept.

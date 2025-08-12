# Arrays & Dynamic Arrays

This section covers the most fundamental data structure, the array, and its flexible evolution, the dynamic array.

### ELI6: The Parking Lot Analogy

A **static array** is like a parking lot with a fixed number of numbered spots. Accessing a car in a specific spot (e.g., #27) is instant because you know exactly where to go. But if the lot is full, you can't add more cars.

A **dynamic array** is like a musician with magic music paper. They start with a small sheet. When it fills up, they magically get a new, bigger sheet and copy all their old notes over before adding the new one. Most additions are fast, but some are slow due to the copying.

---

### Core Concepts

- **Static Array:** A contiguous block of memory with a fixed size determined at compile time.
  - **O(1) Access:** Achieved through pointer arithmetic: `address = start_address + (index * element_size)`.
  - **O(n) Insert/Delete:** Requires shifting all subsequent elements.
- **Dynamic Array:** A flexible array built on top of a static array.
  - **Capacity vs. Size:** It maintains a `capacity` (the size of the internal static array) and a `size` (the number of elements actually stored).
  - **Amortized O(1) Append:** When the array is full (`size == capacity`), it resizes by creating a new, larger array and copying elements over. By doubling the capacity each time, the expensive `O(n)` resize operations are infrequent enough that the average cost of an append remains `O(1)`.

---

### Complexity Analysis

| Operation                  | Static Array      | Dynamic Array    |
| :------------------------- | :---------------- | :--------------- |
| **Access (Read/Write)**    | `O(1)`            | `O(1)`           |
| **Search (by value)**      | `O(n)`            | `O(n)`           |
| **Append (at end)**        | `O(1)` (if space) | `Amortized O(1)` |
| **Pop (from end)**         | `O(1)`            | `Amortized O(1)` |
| **Insert/Delete (middle)** | `O(n)`            | `O(n)`           |

---

### Implementation Goals in `dynamic_array.py`

- Build a `DynamicArray` class from scratch using `ctypes` for the low-level array.
- Implement `__len__`, `__getitem__`, and `append`.
- Create a private `_resize` method that handles growing the array.
- **Follow-up 1:** Implement an `insert(k, value)` method that requires shifting elements.
- **Follow-up 2:** Implement a `pop()` method and enhance the `_resize` logic to shrink the array when its size is less than 1/4 of its capacity.

---

### Key Learnings from Follow-ups

- **Inserting requires shifting:** Inserting an element at an arbitrary index `k` is an `O(n-k)` operation because all elements from `k` onwards must be shifted one position to the right. This highlights a key performance cost.
- **Shrinking requires a threshold:** Simply shrinking the array when `size == capacity / 2` can lead to **thrashing**, where a sequence of `append` and `pop` operations near the boundary would each cost `O(n)`. Using a `1/4` threshold for shrinking provides a buffer, ensuring `pop` remains an amortized `O(1)` operation.

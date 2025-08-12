import ctypes

class DynamicArray:
    """A dynamic array class emulating Python's list."""

    def __init__(self):
        """Create an empty array."""
        self._n = 0  # Count of actual elements
        self._capacity = 1  # Default capacity of the underlying static array
        self._A = self._make_array(self._capacity) # The internal static array

    def __len__(self):
        """Return number of elements stored in the array."""
        return self._n

    def __getitem__(self, k):
        """Return element at index k."""
        if not 0 <= k < self._n:
            raise IndexError('invalid index')
        return self._A[k]

    def append(self, obj):
        """Add object to the end of the array."""
        # The key logic: check if we have space first.
        if self._n == self._capacity:
            # If not, resize to double the current capacity.
            self._resize(2 * self._capacity)
        
        self._A[self._n] = obj
        self._n += 1
    
    def insert(self, k, value):
        """Insert value at index k, shifting subsequent elements to the right."""
        # Note: we allow k == self._n for insertion at the very end.
        if not 0 <= k <= self._n:
            raise IndexError('invalid index')

        # If the array is full, resize it first.
        if self._n == self._capacity:
            self._resize(2 * self._capacity)

        # The crucial part: shift elements to the right.
        # We MUST loop backwards to avoid overwriting data.
        for j in range(self._n, k, -1):
            self._A[j] = self._A[j-1]

        self._A[k] = value
        self._n += 1

    
    def pop(self):
        """Remove and return the last element of the array."""
        if self._n == 0:
            raise IndexError("pop from empty array")

        # The actual removal is simple
        value = self._A[self._n - 1]
        self._A[self._n - 1] = None # Help with garbage collection
        self._n -= 1

        # The shrinking logic
        if self._n < self._capacity // 4:
            self._resize(self._capacity // 2)

        return value



    def _resize(self, new_capacity):
        """Resize internal array to a new capacity."""
        B = self._make_array(new_capacity)  # 1. Create a new, bigger array
        for k in range(self._n):            # 2. Copy all existing elements
            B[k] = self._A[k]
        
        self._A = B                         # 3. Use the new array
        self._capacity = new_capacity       # 4. Update the capacity

    def _make_array(self, capacity):
        """Return a new empty array with a given capacity."""
        # This is a low-level way in Python to create a raw static array.
        return (capacity * ctypes.py_object)()

    def __str__(self):
        """Returns a string representation of the array."""
        return '[' + ', '.join(str(self._A[i]) for i in range(self._n)) + ']'
    


# ** Example Usage ** #

d_array = DynamicArray()

print("initial length of array: ", len(d_array)) # 0
print("initial capacity of array: ", d_array._capacity) # 1

d_array.append(1)
d_array.append(2)
d_array.append(3)

print("dynamic array: ", d_array)
print("length after adding 3 elements: ", len(d_array)) # 3
print("capacity after adding 3 elements: ", d_array._capacity) # 4, was resized while adding element 2

print("Element at index 1: ", d_array[1])

# Insert
d_array.insert(1, 5)
d_array.insert(4, 8)

print("Array after insertions: ", d_array)
print("capacity after inserting 2 elements: ", d_array._capacity) # 8

# Pop
d_array.pop()
d_array.pop()
print("capacity after popping 2 elements: ", d_array._capacity) # 8

d_array.pop()
d_array.pop()
print("capacity after popping 2 more elements: ", d_array._capacity) # 4
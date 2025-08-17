class DoublyLinkedList:
    class _Node:
        """Lightweight, non-public class for a doubly linked node."""

        __slots__ = ("_element", "_next", "_prev")

        def __init__(self, element, prev, next):
            self._element = element
            self._prev = prev
            self._next = next

    # ** Only the list from _header._next till _trailer._prev is the real one **
    def __init__(self):
        """Create an empty list."""
        # We use "sentinel" or "header/trailer" nodes.
        # This is a common and robust technique to simplify code.
        self._header = self._Node(None, None, None)
        self._trailer = self._Node(None, self._header, None)
        self._header._next = self._trailer

        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    # --- The most important private method ---
    def _insert_between(self, e, predecessor, successor):
        """Add element e between two existing nodes and return new node."""
        new_node = self._Node(e, predecessor, successor)
        predecessor._next = new_node
        successor._prev = new_node

        self._size += 1

        return new_node

    # --- Public update Methods ---
    def add_first(self, e):
        return self._insert_between(e, self._header, self._header._next)

    def add_last(self, e):
        return self._insert_between(e, self._trailer._prev, self._trailer)

    def _remove_node(self, node):
        """Remove a nonsentinel node from the list and return its element."""
        predecessor = node._prev
        successor = node._next

        predecessor._next = successor
        successor._prev = predecessor

        value = node._element
        # Optional: help garbage collection by severing node's pointers
        node._prev = node._next = node._element = None
        self._size -= 1

        return value

    def remove_first(self):
        """Remove and return the first element."""
        if self.is_empty():
            raise IndexError("List is empty")
        return self._remove_node(self._header._next)

    def remove_last(self):
        """Remove and return the last element."""
        if self.is_empty():
            raise IndexError("List is empty")
        return self._remove_node(self._trailer._prev)

    def __str__(self):
        if self.is_empty():
            return "None"

        res = []

        cur = self._header._next
        while cur._next is not None:
            res.append(str(cur._element))
            cur = cur._next

        return " -> ".join(res) + " -> None"


# *** Example Usage ***

dll = DoublyLinkedList()

print("Empty Doubly Linked Intialized and Declared: ", dll)
dll.add_first(3)

dll.add_first(2)
dll.add_first(1)

dll.add_last(4)

print("List after adding some elements: ", dll)

dll.remove_first()

print("List after removing an element from start: ", dll)

dll.remove_last()

print("List after removing an element from last: ", dll)

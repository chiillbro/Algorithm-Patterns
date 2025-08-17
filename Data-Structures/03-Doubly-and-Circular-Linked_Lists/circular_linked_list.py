class CircularLinkedList:
    """
    An implementation of a circular singly linked list.

    The list maintains a reference only to the tail node, from which the
    head can be accessed in O(1) time via tail._next.
    """

    class _Node:
        """Lightweight, non-public class for a singly linked node."""

        __slots__ = ("_element", "_next")

        def __init__(self, element, next):
            self._element = element
            self._next = next

    def __init__(self):
        """Create an empty circular linked list."""
        self._tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def get_head(self):
        """Return the head node (or None if empty)."""
        if self.is_empty():
            return None
        return self._tail._next

    def get_tail(self):
        """Return the tail node (or None if empty)."""
        return self._tail

    def add_first(self, e):
        """Add an element to the front of the list."""
        new_node = self._Node(e, None)

        if self.is_empty():
            self._tail = new_node
        else:
            old_head = self.get_head()
            new_node._next = old_head

        self._tail._next = new_node
        self._size += 1

    def add_last(self, e):
        """Add an element to the end of the list."""
        # add_first handles the creation, then we just advance the tail pointer.
        self.add_first(e)
        self._tail = self._tail._next

    def remove_first(self):
        """Remove and return the first element."""
        if self.is_empty():
            raise IndexError("List is empty")

        old_head = self.get_head()
        if self._size == 1:
            # List becomes empty
            self._tail = None
        else:
            # The tail now points to the second element
            self._tail._next = old_head._next

        self._size -= 1
        return old_head._element

    def rotate(self):
        """Rotate the list so the old head becomes the new tail."""
        if self._size > 0:
            # The current head becomes the new tail in one step!
            self._tail = self._tail._next

    def __str__(self):
        """Returns a string representation of the circular list."""
        if self.is_empty():
            return "[]"

        res = []
        head = self.get_head()
        cur = head
        # We need a do-while loop equivalent
        while True:
            res.append(str(cur._element))
            cur = cur._next

            if cur is head:  # Stop when we've looped back to the start
                break

        return " -> ".join(res) + " (loops back) "


# *** Example Usage ***

cll = CircularLinkedList()

print("Empty List: ", cll)

cll.add_first(3)
cll.add_first(2)
cll.add_last(4)

print("List after adding 3 elements: ", cll)

cll.add_first(1)
cll.add_first(0)

cll.remove_first()

print("List after removing an element: ", cll)

cll.rotate()

print("List after rotating: ", cll)

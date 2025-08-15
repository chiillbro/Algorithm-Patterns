class SinglyLinkedList:
    # We start by defining the Node class inside our LinkedList.
    # This is a common practice as Nodes are intrinsically tied to their list.
    class _Node:
        """Lightweight, non-public class for storing a singly linked node."""
        __slots__ = '_element', '_next' # __slots__ saves memory

        def __init__(self, element, next_node):
            self._element = element
            self._next = next_node

    # --- LinkedList methods start here ---
    def __init__(self):
        """Create an empty list."""
        self._head = self._tail = None
        self._size = 0

    def __len__(self):
        """Return the number of elements in the list."""
        return self._size

    def is_empty(self):
        """Return True if the list is empty."""
        return self._size == 0
    
    def __str__(self):
        """Returns a string representation of the list for printing."""
        if self.is_empty():
            return "None"
        
        result = []
        current = self._head
        while current is not None:
            result.append(str(current._element))
            current = current._next
        return " -> ".join(result) + " -> None"

    # --- Core Operations ---
    
    def add_first(self, e):
        """Add element e to the front of the list. O(1)"""
        # Create a new node, pointing to the current head.
        new_node = self._Node(e, self._head)
        # The list's head is now this new node.
        self._head = new_node

        if self.is_empty():
            self._tail = new_node
        self._size += 1

    def add_last(self, e):
        """Add element e to the end of the list. O(n)"""
        new_node = self._Node(e, None) # The new node will be the last one
        
        if self.is_empty():
            self._head = new_node # If empty, it's the only node
        else:
            # We must traverse to the end of the list
            current = self._head
            while current._next is not None:
                current = current._next
            # The current last node now points to our new node
            current._next = new_node
        
        self._size += 1
    

    ## Follow-up 1: The above core operation `add_last` is very expensive, we can optimize it by sacrificing a tiny amount of memory for tracking _tail pointer.
    def optimized_add_last(self, e):
        """"Add element e to the end of the list using _tail. O(1)"""
        new_node = self._Node(e, None)
        if self.is_empty():
            self._head = new_node
        else:
            self._tail._next = new_node
        
        self._tail = new_node
        self._size += 1
    
    ## Follow-up 2: Methods to remove elements from start and end
    def remove_first(self):
        """Remove and return the first element. O(1)"""
        if self.is_empty():
            raise IndexError("List is empty")
        
        value = self._head._element
        self._head = self._head._next

        self._size -= 1

        # CRITICAL: If the list is now empty, the tail is also gone.
        if self.is_empty():
            self._tail = None
        
        return value
    
    def remove_last(self):
        """Remove and return the last element. O(n)"""
        if self.is_empty():
            raise IndexError("List is empty")
    
        # Only one element, it's the same as remove_first
        if self._size == 1:
            return self.remove_first()
    
        cur = self._head

        # Traverse to find the second-to-last node
        while cur._next is not self._tail:
            cur = cur._next
        
        value = cur._element
        # The second-to-last node is now the new tail
        cur._next = None
        self._tail = cur

        self._size -= 1
        return value

    
    def __next__(self):
        """Allows usage of next() to provide the all the elements one by one until encountering None."""
        cur = self._head
        if not cur:
            StopIteration
        
        self._head = cur._next

        return cur._element

    def __iter__(self):
        """Allows looping over the linked list values."""
        cur = self._head
        while cur is not None:
            yield cur._element
            cur = cur._next
        

            

# **** Example Usage **** #
my_linked_list = SinglyLinkedList()

my_linked_list.add_first(0)

my_linked_list.optimized_add_last(1)

my_linked_list.optimized_add_last(2)

my_linked_list.add_first(10)

my_linked_list.optimized_add_last(20)

print(my_linked_list)

print(len(my_linked_list))


print(list(my_linked_list))

for i, e in enumerate(my_linked_list):
    print(f"{i+1} th node: ", e)

print(next(my_linked_list))

print(next(my_linked_list))
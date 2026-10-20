
class Node:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


class LinkedList:
    def __init__(self):
        self.head = None

    def get_head(self):
        return self.head

    def set_head(self, node):
        new_node = Node(node)
        new_node.next = self.get_head()
        self.head = new_node

    def append_to_LL(self, new_node):
        if self.get_head() is None:
            self.set_head(new_node)
            return

        cur = self.get_head()

        while cur.next is not None:
            cur = cur.next

        cur.next = Node(new_node)

    def makeLinkedList(self, arr):
        self.head = None

        for value in arr:
            self.append_to_LL(value)

        return self.head

    def display(self):
        cur = self.head
        result = []

        while cur is not None:
            result.append(str(cur.val))
            cur = cur.next

        print(" -> ".join(result))

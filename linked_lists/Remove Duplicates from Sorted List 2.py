""" 
You are given the head of a sorted linked list.

Delete all nodes that have duplicate numbers, leaving only distinct numbers from the original list.

Return the linked list sorted as well.
"""
from Node import LinkedList,Node

class Solution(LinkedList):
    def removeduplicate(self,head):
        dummy =Node(0)
        dummy.next = head
        prev,cur = dummy,head
        
        while cur:
            if cur.next and cur.val == cur.next.val:
                while cur.next and cur.val == cur.next.val:
                    cur=cur.next
                prev.next = cur.next
            else:
                prev = prev.next
            cur = cur.next
        return dummy.next


def to_list(head):
    """Walk a linked list and return its values as a python list"""
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def run_remove(arr):
    ll = LinkedList()
    ll.makeLinkedList(arr)
    return to_list(Solution().removeduplicate(ll.get_head()))


if __name__ == "__main__":
    tests = [
        # (input, expected)
        ([1, 2, 3, 3, 4, 4, 5], [1, 2, 5]),        # example: duplicates in the middle
        ([1, 1, 1, 2, 3], [2, 3]),                 # duplicates at the head
        ([1, 2, 3, 3], [1, 2]),                    # duplicates at the tail
        ([], []),                                  # empty list
        ([1], [1]),                                # single node
        ([1, 2, 3], [1, 2, 3]),                    # no duplicates
        ([1, 1], []),                              # everything removed
        ([7, 7, 7, 7], []),                        # all the same value
        ([1, 1, 2, 2, 3, 3], []),                  # only duplicate groups
        ([1, 1, 2, 3, 3, 4], [2, 4]),              # alternating groups and singles
        ([-3, -3, -1, 0, 0, 2], [-1, 2]),          # negatives
    ]

    for i, (arr, expected) in enumerate(tests, 1):
        got = run_remove(arr)
        assert got == expected, f"Test {i} failed: {arr} -> {got}, expected {expected}"
        print(f"Test {i} passed: {arr} -> {got}")

    print("All tests passed")

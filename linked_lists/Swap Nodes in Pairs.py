
from Node import LinkedList,Node

class Solution(LinkedList):
    """
    Given a linked list, swap every two adjacent nodes and return its head.
    You must solve the problem without modifying the values in the list's nodes
    (i.e., only nodes themselves may be changed.)

    Example 1:

    Input: head = [1,2,3,4]

    Output: [2,1,4,3] 
    """
    def swapPairs(self, head):
        dummy =Node(0)
        dummy.next= head
        prev,cur =dummy,head
        
        while cur and cur.next:
            #save nodes first
            next_pair =cur.next.next
            node_to_swap =cur.next
            
            #reverse
            cur.next = next_pair
            node_to_swap.next =cur
            prev.next =node_to_swap
            
            #Move pointers
            prev =cur
            cur =next_pair
        return dummy.next
        
        


def to_list(head):
    """Walk a linked list and return its values as a python list"""
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def run_swap(arr):
    ll = LinkedList()
    ll.makeLinkedList(arr)
    return to_list(Solution().swapPairs(ll.get_head()))


if __name__ =="__main__":
    tests = [
        # (input, expected)
        ([1, 2, 3, 4], [2, 1, 4, 3]),          # example: even length
        ([], []),                              # empty list
        ([1], [1]),                            # single node
        ([1, 2], [2, 1]),                      # exactly one pair
        ([1, 2, 3], [2, 1, 3]),                # odd length, last node stays
        ([1, 2, 3, 4, 5], [2, 1, 4, 3, 5]),    # longer odd length
        ([1, 2, 3, 4, 5, 6], [2, 1, 4, 3, 6, 5]),  # longer even length
        ([7, 7, 7, 7], [7, 7, 7, 7]),          # all duplicates
        ([-1, 0, -2, 5], [0, -1, 5, -2]),      # negatives
    ]

    for i, (arr, expected) in enumerate(tests, 1):
        got = run_swap(arr)
        assert got == expected, f"Test {i} failed: {arr} -> {got}, expected {expected}"
        print(f"Test {i} passed: {arr} -> {got}")

    print("All tests passed")

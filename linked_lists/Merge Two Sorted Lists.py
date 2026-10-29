
#QUESTION
""" 
You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list
"""
from Node import LinkedList,Node
class Solution(LinkedList):
    def mergeTwoLists(self, list1, list2):
        """ 
        <p>Given the head of 2 sorted linked list <br/>
        <h4>This function returns the head of the  merged sorted list
        """
        dummy= Node(0)
        cur = dummy
        
        while list1 and list2:
            if list1.val <= list2.val:
                cur.next = list1
                list1 = list1.next
            else:
                cur.next = list2
                list2=list2.next
            cur= cur.next
            
        if list1:
            cur.next= list1
        else:
            cur.next =list2
        return dummy.next





#TEST

def to_list(head):
    """Walk a linked list and return its values as a python list"""
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def run_merge(arr1, arr2):
    list1 = LinkedList()
    list1.makeLinkedList(arr1)
    list2 = LinkedList()
    list2.makeLinkedList(arr2)
    return to_list(Solution().mergeTwoLists(list1.get_head(), list2.get_head()))


if __name__ =="__main__":
    tests = [
        # (list1, list2, expected)
        ([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4]),  # example from the question
        ([], [], []),                                # both empty
        ([], [0], [0]),                              # list1 empty
        ([5], [], [5]),                              # list2 empty
        ([1, 2, 3], [4, 5, 6], [1, 2, 3, 4, 5, 6]),  # list1 entirely smaller
        ([4, 5, 6], [1, 2, 3], [1, 2, 3, 4, 5, 6]),  # list2 entirely smaller
        ([1, 1, 1], [1, 1], [1, 1, 1, 1, 1]),        # all duplicates
        ([1, 3, 5, 7], [2], [1, 2, 3, 5, 7]),        # different lengths
        ([-3, -1, 2], [-2, 0], [-3, -2, -1, 0, 2]),  # negatives
    ]

    for i, (a, b, expected) in enumerate(tests, 1):
        got = run_merge(a, b)
        assert got == expected, f"Test {i} failed: {a} + {b} -> {got}, expected {expected}"
        print(f"Test {i} passed: {a} + {b} -> {got}")

    print("All tests passed")

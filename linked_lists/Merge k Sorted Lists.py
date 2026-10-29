""" 
You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.

 

Example 1:

Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
Explanation: The linked-lists are:
[
  1->4->5,
  1->3->4,
  2->6
]
merging them into one sorted linked list:
1->1->2->3->4->4->5->6
Example 2:

Input: lists = []
Output: []
Example 3:

Input: lists = [[]]
Output: []
"""
from Node import LinkedList,Node

class Solution(LinkedList):
    def mergeKLists(self, lists):
        
        """
        <h4> This function takes an array of linked list <br/>
        Applies the divide and conquer concept <br/>
        And implements the merge sort agorithm
        Args: 
            lists: List[Optional[ListNode]]
        
        Returns: 
             Optional[ListNode]
        """
        
        if not lists and len(lists)==0:
            return
        
        while len(lists)>1:
            cur_merged=[]
            for i in range(0, len(list),2):
                list1 =lists[i]
                list2 = lists[i+1] if (i+1)< len(lists) else []
                cur_merged.append(self.mergeTwoList(list1,list2)) 
            lists =cur_merged
        return lists[0]
    def mergeTwoList(self, list1,list2):
        #TODO
        dummy =Node(0)
        cur = dummy
        
        while list1 and list2:
            if list1 <= list2:
                cur.next= list1
                list1= list1.next
            else:
                cur.next = list2
                list2 = list2.next
            cur = cur.next
        if list1:
            cur.next = list1
        if list2:
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


def run_merge(arrays):
    heads = []
    for arr in arrays:
        ll = LinkedList()
        ll.makeLinkedList(arr)
        heads.append(ll.get_head())
    return to_list(Solution().mergeKLists(heads))


if __name__ == "__main__":
    tests = [
        # (lists, expected)
        ([[1, 4, 5], [1, 3, 4], [2, 6]], [1, 1, 2, 3, 4, 4, 5, 6]),  # example 1
        ([], []),                                                    # example 2: no lists
        ([[]], []),                                                  # example 3: one empty list
        ([[], []], []),                                              # all empty
        ([[1, 2, 3]], [1, 2, 3]),                                    # single list
        ([[1], [0]], [0, 1]),                                        # two lists
        ([[], [1], []], [1]),                                        # empty lists mixed in
        ([[1, 2], [3, 4], [5, 6], [7, 8]], [1, 2, 3, 4, 5, 6, 7, 8]),  # even count, already ordered
        ([[7, 8], [5, 6], [3, 4], [1, 2]], [1, 2, 3, 4, 5, 6, 7, 8]),  # reverse ordered
        ([[1, 1], [1], [1, 1, 1]], [1, 1, 1, 1, 1, 1]),              # all duplicates
        ([[-5, -1], [-3], [0, 2]], [-5, -3, -1, 0, 2]),              # negatives, odd count
    ]

    for i, (arrays, expected) in enumerate(tests, 1):
        got = run_merge(arrays)
        assert got == expected, f"Test {i} failed: {arrays} -> {got}, expected {expected}"
        print(f"Test {i} passed: {arrays} -> {got}")

    print("All tests passed")

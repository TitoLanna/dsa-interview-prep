"""
Given the head of a linked list and a value x, 
partition it such that all nodes less than x come before nodes greater than or equal to x.

You should preserve the original relative order of the nodes in each of the two partitions.

Input: head = [1,4,3,2,5,2], x = 3
Output: [1,2,2,4,3,5]

Input: head = [2,1], x = 2
Output: [1,2]
"""
#My approach
#partition the list in to two dummy nodes
# connect the less on together
from Node import LinkedList,Node
class Solution():
    def partition(self,head,x):
        partition_1 = Node(0)
        partition_2= Node(0)
        
        partition_1_prev = partition_1
        partition_2_prev =partition_2
        cur= head
        
        while cur:
            if cur.val < x:
                partition_1_prev.next= cur
                partition_1_prev = cur
            else:
                partition_2_prev.next= cur
                partition_2_prev=cur
            cur= cur.next
            
        partition_2_prev.next = None
        partition_1_prev.next =partition_2.next
        return partition_1.next
                
                
def to_list(head):
    out=[]
    while head:
        out.append(head.val)
        head=head.next
    return out
      
def run_partition(arr,x):
    ll=LinkedList() 
    ll.makeLinkedList(arr)     
    return to_list(Solution().partition(ll.get_head(),x))


if __name__ =="__main__":
    test_cases = [
        ([1,4,3,2,5,2], 3, [1,2,2,4,3,5]),  # example 1
        ([2,1], 2, [1,2]),                  # example 2
        ([], 3, []),                        # empty list
        ([1], 0, [1]),                      # single node, goes to the >= side
        ([1], 5, [1]),                      # single node, goes to the < side
        ([1,2,3], 10, [1,2,3]),             # all nodes less than x
        ([4,5,6], 1, [4,5,6]),              # all nodes >= x
        ([3,3,3], 3, [3,3,3]),              # all equal to x
        ([5,4,3,2,1], 3, [2,1,5,4,3]),      # descending, order preserved in each part
        ([1,2,3,4,5], 3, [1,2,3,4,5]),      # already partitioned
        ([3,1,2], 3, [1,2,3]),              # x at the head
        ([1,1,4,4,2,2], 3, [1,1,2,2,4,4]), # duplicates keep relative order
        ([-1,5,-3,2], 0, [-1,-3,5,2]),      # negative values
    ]

    for i, (arr, x, expected) in enumerate(test_cases, 1):
        res = run_partition(arr, x)
        assert res == expected, f"Test{i} failed: {arr}, x:{x} -> {res}, expected: {expected}"
        print(f"Test{i} passed: {arr}, x:{x} -> got {res}")
    print("All test cases passed!")
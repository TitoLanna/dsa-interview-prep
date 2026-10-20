"""
You are given the head of a singly linked-list. The list can be represented as:

L0 → L1 → … → Ln - 1 → Ln
Reorder the list to be on the following form:

L0 → Ln → L1 → Ln - 1 → L2 → Ln - 2 → …
You may not modify the values in the list's nodes. Only nodes themselves may be changed.

Example:
Input: head = [1,2,3,4]
Output: [1,4,2,3]

constraint:
The number of nodes in the list is in the range [1, 5 * 10**4].
1 <= Node.val <= 1000
"""
from Node  import LinkedList

class Solution:
    def reorderList(self,head):
        
        if head and head.next is None:
            return
        
        cur= head
        stack=[]
        while cur:
            stack.append(cur)
            cur= cur.next
        
        cur = head
        n= len(stack)
        for _ in range(n//2):
            last = stack.pop()
            temp_next = cur.next
            cur.next = last
            last.next = temp_next
            cur= temp_next
        cur.next =None
       

# TEST
if __name__ == "__main__":
    arr = [2, 3, 4, 5, 6]

    ll = LinkedList()
    ll.makeLinkedList(arr)

    print("Before:")
    ll.display()

    solution = Solution()
    solution.reorderList(ll.get_head())

    print("After:")
    ll.display()




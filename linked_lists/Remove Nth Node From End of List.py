"""
Given the head of a linked list, remove the nth node from the end of the list and return its head. 
"""
from Node import LinkedList,Node

class Solution(LinkedList):
    def removeNthFromEnd(self,head,n):
        dummy = Node(0)
        dummy.next = head
        
        slow = head
        fast = head
        prev = dummy
        
        for _ in range(n):
            if fast is None:
                return None
            fast= fast.next
        
        while fast:
            prev = slow
            slow = slow.next
            fast = fast.next
        prev.next = slow.next
        slow.next=None
        
        return dummy.next
    #Test
if __name__ == "__main__":
    
    arr = [1,2,3,4,5]
    ll =LinkedList()
    ll.makeLinkedList(arr)
    print("Before:",ll.display())
    head = ll.get_head()
    solution = Solution().removeNthFromEnd(head,2)  
    
    print("After",ll.display())
        
        
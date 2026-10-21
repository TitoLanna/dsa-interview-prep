""" 
Given the head of a sorted linked list, 
delete all duplicates such that each element appears only once. 
Return the linked list sorted as well.

Input: head = [1,1,2]
Output: [1,2]

Input: head = [1,1,2,3,3]
Output: [1,2,3]
"""
from Node import LinkedList
class Solution(object):
    def deleteDuplicates(self,head):
        cur = head
        while cur and cur.next:
            if cur.val == cur.next.val:
                cur.next = cur.next.next
            else:
                cur = cur.next
        return head
        


#Test
if __name__ == "__main__":
    
    arr = [2,3,3,5,5,6]
    ll =LinkedList()
    ll.makeLinkedList(arr)
    print("Before:",ll.display())
    head = ll.get_head()
    solution = Solution().deleteDuplicates(head)
    found_at,address = ll.list_search(head,3)
    print("Search:",found_at," found at:",address)
    print("After",ll.display())
    
    
    
        
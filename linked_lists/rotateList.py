#Given the head of a linked list, rotate the list to the right by k places.
"""
Input :[1,2,3,4,5] k= 2
Output:[4,5,1,2,3]
"""
from Node import LinkedList


class Solution(object):
    def rotateRight(self,head,k):
        
        if not head or not head.next or k==0:
            return head
        
        cur = head
        length = 1
        #Get Length of the linkedList
        while cur:
            length += 1
            cur=cur.next
        
        k %= length
        
        for _ in range(k):
            prev =None
            cur = head
            
            #Get the Tail of the linkedList
            while cur.next:
                prev = cur
                cur = cur.next
            #Disconnect the last node

            prev.next = None
            
            #Move the last node 
            cur.next  = head
            head = cur
        
        return head




if __name__ == "__main__":
    arr = [2, 3, 4, 5, 6]
    k =2

    ll = LinkedList()
    ll.makeLinkedList(arr)

    print("Before:")
    ll.display()
    solution = Solution()
    solution.rotateRight(ll.get_head(),k)
    print("After:")
    ll.display()



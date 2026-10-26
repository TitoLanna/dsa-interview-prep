from Node import LinkedList,Node
#QUESTION
"""Given the head of a linked list and an integer val, 
remove all the nodes of the linked list that has Node.val == val, 
and return the new head.

"""
#EXAMPLE:
"""
Input: head = [1,2,6,3,4,5,6], val = 6
Output: [1,2,3,4,5] 
"""
class Solution(LinkedList):
    def removeElements(self,head,val):
        
        dummy = Node(0)
        dummy.next = head
        
        prev = dummy
        cur = head
        
        while cur is not None:
            if cur.val != val:
                prev = cur
                cur = cur.next
            else:
                prev.next = cur.next
                cur =cur.next
        return dummy.next
    
    def printList(self,head):
        """ 
        This function returns a print of the a linked list<br/> 
        when given a head node
        
        """
        cur = head
        while cur:
            yield cur.val
            cur = cur.next
           
        
    


if __name__ =="__main__": 
    nodes =[7,7,7,7]
    ll = LinkedList()
    head =ll.makeLinkedList(nodes)
    res =Solution()
    
    head =res.removeElements(head,7)
    for value in res.printList(head):
        print(value,end="->")
    print(None)
    
        
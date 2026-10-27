
#QUESTION
""" 
You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list
"""
from Node import LinkedList,Node
class Solution(LinkedList):
    def mergeTwoLists(self, list1, list2):
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

if __name__ =="__main__":
    
    list1 =LinkedList()
    list1.makeLinkedList([1,2,4])
    list2 = LinkedList()
    list2.makeLinkedList([1,3,4])
    
    print("Before:\t")
    l1_head= list1.get_head()
    l2_head = list2.get_head()
    solu = Solution()
    res =solu.mergeTwoLists(l1_head,l2_head)#Return a linked list
    
    while res:
        if res.next is not None:
             print(res.val,end="->")
        else: 
            print(res.val,end=" ")
        res= res.next
    print()
    
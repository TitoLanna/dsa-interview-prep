

#QUESTION:
"""
You are given two non-empty linked lists representing two non-negative integers. 
The digits are stored in reverse order, and each of their nodes contains a single digit. 
Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.
Example:
Input: l1 = [2,4,3], 
       l2 = [5,6,4]
Output: [7,0,8]


Constraints:
0<=size of LinledList<=100
0<=Node.val<=9
"""


class Node:
    def __init__(self ,val ,next=None):
        self.val =val
        self.next =next
        
    @staticmethod
    def loadList(myList):
        
        if not myList:
            return None
        
        
        head = Node(myList[0])
        curr = head
        
        for val in myList[1:]:
            curr.next=Node(val)
            curr =curr.next
        return head

            
    @staticmethod
    def traverse(head):
        if head is None:
            print(" ")
            return 
        print(head.val,end=" ")
        Node.traverse(head.next)
        
        
              
        
def addTwoNumbers(l1,l2):
    dummy = Node(0)
    current = dummy
    carry =0
    while l1 or l2 or carry:
        a = l1.val if l1 else 0
        b = l2.val if l2 else 0
        
        total = a + b + carry
        digit = total % 10
        carry = total//10
        
        if l1:
            l1 = l1.next
        if l2:
            l2 =l2.next
        
        current.next=Node(digit) 
        current =current.next
    return dummy.next



#test
l1=Node.loadList([2,4,3])
l2 =Node.loadList([5,6,4])
Node.traverse(
    addTwoNumbers(
        l1,
        l2
    )
)

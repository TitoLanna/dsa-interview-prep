#QUESTION
""" 
There is a singly-linked list head and we want to delete a node node in it.

You are given the node to be deleted node. You will not be given access to the first node of head.

All the values of the linked list are unique, and it is guaranteed that the given node node is not the last node in the linked list.

Delete the given node. Note that by deleting the node, we do not mean removing it from memory. We mean:

The value of the given node should not exist in the linked list.
The number of nodes in the linked list should decrease by one.
All the values before node should be in the same order.
All the values after node should be in the same order.
Custom testing:

For the input, you should provide the entire linked list head and the node to be given node. node should not be the last node of the list and should be an actual node in the list.
We will build the linked list and pass the node to your function.
The output will be the entire list after calling your function.

"""
from Node import LinkedList
class Solution(LinkedList):
    def deleteNode(self,node):
            """
            Given a node  this is a function that copies the <br/>
            next node value and removes the next node
            
            Args:
                 Node
            Returns:

            
            """
            if node is None or node.next is None:
                raise RuntimeError("Cannot delete this node using this method")
            node.val = node.next.val
            node.next = node.next.next
    
    
if __name__ == "__main__":
    ll = LinkedList()
    test =[2,3,4,5,6]
    ll.makeLinkedList(test)
    print("Before:\t")
    ll.display()
    print()
    cur =ll.get_head()
    while cur.val!= 5:
        cur=cur.next
    res =Solution()
    res.deleteNode(cur)
    print("After:\t")
    ll.display()
  
    
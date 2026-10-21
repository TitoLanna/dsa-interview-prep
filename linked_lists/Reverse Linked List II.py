
from Node import LinkedList,Node
class Solution(object):
    def reverseBetween(self,head, left,right):
        dummy = Node(0)
        dummy.next =head
        prev = dummy
        for _ in range(left -1):
            prev = prev.next
        cur =prev.next
        
        for _ in range(right-left):
            next_node = cur.next
            cur.next = next_node.next
            next_node.next = prev.next
            prev.next = next_node
        return dummy.next



if __name__=="__main__":
    arr = [1,2,3,4,5,6]
    ll = LinkedList()
    ll.makeLinkedList(arr)
    print("Before:",ll.display())
    res = Solution()
    res.reverseBetween(ll.get_head(),2,5)
    print("After:",ll.display())
    
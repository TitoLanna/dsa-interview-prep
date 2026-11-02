""" Given a linked list, swap every two adjacent nodes and return its head. 
You must solve the problem without modifying the values in the list's nodes 
(i.e., only nodes themselves may be changed.)"""

from Node import LinkedList,Node
class Solution(LinkedList):
    def swapPairs(self, head):
        dummy = Node(0)
        dummy.next = head
        prev,cur = dummy,head
        
        while cur and cur.next:
            next_prev = cur.next.next
            second = cur.next
            
            second.next = cur
            cur.next = next_prev
            prev.next =second
            
            prev = cur
            cur = next_prev
          
        
        return dummy.next

def to_list(head):
    cur = head
    out =[]
    while cur:
        out.append(cur.val)
        cur=cur.next
    return out

def run_swap(arr):
    ll = LinkedList()
    ll.makeLinkedList(arr)
    return to_list(Solution().swapPairs(ll.get_head()))

#TEST

if __name__ == "__main__":
    test_cases =[
        ([1,2,3,4],[2,1,4,3]),#the normal case
        ([],[]),                #Empty array
        ([1],[1]),              #One element in the array
        ([1,2,3],[2,1,3])       #Test  one swap
    ]
    
    for i,(arr,expected) in enumerate(test_cases,1):
        res = run_swap(arr)
        assert res == expected ,f"Test{i} failed: {arr}->{res},expected :{expected}"
        print(f"Test{i} passed : {arr}-> got {res}")
    print("All test cases passed!")
    
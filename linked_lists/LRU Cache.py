""" 
Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

Implement the LRUCache class:

LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
int get(int key) Return the value of the key if the key exists, otherwise return -1.
void put(int key, int value) Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity from this operation, evict the least recently used key.
The functions get and put must each run in O(1) average time complexity.

Input
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
Output
[null, null, null, 1, null, -1, null, -1, 3, 4]
"""
class ListNode:
    def __init__(self ,key=0,val=0):
        self.key = key
        self.val = val
        self.prev =None
        self.next =None
        
       
class LRUCache(object):
    def __init__(self,capacity):
        """ 
        <H4>The idea here is to create a doubly linked list with the head and tail
        ```
        {head}<->{tail}
        ```
        initialize the capacity and the cache that would save and update the key pair values
        """ 
        self.capacity = capacity
        self.cache ={}
        
        self.head  = ListNode()
        self.tail  = ListNode()
        #Connect the Linked List
        self.head.next = self.tail
        self.tail.prev = self.head
    def remove(self,node):
        """ <h4>This function removes nodes from the front of the LinkedList
        
        - Before: {head}<[node]>{tail}
        - After:{head}<->{tail}
        """
        prev_node = node.prev
        next_node = node.next
        prev_node.next = node.next
        next_node.prev = prev_node
    def insert(self,node):
        """ <h3> This inserts at back of the linked list 
        
        ``` {prev_node}<[new node]>{tail} 
        ```
        """
        prev_node = self.tail.prev
        node.prev = prev_node
        prev_node.next  = node
        self.tail.prev = node
        node.next = self.tail
        
    def get(self,key):
        """
        <H4>This checks if the node key exist in cache
        
        if it does return the value there
        
        otherwise it returns -1
        <ul>
            <li>Key:{node}</li>
           
        </ul>
        """
        if key not in self.cache:
           return -1
        node = self.cache[key]#{node}
        self.remove(node)
        self.insert(node)
        return node.val
    def put (self,key,value):
        if key in self.cache:
            node = self.cache[key]
            #Update the node value
            node.val = value
            self.remove(node)
            self.insert(node)
            return
        #if the node does not exist
        node=ListNode(key,value)
        self.cache[key] =node
        self.insert(node)
        #it the capacity has been reached
        if len(self.cache) > self.capacity:
            lru = self.head.next
            self.remove(lru)
            del self.cache[lru.key]
        
    
#Test
if __name__ =="__main__":
    # Example from the problem statement
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)            # evicts key 2
    assert cache.get(2) == -1
    cache.put(4, 4)            # evicts key 1
    assert cache.get(1) == -1
    assert cache.get(3) == 3
    assert cache.get(4) == 4

    # Missing key on an empty cache
    cache = LRUCache(1)
    assert cache.get(1) == -1

    # Capacity 1: every new key evicts the previous one
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == -1
    assert cache.get(2) == 2

    # Updating an existing key changes the value and does not evict
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(1, 10)
    assert cache.get(1) == 10
    assert cache.get(2) == 2

    # Updating a key makes it most recently used
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(1, 10)           # 2 is now the least recently used
    cache.put(3, 3)            # evicts key 2
    assert cache.get(2) == -1
    assert cache.get(1) == 10
    assert cache.get(3) == 3

    # get makes a key most recently used
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.get(1)               # 2 is now the least recently used
    cache.put(3, 3)            # evicts key 2
    assert cache.get(2) == -1
    assert cache.get(1) == 1
    assert cache.get(3) == 3

    # A failed get does not change the order
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(99) == -1
    cache.put(3, 3)            # evicts key 1, the oldest
    assert cache.get(1) == -1
    assert cache.get(2) == 2
    assert cache.get(3) == 3

    # Without any access, eviction follows insertion order
    cache = LRUCache(3)
    for k in (1, 2, 3, 4, 5):
        cache.put(k, k)        # 4 evicts 1, 5 evicts 2
    assert cache.get(1) == -1
    assert cache.get(2) == -1
    assert [cache.get(k) for k in (3, 4, 5)] == [3, 4, 5]

    # Repeated gets of the same key
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    for _ in range(5):
        assert cache.get(1) == 1
    cache.put(3, 3)            # evicts key 2
    assert cache.get(2) == -1
    assert cache.get(1) == 1

    # A value of 0 is not treated as missing
    cache = LRUCache(2)
    cache.put(1, 0)
    assert cache.get(1) == 0

    # An evicted key can be inserted again
    cache = LRUCache(1)
    cache.put(1, 1)
    cache.put(2, 2)            # evicts key 1
    cache.put(1, 11)           # evicts key 2
    assert cache.get(2) == -1
    assert cache.get(1) == 11

    # Size never exceeds capacity
    cache = LRUCache(3)
    for k in range(20):
        cache.put(k, k)
        assert len(cache.cache) <= 3
    assert [cache.get(k) for k in (17, 18, 19)] == [17, 18, 19]
    assert cache.get(16) == -1

    # Forward and backward links stay consistent
    cache = LRUCache(3)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(3, 3)
    cache.get(1)
    cache.put(2, 22)
    cache.put(4, 4)            # evicts key 3
    forward, node = [], cache.head.next
    while node is not cache.tail:
        forward.append(node.key)
        node = node.next
    backward, node = [], cache.tail.prev
    while node is not cache.head:
        backward.append(node.key)
        node = node.prev
    assert forward == [1, 2, 4]
    assert backward == [4, 2, 1]

    print("All tests passed")
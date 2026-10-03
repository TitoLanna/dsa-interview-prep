"""
The next greater element of some element x in an array is the first greater element 
that is to the right of x in the same array.

You are given two distinct 0-indexed integer arrays nums1 and nums2, where nums1 is a subset of nums2.

For each 0 <= i < nums1.length, find the index j such that nums1[i] == nums2[j] and determine the next greater 
element of nums2[j] in nums2. If there is no next greater element, then the answer for this query is -1.

Return an array ans of length nums1.length such that ans[i] is the next greater element as described above.
"""


def nextGreaterElement(nums1,nums2):
    db={}
    ans =[0]* len(nums1)
    for  i in range(len(nums2)-1):
        # Store the value: next_value 
        db[nums2[i]] = db.get(nums2[i],0)+nums2[i+1]
    
    
    for i,val in enumerate (nums1):
        
      if val in db and  val < db[val]:
         ans[i] = db[val]
         
      else:
          ans[i] = -1   
        
        
    return ans
        
        




n1 = [2,4]
n2 = [1,2,3,4] 
res = nextGreaterElement(n1,n2)

print(res)
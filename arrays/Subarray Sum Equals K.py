""" 
Given an array of integers nums and an integer k, 
return the total number of subarrays whose sum equals to k.

A subarray is a contiguous non-empty sequence of elements within an array.

 

Example 1:

Input: nums = [1,1,1], k = 2
Output: 2

Example 2:

Input: nums = [1,2,3], k = 3
Output: 2
"""

def subbarraySum(nums,k):
    freq ={}
    ans=0
    n=len(nums)
    
    for i in range(n):
        freq[i]=nums[i]
        if freq[i]==k:
           ans+=1
        for j in range(i+1,n):
            freq[i] +=nums[j]
            if freq[i]==k:
               ans+=1
      
            
    return ans, freq
nums = [1,2,3]
print(subbarraySum(nums,3))
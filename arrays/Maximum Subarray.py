""" 
Given an integer array nums, find the subarray with the largest sum, and return its sum.

 

Example 1:

Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.
Example 2:

Input: nums = [1]
Output: 1
Explanation: The subarray [1] has the largest sum 1.
Example 3:

Input: nums = [5,4,-1,7,8]
Output: 23
Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.
"""
def maxSubArray(nums):
    """ 
    The Brute force approach.
    Time complexity of O(n**2)
    space complexity of O(1)
    """
    
    n = len(nums) 
    best_max=0
    for i in range(n-1):
        cur_max =0
        for j in range(i,n):
            cur_max+=nums[j]
            best_max =max(cur_max,best_max)         
    return best_max


def max_SubArray(nums):
    ans =nums[0]
    cur_sum=0
    for num in nums:
      if cur_sum < 0:
         cur_sum = 0
      cur_sum +=num 
      ans =ans if ans > cur_sum else cur_sum
            
    return ans


nums =[5,4,-1,7,8]

excepted_result = 6
res = maxSubArray(nums)
res2 = max_SubArray(nums)
print(res,"\n",res2)
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

def subarraySum(nums,k):
    """This is the brute force approach """
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
      
            
    return ans
#The Prefix Sum and Hashmap approach

def sub_array_Sum (nums, k):
    
    res =0
    cur_sum=0
    freq = {0:1}
    for num in nums:
        cur_sum+= num
        diff = cur_sum -k
        
        res += freq.get(diff,0)
        freq[cur_sum]=1+freq.get(cur_sum,0)
    return res

#Test Cases

test_cases =[
    {
        "input":[1,1,1],
        "k":2,
        "exp_output":2
    },
    { 
        "input":[1,2,3],
        "k":3,
        "exp_output":2
    }
]
for i,test in enumerate(test_cases):
    nums,k,expected= test["input"],test["k"],test["exp_output"]
    result = sub_array_Sum(nums,k)
    isPassed = True 
    if expected!= result:
        isPassed =False
        
    if isPassed:
        print(f"\n Loading...\ntest_[{i+1}]")
        print(f"{nums}:")
        print(f"result: {result}")
        print("Passed !")
    else:
        print(f"\nLoading... \ntest_[{i+1}]")
        print(f"{nums}:")
        print(f"result: {result}\t",f"Expected result:{expected}")
        print("\n Failed ! ")
         
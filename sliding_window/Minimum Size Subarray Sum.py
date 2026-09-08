

# Given a positive integer array and a target.
#write a function that return the minimum length of the 
# sub array whose element sum is equal to the target return 0 otherwise

"""
Follow up :
            if you figured out the O(n) solution,
            try coding another solution of which the time complexity is O(nlogn)
"""
def minSubArrayLen(target,nums):
    """
    This function takes 2 inputs an integet`target`
    and an integer array `nums` and return the sub array with 
    minimum length 
    
    Args:
            target(int): The integer input
            nums(int[]): The integer array
    Returns:
           minsubArrayLen(int): The minimum sub array length
    **Efficiency:**
            Time Complexity: O(n)
            Space Complexity: O(n)
    
    """
    
    
    l = 0
    cur_window_sum =0
    min_subLen = float("inf")
    
    
    for r in range(len(nums)):
        cur_window_sum += nums[r]
        
        while cur_window_sum >=target:
            min_subLen=min(min_subLen,r-l+1)
            cur_window_sum -=nums[l]
            l+=1    
    return 0 if min_subLen == float("inf") else min_subLen



#TEST
test_cases = [
    {
        "target":7,
        "nums":[2,3,1,2,4,3],
        "output": 2
            },
    {
        "target":4,
        "nums":[1,4,4],
        "output":1
         },
    {"target":11,
     "nums":[1,1,1,1,1,1,1,1],
     "output":0
         }
    
]
solution ={}
for i , test in enumerate ( test_cases):
    nums= test['nums']
    target = test['target']
    exp_output = test['output']
    res = minSubArrayLen(target,nums)
    solution[f"Test_[{i+1}]"]=(
        f"Passed ! [✅] |nums:{nums}\ttarget:{target}\t| Produced: {res} |Expected :{exp_output}"
        if res == exp_output 
        else
        f" Failed ! [❌]  |nums:{nums}\ttarget:{target}\t| Produced: {res} |Expected :{exp_output}"
    )
for test,result in solution.items():
    print(f"{test}:{result}")
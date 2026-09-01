# Give an integer array nums,
# write a function that returns True if any value  appears at least twice in the array
# and return False if every element is distinct
""" 
Example 1:

Input: nums = [1,2,3,1]

Output: true

Explanation:

The element 1 occurs at the indices 0 and 3.

Example 2:

Input: nums = [1,2,3,4]

Output: false

Explanation:

All elements are distinct.

Example 3:

Input: nums = [1,1,1,3,3,4,3,2,4,2]

Output: true
""" 

def containsDuplicate(nums):
    seen= set()
    
    for i in range(len(nums)):
        if nums[i] in seen:
            return True
        seen.add(nums[i])
    return False

#Test Cases

test_cases =[
    {
        "input":[1,1,1,3,3,4,3,2,4,2],
        "exp_output":True
    },
    {
       "input":[1,2,3,4],
        "exp_output":False
        },
    {
        "input":[1,2,3,1],
        "exp_output":True
     }
]

for i,test in enumerate(test_cases):
    nums= test["input"]
    exp_t = test["exp_output"]
    res = containsDuplicate(nums)
    print( f"Test Case[{i+1}]\t -> input: {nums} ","||","Passed" if exp_t == res else "Failed")




#Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, 
#find two numbers such that they add up to a specific target number. 
#Let these two numbers be numbers[index1] and numbers[index2] where 1 <= index1 < index2 <= numbers.length.

#Return the indices of the two numbers index1 and index2, 
# each incremented by one, as an integer array [index1, index2] of length 2.

#The tests are generated such that there is exactly one solution. 
# You may not use the same element twice.

#Your solution must use only constant extra space.

"""
Example 1:

Input: numbers = [2,7,11,15], target = 9
Output: [1,2]
Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].

Example 2:
Input: numbers = [2,3,4], target = 6
Output: [1,3]
Explanation: The sum of 2 and 4 is 6. Therefore index1 = 1, index2 = 3. We return [1, 3].

Example 3:

Input: numbers = [-1,0], target = -1
Output: [1,2]
Explanation: The sum of -1 and 0 is -1. Therefore index1 = 1, index2 = 2. We return [1, 2].
"""

def twoSumII(numbers,target):
    index_map ={}
    for idx,val in enumerate(numbers):
        #If index_1 + index_2 = target 
        #return [index_1,index_2]
        #Same as (target - index_1 = index_2)
        comp = target -val
        idx+=1
        if comp in index_map:
            return[index_map[comp] ,idx]
        index_map[val] = idx
    return []
        
     

#Test
test_case =[
    {
       "Input": [-1,0], 
       "target" :-1,
       "Output": [1,2] 
    },
    {
       "Input": [2,3,4], 
        "target" :6,
        "Output": [1,3]  
    },
    {
        "Input": [2,7,11,15], 
        "target" :9,
        "Output": [1,2]  
    }
]
for i,test in enumerate(test_case):
    nums=test["Input"]
    target=test["target"]
    exp_output= test["Output"]
    res=twoSumII(nums,target)
    print(f"Test [{i+1}] : ",f"Passed  [✅]{res}" if res ==exp_output else f"Failed [❌] \t Produced: {res} \t Expected: {exp_output}")

"""

You are given a 0-indexed integer array nums and an integer pivot. 
Rearrange nums such that the following conditions are satisfied:

Every element less than pivot appears before every element greater than pivot.
Every element equal to pivot appears in between the elements less than and greater than pivot.
The relative order of the elements less than pivot and the elements greater than pivot is maintained.
More formally, consider every pi, pj where pi is the new position of the ith element and pj is the new position of the jth element. 
If i < j and both elements are smaller (or larger) than pivot, then pi < pj.
Return nums after the rearrangement.

Example 1:

Input: nums = [9,12,5,10,14,3,10], pivot = 10
Output: [9,5,3,10,10,12,14]

Example 2:

Input: nums = [-3,4,3,2], pivot = 2
Output: [-3,2,4,3]

Constraints:

1 <= nums.length <= 105
-106 <= nums[i] <= 106
pivot equals to an element of nums.
"""
class Solution(object):
    def pivotArray(nums,pivot):
        less = []
        pivot_db =[]
        greater =[]
        for num in nums:
            if num < pivot:
                less.append(num)
            elif num == pivot:
                pivot_db.append(num)
            else:
                greater.append(num)
        return less+pivot_db+greater
def run_pivotArray(nums,pivot):
    return Solution.pivotArray(nums,pivot)
if __name__ =="__main__":
    Test =[
        ([[-3,4,3,2],2,[-3,2,4,3]]),#Example array with a negative
        ([[9,12,5,10,14,3,10],10,[9,5,3,10,10,12,14]]),#Example regular array
        ([[3,2],3,[2,3]]),#Only two element
        ([[2],2, [2]]) #One element
    ]
    
    for i , (arr,pivot,expected) in enumerate(Test,1):
        res = run_pivotArray(arr,pivot)
        assert res == expected, f"Test{i} failed expected{expected} -> Output:{res}"
        print(f"Test{i} passed arr{arr} pivot||{pivot} \t Output:{res} \t Expected: {expected}")
    print("Complete")
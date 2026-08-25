"""
You are given an array of integers NUMS and integer target,
return indices of the two numbers such that they add up to target

You may assume that each input would have exactly one solution,and you may not use
the same element twice.

You can  return the answer in any order.

Example 1:
nums =[2,7,11,15]
target = 9
return [0,1]

Example 2
nums =[3,2,4]
target = 6
return [1,2]

Example 3
nums = [3,3]
target 6
return [0,1]

Example 4 
nums = [3,2,3]
target = 6
return [0,2]

"""
@DeprecationWarning
def two_sum(arr, target):
    if len(arr)==2:
        return[0,1]
    if len(arr) < 2:
        return []
    
    res =[]
    j =0
    while j < len(arr)-1:
        i =j+1
        cur =arr[i] +arr[j]
        if cur == target:
            res.append(j)
            res.append(i)
        j+=1     
    return res
def two_sum(arr,target):
    
    num_to_index ={}
    
    for i,val in enumerate(arr):
        complement  = target -val
        print(num_to_index)
        if complement in num_to_index:
            return [num_to_index[complement],i]
        
        num_to_index[val]=i
    return []



print(two_sum([2,7,11,15],9))







"""num_to_index={}

        for i, num in enumerate(nums):
            complement= target-num
            if complement in num_to_index:
                return [num_to_index[complement],i]
            num_to_index[num]=i

        return []"""
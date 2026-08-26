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
"""
This code appeared to work only on two continuous index
and would not work for a problem like Example 4 which requires two distant index locations
"""

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
        
        if complement in num_to_index:
            return [num_to_index[complement],i]
        
        num_to_index[val]=i
    return []
"""
THOUGHT PROCESS:
For my second solution, using a hash map or dictionary to 
-store the complement"as Key" and the index "as the value"
follow an z = x+y reason , that if  y =z - x
we intially store y in a dictionary and later on if we come across the complement
we return the value of that complement and the current index "i"

Question I asked :
what happens when we have a complement like 3 in our num_to_index
for instance
3:0
and we come across another 3 at index 4 
when our target is 6.
nums =[3,2,1,2,3,5]
our current num_to_index{
    3:0,
    2:1,
    1:2,
    2:3,
    -->complement =3
    if 3 is in num_to_index:
    return[get_already_existing_complement->"3":0, current index]
    else:
    store the "current value" : index
}
"""



print(two_sum([2,7,11,15],9))







"""num_to_index={}

        for i, num in enumerate(nums):
            complement= target-num
            if complement in num_to_index:
                return [num_to_index[complement],i]
            num_to_index[num]=i

        return []"""
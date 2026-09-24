"""
You are given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue.

We will use the integers 0, 1, and 2 to represent the color red, white, and blue, respectively.

You must solve this problem without using the library's sort function.

"""
def sortColors(nums):
    """
    Solving this problem using a hashmap
    """
    
    hashmap ={}
    
    #Add elements to hashmap
    for i , val in enumerate(nums):
        hashmap[val] = hashmap.get(val,0)+1
    index =0
    
    for key in range(3):
        for _ in range(hashmap.get(key,0)):
            nums[index] = key
            index +=1
            
    return nums

            
nums =[1,0,2,1,2,0]
res = sortColors(nums)
print(f"Results:{res}")
    
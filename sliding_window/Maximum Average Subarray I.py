#Given an integer array nums of n elements and an integer K.
#Write a function that returns the maximum average of a contiguous subarray  whose 
#length is equal to k.
#Note: Any answer with a calculation error less than 10**-5  will be accepted.



""" 
SOLUTION:
A function that takes an array"nums" and an Integer"K"
and returns a float value
"""
def findMaxSubarray(nums: list[int],k:int)->float:
    left:int =0
        
    cur_window :float = float(sum(nums[left:k]))
    max_avg:float =  cur_window/k
    
    for right in range(k,len(nums)):

            #Add new element
        cur_window +=nums[right]
            #Remove first window element
        cur_window -=nums[left]
            #increase the left pointer
        left +=1
            #find Average of the current window
        cur_window_avg = cur_window/k

        max_avg = max(max_avg,cur_window_avg)
    return round(max_avg,5)
        


#TEST
test_cases =[
    {
        "input":[1,12,-5,-6,50,3],"k":4
        ,
        "output":12.75000
    },    {
        "input":[5],"k":1
        ,
        "output":5.00000
    },
     {
            "input":[3,3,4,3,0],"k":3
            ,
            "output":3.33333
        }
]
for idx,test in enumerate(test_cases):
    nums,k,exp_output = test["input"],test["k"],test["output"]
    res =findMaxSubarray(nums,k)
    print(
         f"Passed! ✅ |  Produced: {res} | Expected: {exp_output}"
                if res == exp_output
                else 
                f"Failed ❌ | Produced: {res} | Expected: {exp_output}"
                )

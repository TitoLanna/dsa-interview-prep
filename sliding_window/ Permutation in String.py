

""""

Given two strings `s1`and `s2`
 return `true` if `s2` contains a permutation of `s1`
 or `false` otherwise.
 In other words , return true if one of the `s1`'s permutaions is the substring of `s2`
 
"""
def checkInclusion(s1,s2):
    
    """
    Given two String `s1`and `s2`
    this is a function that  returns a boolean value if `s1`is a permutation of subString `s2`
    
    
    Args : Two input parameters
    S1 (str) 
    
    s2 (Str)
    Returns:
        boolean : True or False
    
    """
    if len(s1) > len(s2):
        return False
    
    s1Count ={}
    s2Count ={}
    
    # Count the element in the s1
    for i in range(len(s1)):
        s1Count[s1[i]]= s1Count.get(s1[i],0)+1

   #Lets first count the elements in s2
    left = 0
    
    for right in range(len(s2)):
        # Increase the count on the right element by 1
        s2Count[s2[right]] = s2Count.get(s2[right],0)+1
        # check is window size are the same
        if right-left+1 == len(s1):
            # check if the count in both windows are the same?
            if s1Count == s2Count:
              return True
            #remove the left character before sliding the window    
            s2Count[s2[left]]-=1
            if s2Count[s2[left]]==0:
                s2Count.pop(s2[left])
                
            # slide the window        
            left+=1    

    return False
    



#TEST

test_cases = [
    {
         "s1": "ab", "s2": "eidbaooo",
         "output":True
    },
    {
             "s1": "ab", 
             "s2": "eidboaoo",
             "output":False
        }
]

solutions ={}
for  i,test in enumerate(test_cases):
    s1,s2= test["s1"],test['s2']
    exp_res = test ["output"]
    result  = checkInclusion(s1,s2)
    
    solutions[i] = (
        f"Test_[{i+1}]... Passed !|| Output: {result} || Expected Output :{exp_res} " 
        if result == exp_res 
        else 
        f"Test_[{i+1}]... Failed !|| Output: {result} || Expected Output :{exp_res}"
    )
for test in solutions:
    print(solutions[test])
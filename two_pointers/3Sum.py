

#Given an integer array Nums
# return all the triplets
#[nums[i],num[j],nums[k]]
#such that :
# i != j
# i != k
# j != k,
# nums[i] + nums[j] + nums[k] == 0.




def _3Sum(nums):
    res =[]
    nums.sort()
    for i in range(len(nums)-2):
        if i > 0 and nums[i]==nums[i-1]:
            continue
        if nums[i]>0:
            break
        
        left = i+1
        print("left:",left)
        right = len(nums)-1
        print("right:",right)
        print("i: ",i)
        while left < right:
            total = nums[i]+ nums[left]+nums[right]
            if total ==0:
                res.append([nums[i],nums[left],nums[right]])
                left +=1
                right-=1
            
                while left < right and nums[left]== nums[left-1]:
                    left+=1
                
                while left  < right and nums[right]== nums[right+1]:
                    right-=1
                
            elif total < 0:
                left+=1
            else:
                right-=1
    return res
            
   


#Test
test_case =[
                {
                    "nums": [-1,0,1,2,-1,-4],
                    "Output": [
                            [-1,-1,2],
                            [-1,0,1]
                            ]
                },
                {
                    "nums": [0,1,1],
                    "Output": []
                },
                { 
                    "nums": [0,0,0],
                    "Output": [[0,0,0]]
                    }
            ]

solution ={}
for i,test in enumerate(test_case):
    res = _3Sum(test["nums"])
    exp_output = test["Output"]
    solution[f"Case_{i+1}"] = (f"Passed! [✅]{res} " 
                                     if res== exp_output 
                                     else 
                                     f"Failed [❌] \t Produced: {res} \t Expected: {exp_output}"
                                     )
for case in solution:
    print("Loading...")
    print(case ,solution[case])
        

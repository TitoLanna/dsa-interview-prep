
"""
Given an array of integers temperatures represents the daily temperatures, 
return an array answer such that answer[i] is the number of days you have
to wait after the ith day to get a warmer temperature. 
If there is no future day for which this is possible, keep answer[i] == 0 instead.
"""
def dailyTemperatures(temps):
    n = len(temps)
    result=[0]*n 
    stack = []# pair [temps,index]
    
    
    for i ,temp in enumerate(temps):
        while stack and temp > stack[-1][0]:
            stack_temp, stack_index = stack.pop()
            result[stack_index] = (i - stack_index)
        stack.append([temp, i])
        
    return result
       
               
                
            
            
        
        
   
    
    

    
temperatures = [73,74,75,71,69,72,76,73]
res = dailyTemperatures(temperatures) #[1,1,4,2,1,1,0,0]

print(res)
print('Passed' if res ==[1,1,4,2,1,1,0,0] else 'Failed')
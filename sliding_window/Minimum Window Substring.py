
"""
Give 2  strings s,t.
Write a function that returns the the minimun window substring of s 
where every t element is present.
return an empty string otherwise


Example 1:

Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
Explanation: The minimum window substring "BANC" includes 'A', 'B', and 'C' from string t.
Example 2:

Input: s = "a", t = "a"
Output: "a"
Explanation: The entire string s is the minimum window.
Example 3:

Input: s = "a", t = "aa"
Output: ""
Explanation: Both 'a's from t must be included in the window.
Since the largest window of s only has one 'a', return empty string.
"""

def minWindow(s,t):
    
    n = len(t)
    
    sCount = {}
    tCount = {}
    
    for i in range(n):
        tCount[t[i]] =tCount.get(t[i],0)+1
    
    l =0
    min_window_size = float("inf")
    window =(0,0)
    have,need = 0,len(tCount)
    
    for r,val in enumerate(s):
        sCount[val] = sCount.get(val,0)+1
        
        if val in tCount and sCount[val]== tCount[val]:
            have+=1
            
            while have == need:
                
                if (r-l+1)< min_window_size:
                    window=(l,r)
                    min_window_size=r-l+1
                sCount[s[l]]-=1
                if s[l] in tCount and sCount[s[l]]< tCount[s[l]]:
                    have-=1
                l+=1
    l,r =window            
    return s[l:r+1] if min_window_size!= float("inf") else ""
        
        
      
       
       
        
   
        
        
    
    
s = "ADOBECODEBANC"
t = "ABC"
print(minWindow(s,t))
    

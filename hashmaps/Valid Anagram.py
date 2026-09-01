# Given  two string S and T .
# Write a function the return True if T is an anagram of s 
# return False otherwise
""" 
Example 1:

Input: s = "anagram", t = "nagaram"

Output: true

Example 2:

Input: s = "rat", t = "car"

Output: false



"""
def isAnagram(s,t):
    #Helper function
    def helpme(s):
        freq={}
        for i in range( len(s)): 
            freq[s[i]] =freq.get(s[i],0)
            if s[i] in  freq:
               freq[s[i]]+=1
        return freq
    freq =helpme(s)
    freq_t=helpme(t)
    
    if freq_t == freq:
        return True
    return False

#s = "anagram"
#t = "nagaram"
#print(isAnagram(s,t))

#Test


test_cases=[
    {
        "input":
            {
             "s":"anagram",
             "t":"nagaram"
             }
        ,"output":True
        },
    {
                "input":
                    {
                     "s":"rat",
                     "t": "car"
                     }
                ,"output":False
                }
]
for i,test in enumerate(test_cases):
    s = test['input']['s']
    t=test['input']['t']
    exp_output = test['output']
    res = isAnagram(s,t)
    print(
        f"Test case [{i+1}]",
        "Passed ! "if res==exp_output else "Failed",
        f"\ninput:\ts->{s}\tt->{t}"
        )
         
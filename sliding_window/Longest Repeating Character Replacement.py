
""" 
    Given a string s and an integer k.
    You can choose any character of the string and change it 
    to  any other uppercase English character. 
    You can perform this operation at most k times.
"""
def characterReplacement(s,k):
    """ 
    
    Args: 
        s (str): The string .Example  s="ABAB"
        k (int): The integer . Example k =2
        
    Returns:
        int : The length of the longest substring containing the same letter

    `Time: O(n)`
    
    `Space : O(1)`
    """
    left = 0
    longest =0
    count =[0]* 26
    
    for r in range(len(s)):
        count[ord(s[r]) -65]+=1
        
        while (r-left+1) - max(count)> k:
            count[ord(s[left])-65]-=1
            left+=1
        longest= max(longest,r-left+1)
        
    return longest
   
        


s=  "ABAB"
k = 2
print(characterReplacement(s,k))
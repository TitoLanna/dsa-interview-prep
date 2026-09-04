#Given a string s, return true if the s can be palindrome after deleting at most one character from it
"""
Example 1:

Input: s = "aba"
Output: true
Example 2:

Input: s = "abca"
Output: true
Explanation: You could delete the character 'c'.
Example 3:

Input: s = "abc"
Output: false
 
"""
def validPalindrome(s):
    l,r= 0,len(s)-1
    
    def isPalindrome(left,right):
        while left<right:
            if s[left]!=s[right]:
                return False
            left+=1
            right-=1
        return True
    
    while l< r:
        if s[l]!= s[r]:
            return(
                isPalindrome(l+1,r)
                or
                isPalindrome(l,r-1)
            )
        l+=1
        r-=1
    return True
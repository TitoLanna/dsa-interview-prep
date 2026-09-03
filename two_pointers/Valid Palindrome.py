#A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters,
# it reads the same forward and backward. Alphanumeric characters include letters and numbers.

# Given a string s, return true if it is a palindrome, or false otherwise.

 
"""
Example 1:

Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.

Example 2:

Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.

Example 3:

Input: s = " "
Output: true
Explanation: s is an empty string "" after removing non-alphanumeric characters.
Since an empty string reads the same forward and backward, it is a palindrome.
"""
def ispalindrome(s):
    #Time : O(1)
    #Space: O(1)
    """ 
    This is very good for interviews the while loops helps if you do not know 
    ahead of time the number of elements in the string
    """
    
    l = 0
    r = len(s)-1
    while l< r:    
        while  l < r and not s[l].isalnum():
            l+=1
            
        while l<r and not s[r].isalnum():
            r-=1
        if s[l].lower()!= s[r].lower():
            return False
        l+=1
        r-=1
    return True

#An alternative approach
#Time: O(n) 
#Space: O(n)
def is_palindrome(s):
    clean ="".join(char.lower() for char in s if char.isalnum())
    return clean ==clean[::-1]
    
s="race a car"
print ("Initial function ")
print(ispalindrome(s))

print ("Second function ")
print(is_palindrome(s))
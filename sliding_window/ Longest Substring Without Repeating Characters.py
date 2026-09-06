
# Given a string s.
# write a function the returns the length of the longest substring without duplicate characters






def longestSubstring_length(s):
    """
    Takes in a string and returns an integer.

    Args:
        s (str): The input string.

    Returns:
        int: The length of the longest substring
            without repeating characters.

    Efficiency:
        Time Complexity: O(n^2)
        Space Complexity: O(n)
    """
    
    l =0
    subStrings={}
    r=0
    #Handle empty array
    if len(s)< 1:
        return 0
    while l <= r and r < len(s):
         cur_subString = s[l:r]
         if s[r] not in cur_subString:
             r+=1
             cur_subString =s[l:r]
             subStrings[cur_subString]=len(cur_subString)
         else:
             l+=1
             
    return max(subStrings.values())
def lengthOfLongestSubstring(s):
        """
        Takes in a string and returns an integer.

        Args:
            s (str): The input string.

        Returns:
            int: The length of the longest substring
                 without repeating characters.

        Efficiency:
            Time Complexity: O(n)
            Space Complexity: O(n)
        """

        left = 0
        max_length = 0
        seen = {}

        for right, char in enumerate(s):

            if char in seen and seen[char] >= left:
                left = seen[char] + 1

            seen[char] = right

            max_length = max(
                max_length,
                right - left + 1
            )

        return max_length




#TEST

test_cases =[
    {
        "input":"abcabcbb" ,
        "output":3
            
    },
    {
            "input":"bbbbb" ,
            "output":1
                
        }
    ,{
            "input":"pwwkew" ,
            "output": 3
                
        },
    {
        "input":"S",
        "output":1
    },
    {
       "input":"",
        "output":0 
    }
]

for i,test in enumerate(test_cases):
    s,exp_output = test["input"],test["output"]
    res = longestSubstring_length(s)
    print(
        f"Test Case {i+1}|",f"Passed! ✅ |  Produced: {res} | Expected: {exp_output}"
        if res == exp_output
        else 
        f"Failed ❌ | Produced: {res} | Expected: {exp_output}"
    )
  
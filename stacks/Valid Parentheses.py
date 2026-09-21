"""
Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:

Open brackets must be closed by the same type of brackets.
Open brackets must be closed in the correct order.
Every close bracket has a corresponding open bracket of the same type.


"""
def isValid(s):
    brackets ={"(":")","{":"}","[":"]"}
    stack =[]
   
    for char in s:
        if char in brackets:
            stack.append(char)
        elif stack and brackets[stack[-1]] == char:
            stack.pop()
        else:
            return False
    return True if not stack else False 
              

print(isValid("[]{}()"))
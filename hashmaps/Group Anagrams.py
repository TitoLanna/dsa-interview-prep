#Given an array of strings,
#write a function that groups the anagrams together 
# and return the array 
"""
Example 1
 
Input: strs = ["eat","tea","tan","ate","nat","bat"]

Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

Example 2

Input: strs = [""]

Output: [[""]]

Example 3:

Input: strs = ["a"]

Output: [["a"]]


"""
def groupAnagram(strs):#O(n*K*logK)
   anagram ={}
   
   for word in strs:#O(n)
       sorted_word = "".join(sorted(word))#O(klogK)sorting algorithm
       if sorted_word in anagram:
           anagram[sorted_word].append(word)
       else:
           anagram[sorted_word] = [word]
   return list(anagram.values()) 
def groupAnagram(strs): 
    anagram={}
    for word in strs:
        count =[0]* 26 #a...z 
        for char in word:
            count[ord(char)-ord('a')]+=1 # a->80 b->81 81-80= 1 index location add 1
        key = tuple(count)
        if key not in anagram:
            anagram[key]=[word]
        else:
            anagram[key].append(word)
    return list(anagram.values())
    
#TEST
test_cases =[
    {
        "input":["eat","tea","tan","ate","nat","bat"],
        "output":[["bat"],["nat","tan"],["ate","eat","tea"]]
        },
    {
        "input":[""],
        "output":[[""]]     
        },
    {
        "input":["a"],
        "output":[["a"]]  
    }
    
    
]
for i,test in enumerate(test_cases):
    res = groupAnagram(test["input"])
    
    
    print(f"Test [{i+1}]\t{test["input"]} \t {res}")

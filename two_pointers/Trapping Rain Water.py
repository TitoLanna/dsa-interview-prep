
#Given n non-negative integers representing an elevation map where the width of each bar is 1, 
# compute how much water it can trap after raining.


# 11|
# 10|                                        _____
#  9|                                        |   |
#  8|            ______            ______    |   |
#  7|            |    |            |    |    |   |
#  6|            |    |            |    |    |   |
#  5|            |    |            |    |    |   |
#  4|            |    |            |    |____|   |
#  3|        ____|    |         ___|    |    |   |
#  2|___    |    |    |     ___|   |    |    |   |
#  1|   |   |    |    |    |   |   |    |    |   |
#  0|------------------------------------------------->
#[1,0,2,7,0,1,2,7,3,9]
def trap(h):
    if not h: return 0
    trapped_water =0
    l,r = 0,len(h)-1
    leftMax,rightMax = h[l],h[r]
    
    while l< r:
       
       if leftMax < rightMax:
           l+=1
           leftMax =max(leftMax,h[l]) 
           trapped_water+=leftMax -h[l]
       else:
           r-=1
           rightMax= max(rightMax,h[r])
           trapped_water+= rightMax-h[r]
              
    return trapped_water



#TEST
test_cases =[
    {
        "input":[0,1,0,2,1,0,1,3,2,1,2,1],
        "expected":6
    },
    {
        "input":[4,2,0,3,2,5],
        "expected":9
    }
]

import sys

solution = {}

total = len(test_cases)

for i, test in enumerate(test_cases):

    # Run test
    result = trap(test["input"])
    expected = test["expected"]

    # Store result
    solution[f"Case_{i + 1}"] = (
        "Passed! ✅"
        if result == expected
        else f"Failed ❌ | Produced: {result} | Expected: {expected}"
    )

    # Progress
    current = i + 1
    percent = current / total

    bar_length = 30
    filled = int(bar_length * percent)

    bar = "█" * filled + "░" * (bar_length - filled)

    sys.stdout.write(
        f"\rLoading test cases [{bar}] {int(percent * 100)}%"
    )
    sys.stdout.flush()


print("\n")

# Display results
for case, result in solution.items():
    print(f"{case}: {result}")

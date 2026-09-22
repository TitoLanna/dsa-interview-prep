"""
You are given an integer array prices where prices[i] is the price of the ith item in a shop.

There is a special discount for items in the shop. 
If you buy the ith item, then you will receive a discount equivalent to prices[j] 
where j is the minimum index such that j > i and prices[j] <= prices[i]. Otherwise, you will not receive any discount at all.

Return an integer array answer where answer[i] is the final price you will pay for the ith item of the shop, considering the special discount.

"""

def finalPrices(prices):
    results = prices
    stack =[] #pairs :[price,index]
    for i, price in enumerate(prices):
        while stack and price <= stack[-1][0]:
            stack_p,stack_id  = stack.pop()
            results[stack_id] = (stack_p - price)
        stack.append([price,i])
    return results
    

prices =[8,4,6,2,3]
res = finalPrices(prices)

print(res)

print("Passed" if res ==[4,2,4,2,3] else "Failed")
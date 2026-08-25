""" 
You are given an array PRICES where PRICES[i]is the price of a given stock on the ith day

You want to maximize your profit by choosing a single day to buy one stock and a different day 
in the future to sell that stock.

Return the maximum  profit you can achieve from the transaction. If you cannot achieve any profit
return 0


Example 1

Input: prices = [7,1,5,3,6,4]
Output: 5

Example 2

Input: prices = [7,6,4,3,1]
Output: 0
"""

def max_profit(prices):
    
    cheapest_stock =prices[0]
    largest_profit = 0
    for i,val in enumerate(prices):
        #find the cheapest stock
        cheapest_stock= min(cheapest_stock,val)
        cur_max =val - cheapest_stock
        largest_profit = max(cur_max,largest_profit)
        
        
    
        
    return largest_profit

print(max_profit([7,1,5,3,6,4]))
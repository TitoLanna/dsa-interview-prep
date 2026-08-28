""" 
Given an m x n matrix, return all elements of the matrix in spiral order.

Example 1
Input: matrix = [
                 [1,2,3],
                 [4,5,6],
                 [7,8,9]
                 ]
Output: [1,2,3,6,9,8,7,4,5]

Example 2
Input: matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
Output: [1,2,3,4,8,12,11,10,9,5,6,7]

"""

def spiralOrder( matrix):
    res =[]
    n=len(matrix)
    left=0 # Moves left
    right=len(matrix[0]) #Moves right
    top =0 # Moves down
    bottom=n # Moves Up
   
    while left < right and top < bottom:
        # Move  to right ->
        for i in range(left,right):
            a =matrix[top][i]
            res.append(a)
        top+=1
        #Move down
        for  i in range(top,bottom):
            a = matrix[i][right-1]
            res.append(a)
        right-=1
        if  not(left < right and top < bottom):
                    break
        
        # Move to left <-
        for i in range(right-1,-1,-1):
            a = matrix[bottom-1][i]
            res.append(a)
        bottom-=1
        
        #Move up
        for i in range(bottom-1,top-1,-1):
            a = matrix[i][left]
            res.append(a)
        left+=1
        
        print(res)
    
    return res


matrix= [
          [1,2,3,4]
         ,[5,6,7,8],
          [9,10,11,12]
          ]

expected_output =[1,2,3,4,8,12,11,10,9,5,6,7]
result =spiralOrder(matrix)
print(result==expected_output)

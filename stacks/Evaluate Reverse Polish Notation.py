

def reverse_polish_notation(arr):
    """
    Evaluate an arithmetic expression written in Reverse Polish Notation.

    Scans the tokens left to right using a stack. Operands are pushed onto the
    stack; when an operator is seen, the top two operands are popped, the
    operator is applied, and the result is pushed back. After the last token,
    the single value left on the stack is the answer.

    Note that the first value popped is the right-hand operand (b) and the
    second is the left-hand operand (a), so each operator lambda takes (b, a)
    and computes "a <op> b". This matters for the non-commutative operators
    '-' and '/'.

    Args:
        arr (list[str]): Tokens of a valid RPN expression. Each token is
            either an integer string (e.g. "4", "-13") or one of the
            operators '+', '-', '*', '/'.

    Returns:
        int: The value of the expression. Division truncates toward zero
            (e.g. 13 / 5 -> 2, -7 / 2 -> -3), not toward negative infinity.

    Example:
        >>> reverse_polish_notation(["2", "1", "+", "3", "*"])  # (2 + 1) * 3
        9
        >>> reverse_polish_notation(["4", "13", "5", "/", "+"])  # 4 + (13 / 5)
        6

    Complexity:
        Time:  O(n), each token is processed once.
        Space: O(n), the stack can hold up to n operands in the worst case.
    """
    operators = {
            "+": lambda b , a:a+b,
            "-": lambda b , a:a-b,
            "*": lambda b , a:a * b,
            "/": lambda b , a: int(float(a / b))
    }
        
   
    stack =[]
    for element in arr:
        if element not in operators:
            stack.append(int(element))
        else:
           # a = stack.pop()
           
           # b = stack.pop()
            
            stack.append(
                operators[element](
                stack.pop(),
                stack.pop()
                                 )
                         )
    return stack[-1]

tokens = ["4","13","5","/","+"]
res = reverse_polish_notation(tokens)#((2 + 1) * 3) = 9
print(res)
    
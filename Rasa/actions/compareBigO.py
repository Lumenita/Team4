from sympy import *

def tokenize(the_text):
        the_text = the_text.split()
        bigO = []
        for x in the_text:
            if x.find("(") == 1:
                bigO.append(x.lstrip("O"))
        return bigO

def compare_functions(the_text):
        x, y, z, n = symbols("x y z n")
        func1 = the_text[0]
        func2 = the_text[1]
        top = sympify(func1)
        bot = sympify(func2)
        expr = (top / bot)

        result = limit(expr, n, oo)

        if (result == 0):
            return f'O({top}) < O({bot})'
        elif (result == oo):
            return f'O({top}) > O({bot})'
        else:
            return f'O({top}) = O({bot})'


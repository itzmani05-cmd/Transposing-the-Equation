import re

equation = 'V=IR'
getting_input = "R"

print("Equation:", equation)
print("Getting_input:", getting_input)

def spliting_equation(equation):
    equation = equation.replace(" ", "")
    print("Splitting_Equation: ",equation)
 
    result = []
    term = ""
    print("Equation",equation)
    
    for char in equation:
        if char in "+-":  
            if term:  
                result.append(term)
            term = char  
        else:
            term += char  
    if term:
        result.append(term)
        
    print("Result: ",result)
    return result
   
    
def lhsRhs(lhs, rhs, variable):
    left_side = []
    right_side = []

    lhs_terms = spliting_equation(lhs)
    rhs_terms = spliting_equation(rhs)

    print("LHS terms:", lhs_terms)
    print("RHS terms:", rhs_terms)

    for term in lhs_terms:
        term = term.strip()
        if term and getting_input in term:
            left_side.append(term)
        else:
            if term.startswith("-"):
                right_side.append(f"+{term[1:]}")
            elif term.startswith("+"):
                right_side.append(f"-{term[1:]}")
            else:
                right_side.append(f"-{term}")

    for term in rhs_terms:
        term = term.strip()
        if term and getting_input in term:
            if term.startswith("-"):
                left_side.append(f"+{term[1:]}")
            elif term.startswith("+"):
                left_side.append(f"-{term[1:]}")
            else:
                left_side.append(f"-{term}")

        else:
            if term.startswith("-") or term.startswith("+"):
                right_side.append(term)
            else:
                right_side.append(f"+{term}")
                
    print("1LHS terms:", left_side) 
    print("1RHS terms:", right_side)
    
    return left_side, right_side

def left_side_constant(expression):
   
    coefficient = ""
    
    for char in expression:
        if char.isdigit() or char in "+-":
            coefficient += char
        else:
            break  
        
    if coefficient in ["", "+", "-"]:
        coefficient += "1"

    return int(coefficient)


if '=' not in equation:
    print("Invalid equation")
    
else:
    lhs, rhs = equation.split("=")
    lhs_terms = re.findall(r"[+-]?\w+\^?\d*|\w+", lhs)
    rhs_terms = re.findall(r"[+-]?\w+\^?\d*|\w+", rhs)
    tokens = lhs_terms + rhs_terms
    print("Extracted Terms:", tokens)
    
    found = False
    for element in tokens:
        if getting_input in element :
            left_side, right_side = lhsRhs(lhs, rhs, getting_input)
            left_side_str = "".join(left_side)
            right_side_str = "".join(right_side)  
                
            print("Left side str:", left_side_str)
            print("Right side str:", right_side_str)

            coefficient = left_side_constant(left_side_str)
            print("Coefficient of variable:", coefficient)
            dividing = '/'
            
            try:
                if coefficient and coefficient != 0:
                    print("1")
                    print("Output:",left_side_str, "=", right_side_str)

                else:
                    print("2")
                    if left_side_str.startswith("-"):
                        right_side_str = right_side_str.replace(" ", "")
                        right_side_str = right_side_str.replace("-","+")
                        right_side_str = right_side_str.replace("+","-")
                        left_side_str = left_side_str[1:]
                    if left_side_str.startswith("+"):
                        left_side_str = left_side_str[1:]
                    print("Output:", left_side_str, "=", right_side_str)

            except Exception as e:
                print("Error evaluating right side:", e)

            found = True
            break  

    if not found:
        print("Variable is not found in the equation")

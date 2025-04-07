import re

def tokenize_equation(equation):
    tokens = []
    temp = ""
    
    for char in equation:
        if char.isalpha() or char == "^" or char == "_":  
            if temp and temp[-1].isdigit():  
                tokens.append(temp)
                temp = ""
            temp += char  
        elif char.isdigit():
            if temp and temp[-1].isalpha():  
                tokens.append(temp)
                temp = ""
            temp += char
        else:
            if temp:
                tokens.append(temp)
                temp = ""
            tokens.append(char)  

    if temp:
        tokens.append(temp)
    
    print("Token: ",tokens)
    return tokens

def process_tokens(tokens):
    numbers = []
    variables = []

    for token in tokens:
        if token.isdigit():
            numbers.append(int(token))  
        else:
            variables.append(token) 

    result = 1
    for num in numbers:
        result *= num

    final_expression = str(result) + "".join(variables) if numbers else "".join(variables)

    print("Final Expression: ",final_expression)

    return final_expression

def parse_equation(expression):
    terms = re.findall(r"[+-]?\d*[a-zA-Z]+|[+-]?\d+|[+-]", expression)
    return terms

def is_num_without_signs(coefficient_part):
    if not coefficient_part:
        return False
    if coefficient_part[0] in "+-":
        coefficient_part = coefficient_part[1:]
    return coefficient_part.isdigit()

def is_target_variable(term, variable):
    if term.endswith(variable):
        coefficient_part = term[:-len(variable)] 
        return coefficient_part == "" or coefficient_part in ["+", "-"] or is_num_without_signs(coefficient_part)
    return False

def lhs_rhs(lhs, rhs, variable):
    left_side, right_side = [], []
    lhs_terms = parse_equation(lhs)
    rhs_terms = parse_equation(rhs)

    for term in lhs_terms:
        term = term.strip()
        if term and is_target_variable(term, variable):
            left_side.append(term) 
        else:
            if term.startswith("-"):
                right_side.append(term[1:])  
            else:
                right_side.append(f"-{term}") 

    for term in rhs_terms:
        term = term.strip()
        if term and is_target_variable(term, variable):
            if term.startswith("-"):
                left_side.append(term[1:]) 
            else:
                left_side.append(f"-{term}") 
        else:
            if term.startswith("-") or term.startswith("+"):
                right_side.append(term) 
            else:
                right_side.append(f"+{term}") 

    print("LeftSide: ",left_side)
    print("RightSide: ",right_side)

    return left_side, right_side

def process_equation(equation, getting_input):
    if '=' not in equation:
        print("Invalid equation")
        return
    
    lhs, rhs = equation.split("=")
    if not getting_input.isalnum():
        print("Variable is invalid")
        return    
    
    tokens = re.findall(r"-?\d*[a-zA-Z]+|[a-zA-Z]+|\d+|[+\-*/=]", equation)
    elements = []
    for token in tokens:
        contains_letter = False
        for char in token:
            if char.isalpha():
                contains_letter = True
                break  
        if contains_letter:
            elements.append(token)

    selected_list = []
    for item in elements:
        variable_part = ""
        for char in item:
            if char.isalpha():  
                variable_part += char
        selected_list.append(variable_part)


    print("Elements:", elements)
    print("Selected_list:", selected_list)
    
    if getting_input in selected_list:
        left_side, right_side = lhs_rhs(lhs, rhs, getting_input)
        left_side_str = " + ".join(left_side)
        right_side_str = " ".join(right_side)  

        print("Left Side Str: ",left_side_str)
        print("Right Side Str: ", right_side_str)

        print("Output:", left_side_str, "=", right_side_str)

    else:
        print("Variable is not found in the equation")


equation = "x2x*2x_3"
print("Equation:", equation)
tokens = tokenize_equation(equation)
print("Tokens:", tokens)
final_expression = process_tokens(tokens)
print("Final Expression:", final_expression)

equation = "apple = 4e - orange + 5a + 4"
getting_input = "x"
print("Processing equation:", equation)
process_equation(equation, getting_input)
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
    
    # Tokenize and process each side
    lhs_tokens = tokenize_equation(lhs)
    rhs_tokens = tokenize_equation(rhs)

    lhs_processed = process_tokens(lhs_tokens)
    rhs_processed = process_tokens(rhs_tokens)

    print("Processed LHS:", lhs_processed)
    print("Processed RHS:", rhs_processed)

    lhs_terms = parse_equation(lhs_processed)
    rhs_terms = parse_equation(rhs_processed)

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

    return left_side, right_side

def process_equation(equation, getting_input):
    if '=' not in equation:
        print("Invalid equation")
        return
    
    lhs, rhs = equation.split("=")
    if not getting_input.isalnum():
        print("Variable is invalid")
        return    

    left_side, right_side = lhs_rhs(lhs, rhs, getting_input)
    left_side_str = "+".join(left_side)
    right_side_str = "".join(right_side)  

    print("Final Output:", left_side_str, "=", right_side_str)

# Example Usage
equation = "apple = 4e - orange + 5a + 4 + x_4*4"
getting_input = "e"
print("\nProcessing equation:", equation)
process_equation(equation, getting_input)

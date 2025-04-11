from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sympy import symbols, Eq, solve, sympify
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

# CORS middleware setup to allow React frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EquationRequest(BaseModel):
    equation: str
    solve_for: str


def preprocess_equation(equation_str):
    print("Equation_str",equation_str)
    equation_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', equation_str)
    print("Equatino_str2",equation_str)
    equation_str = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', equation_str)
    print("Equatino_str3",equation_str)

    return equation_str

@app.post("/")
def solve_equation(data: EquationRequest):
    try:
        if "=" not in data.equation:
            raise ValueError("Equation must contain '=' sign")

        process = data.equation
        processed = preprocess_equation(process)
        print("Processed",processed)
        lhs_str, rhs_str = processed.split("=")
        lhs = sympify(lhs_str.strip())
        print("LHS",lhs)
        rhs = sympify(rhs_str.strip())
        print("RHS",rhs)

        
        eq = Eq(lhs, rhs)
        print("Eq",eq)
        variable = symbols(data.solve_for)
        print("variable",variable)
        solution = solve(eq, variable)
        print("solution",solution)

        if not solution:
            return {"solution": [f"No solution for {data.solve_for}"]}

        string_solutions = [f"{data.solve_for} = {sol}" for sol in solution]
        return {"solution": string_solutions}

    except Exception as e:
        raise HTTPException(status_code=400, detail="Error")

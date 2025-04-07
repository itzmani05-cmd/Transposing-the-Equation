from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sympy import symbols, Eq, solve, sympify
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware setup to allow React frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for incoming request body
class EquationRequest(BaseModel):
    equation: str
    solve_for: str

@app.post("/")
def solve_equation(data: EquationRequest):
    try:
        if "=" not in data.equation:
            raise ValueError("Equation must contain '=' sign")

        lhs_str, rhs_str = data.equation.split("=")
        lhs = sympify(lhs_str.strip())
        rhs = sympify(rhs_str.strip())

        
        eq = Eq(lhs, rhs)
        variable = symbols(data.solve_for)
        solution = solve(eq, variable)

        if not solution:
            return {"solution": [f"No solution for {data.solve_for}"]}

        # Convert solution to readable format
        string_solutions = [f"{data.solve_for} = {sol}" for sol in solution]
        return {"solution": string_solutions}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

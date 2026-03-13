import os
from parser.dsl import DSL

# Load the dual.lp file
dual_path = os.path.join(os.path.dirname(__file__), "..", "examples", "dual.lp")
problem = DSL(dual_path)

# Create dual simplex solver
dual_solver = problem.to_dual_simplex()

# Solve
solution, optimal_value = dual_solver.solve()

print(f"Solution: {solution}")
print(f"Optimal value: {optimal_value}")

# Expected: x1=0, x2=4, z=4 (from earlier calculation)
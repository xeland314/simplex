from dsl import DSL

# Load the dual.lp file
problem = DSL("dual.lp")

# Create dual simplex solver
dual_solver = problem.to_dual_simplex()

# Solve
solution, optimal_value = dual_solver.solve()

print(f"Solution: {solution}")
print(f"Optimal value: {optimal_value}")

# Expected: x1=0, x2=4, z=4 (from earlier calculation)
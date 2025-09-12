import re
import os
from advanced_simplex import Simplex
from functions import AlgebraicExpression, ObjectiveFunction


class DSL:
    def __init__(self, problem: str):
        if os.path.exists(problem):
            with open(problem, 'r') as f:
                self.problem = f.read()
        else:
            self.problem = problem
            
        self.objective_function = None
        self.constraints = []
        self.method = None
        self._parse_problem()

    def _parse_problem(self):
        lines = self.problem.strip().split('\n')
        
        # Parse method and objective function
        first_line = lines[0].strip()
        if first_line.lower() in ['maximize', 'minimize']:
            self.method = Simplex.MAXIMIZE if first_line.lower() == 'maximize' else Simplex.MINIMIZE
            obj_func_line = lines[1]
        else:
            match = re.match(r'(MINIMIZE|MAXIMIZE) (.*)', first_line, re.IGNORECASE)
            if not match:
                raise ValueError("Invalid problem format: Missing MINIMIZE/MAXIMIZE")
            self.method = Simplex.MINIMIZE if match.group(1).upper() == 'MINIMIZE' else Simplex.MAXIMIZE
            obj_func_line = match.group(2).strip()

        if ':' in obj_func_line:
            obj_func_name = obj_func_line.split(':')[0].strip()
            obj_func_expr = obj_func_line.split(':')[1].strip()
            self.objective_function = ObjectiveFunction(f"{obj_func_name} = {obj_func_expr}")
        else:
            self.objective_function = ObjectiveFunction(obj_func_line)

        # Parse constraints and bounds
        in_constraints_section = False
        in_bounds_section = False
        for line in lines[1:]:
            line = line.strip()
            if not line or line.lower() == 'end':
                continue
            if line.upper() == 'SUBJECT TO':
                in_constraints_section = True
                in_bounds_section = False
                continue
            if line.upper() == 'BOUNDS':
                in_bounds_section = True
                in_constraints_section = False
                continue
            
            if in_constraints_section:
                if ':' in line:
                    constraint_str = line.split(':')[1].strip()
                    self.constraints.append(AlgebraicExpression(constraint_str))
                else:
                    self.constraints.append(AlgebraicExpression(line))
            elif in_bounds_section:
                if 'free' in line.lower():
                    var_name = line.split(' ')[0]
                    self._handle_free_variable(var_name)
                else:
                    self.constraints.append(AlgebraicExpression(line))

    def _handle_free_variable(self, var_name: str):
        var_plus = f"{var_name}_plus"
        var_minus = f"{var_name}_minus"

        # Handle objective function
        if var_name in self.objective_function.terms:
            coefficient = self.objective_function.terms[var_name]
            del self.objective_function.terms[var_name]
            self.objective_function.terms[var_plus] = coefficient
            self.objective_function.terms[var_minus] = -coefficient

        # Handle constraints
        for constraint in self.constraints:
            if var_name in constraint.terms:
                coefficient = constraint.terms[var_name]
                del constraint.terms[var_name]
                constraint.terms[var_plus] = coefficient
                constraint.terms[var_minus] = -coefficient

        self.constraints.append(AlgebraicExpression(f"{var_plus} >= 0"))
        self.constraints.append(AlgebraicExpression(f"{var_minus} >= 0"))

    def to_simplex(self) -> Simplex:
        # Update number of variables
        all_vars = set()
        all_vars.update(self.objective_function.variables)
        for c in self.constraints:
            all_vars.update(c.variables)
        
        return Simplex(
            num_variables=len(all_vars),
            objective_function=self.objective_function,
            method=self.method,
            constraints=self.constraints,
        )

from decimal import Decimal
import re
from math_expression import MathExpression

class ObjectiveFunction(MathExpression):
    """
    Represents an objective function in the form "f(x) = a*x1 + b*x2 + ...".

    This class parses a string representation of an objective function to extract
    its name, coefficients, and variables.
    """

    def __init__(self, expression: str) -> None:
        super().__init__(expression)
        self._parse_expression()
        self._generate_representation()

    def _generate_representation(self) -> None:
        self.representation = f"{self.function_name} = "
        terms_str = []
        for variable, coefficient in self.terms.items():
            if coefficient == 1:
                terms_str.append(f"{variable}")
            elif coefficient == -1:
                terms_str.append(f"- {variable}")
            elif coefficient < 0:
                terms_str.append(f"- {-coefficient} * {variable}")
            else:
                terms_str.append(f"{coefficient} * {variable}")
        self.representation += " + ".join(terms_str)
        self.representation = self.representation.replace("+ -", "-")

    def _parse_expression(self) -> None:
        """
        Parses the objective function string to find its name, coefficients, and variables.

        The function must be in the format: "f(x) = ax1 + bx2 + ... + cxn".
        """
        left_side, right_side = self.expression.split('=')
        self.function_name = left_side.strip()

        # The regex for extracting terms can be a bit complex.
        # This regex tries to capture coefficients (including implicit ones like +1, -1, or absent)
        # and the variables.
        # Pattern: [sign][spaces][optional coefficient][spaces][* optional][spaces][variable]
        term_pattern = re.compile(r'([+-]?\s*\d*\.?\d*\s*\*?)\s*(\w+)')

        for match in term_pattern.finditer(right_side):
            coefficient_str, variable = match.groups()

            # Clean the coefficient string
            cleaned_coefficient_str = coefficient_str.replace(' ', '').replace('*', '')

            # Determine the numerical value of the coefficient
            if cleaned_coefficient_str in ['', '+']:
                coefficient_value = Decimal(1)
            elif cleaned_coefficient_str == '-':
                coefficient_value = Decimal(-1)
            else:
                coefficient_value = Decimal(cleaned_coefficient_str)

            # Add the coefficient to the terms
            self.terms[variable] += coefficient_value

            # Add the variable to the list of ordered variables if it is not already there
            if variable not in self.ordered_variables:
                self.ordered_variables.append(variable)

    @staticmethod
    def is_an_objective_function(function: str) -> bool:
        """
        Determines if a given string represents a valid algebraic function.

        Args:
            function (str): A string representing a possible algebraic function.

        Returns:
            bool: True if the string represents a valid algebraic function, False otherwise.
        """
        # Verify that the string contains an equal sign
        # Define the regular expression to validate algebraic functions
        is_a_function = True
        try:
            f = ObjectiveFunction(function)
            is_a_function &= f.function_name not in f.ordered_variables
        except Exception:
            pass
        finally:
            function_regex = r'^\s*[a-zA-Z]+\d?\s*(\(\w+\d?\))?\s*=\s*([+-]?\s*\d*\*?\s*[a-zA-Z]+\d*\s*)+\s*$'
            is_a_function &= bool(re.match(function_regex, function))
        return is_a_function

    def __repr__(self) -> str:
        return f"ObjectiveFunction({self.representation})"

    def __str__(self) -> str:
        return self.representation
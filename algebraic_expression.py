from decimal import Decimal
import re
from math_expression import MathExpression

class AlgebraicExpression(MathExpression):
    """
    Represents an algebraic equation or inequality.

    This class parses a string to extract its coefficients, variables,
    sign (e.g., '=', '<='), and the independent term.
    """


    def __init__(self, expression: str) -> None:
        super().__init__(expression)
        self._parse_expression()
        self._generate_representation()

    def _generate_representation(self) -> None:
        self.representation = ""
        terms_str = []
        for variable, coefficient in self.terms.items():
            if coefficient == 1:
                terms_str.append(f"{variable}")
            elif coefficient == -1:
                terms_str.append(f"-{variable}")
            elif coefficient < 0:
                terms_str.append(f"-{-coefficient} * {variable}")
            else:
                terms_str.append(f"{coefficient} * {variable}")
        self.representation = " + ".join(terms_str)
        self.representation = self.representation.replace(" + -", " - ")
        self.representation += f" {self.sign} {self.independent_term}"

    def _parse_expression(self) -> None:
        """
        Parses a given equation or inequality as a string and finds
        its coefficients, variable names, sign, and independent term.

        Args:
            - expression (str): A string representing an equation or inequality.
                - The equation must be in the form: "ax1 + bx2 + ... + cxn = d" or "ax1 + bx2 + ... + cxn <= d",
                - where a, b, c, ... are coefficients and
                - d is the independent term.
                - The sign can be "=", "<=", ">=", "<" or ">".
        """
        # Split the equation into two parts: left and right side
        parts = re.split(r'([<>=]=?)', self.expression)
        left_side = parts[0]
        self.sign = parts[1]
        right_side = parts[2]

        # Get the coefficients and variable names from the left side
        for term in re.findall(r'([+-]?\s*\d*\.?\d*\s*\*?)\s*(\w+)', left_side):
            coefficient, variable = term
            coefficient: str = coefficient.replace(' ', '').replace('*', '')
            if coefficient not in ['', '+', '-']:
                self.terms[variable] += Decimal(coefficient)
            else:
                self.terms[variable] += Decimal((coefficient if coefficient else '+') + '1')
            if variable not in self.ordered_variables:
                self.ordered_variables.append(variable)

        # Check if right side has variables
        if re.search(r'[a-zA-Z]', right_side):
            # Right side has variables, so we need to parse it and move terms to the left
            self.independent_term = Decimal('0')
            
            # Handle expressions like "0.3 * (x1 + x2 + x3)"
            match = re.match(r'\s*([\d\.\s]*)\s*\*\s*\((.*)\)', right_side.strip())
            if match:
                multiplier_str, expression_in_parentheses = match.groups()
                multiplier = Decimal(multiplier_str.strip())

                for term in re.findall(r'([+-]?\s*\d*\.?\d*\s*\*?)\s*(\w+)', expression_in_parentheses):
                    coefficient, variable = term
                    coefficient: str = coefficient.replace(' ', '').replace('*', '')
                    
                    term_coefficient = Decimal('0')
                    if coefficient not in ['', '+', '-']:
                        term_coefficient = Decimal(coefficient)
                    else:
                        term_coefficient = Decimal((coefficient if coefficient else '+') + '1')

                    self.terms[variable] -= multiplier * term_coefficient
                    if variable not in self.ordered_variables:
                        self.ordered_variables.append(variable)
            else:
                # Handle simple expressions like "x1 + x2"
                for term in re.findall(r'([+-]?\s*\d*\.?\d*\s*\*?)\s*(\w+)', right_side):
                    coefficient, variable = term
                    coefficient: str = coefficient.replace(' ', '').replace('*', '')
                    
                    term_coefficient = Decimal('0')
                    if coefficient not in ['', '+', '-']:
                        term_coefficient = Decimal(coefficient)
                    else:
                        term_coefficient = Decimal((coefficient if coefficient else '+') + '1')

                    self.terms[variable] -= term_coefficient
                    if variable not in self.ordered_variables:
                        self.ordered_variables.append(variable)
        else:
            # Get the independent term from the right side
            self.independent_term = Decimal(right_side.strip())

    @staticmethod
    def is_an_algebraic_expression(expression: str) -> bool:
        """
        Determines if a given string represents a valid algebraic expression.

        Args:
            - expression(str): A string representing a possible algebraic expression.

        Returns:
            - bool: True if the string represents a valid algebraic expression,
            False otherwise.
        """
        pattern = r'^\s*[+-]?\s*\d*\s*\*?\s*\w+\s*([+-]\s*\d*\s*\*?\s*\w+\s*)*([<>=]=?)\s*[+-]?\d+\s*$'
        return bool(re.match(pattern, expression))

    def __repr__(self) -> str:
        return f"AlgebraicExpression({self.representation})"

    def __str__(self) -> str:
        return self.representation
# Simplex

## Practical use case

Suppose you have a company that produces two products, A and B. Each unit of product A that you produce generates a profit of $3 and each unit of product B generates a profit of $4. You want to maximize your total profits.

However, you have some production constraints. Each unit of product A requires 2 hours of labor and each unit of product B requires 3 hours of labor. You have a total of 100 hours of labor available. In addition, each unit of product A requires 1 kg of raw material and each unit of product B requires 2 kg of raw material. You have a total of 80 kg of raw material available.

This problem can be formulated as a linear programming problem with the following objective function and constraints:

```
Maximize: 3A + 4B
Subject to:
    2A + 3B <= 100
    A + 2B <= 80
    A >= 0
    B >= 0
```

Where `A` and `B` represent the number of units produced of products A and B, respectively.

To solve this problem using the Python program I provided earlier, you can enter the following values when prompted:

- Number of variables: `2`
- Objective function coefficients: `3` and `4`
- Maximize or minimize: `1` (maximize)
- Number of constraints: `2`
- Constraint 1:
    - Coefficients: `2` and `3`
    - Inequality: `<=`
    - Value of `b`: `100`
- Constraint 2:
    - Coefficients: `1` and `2`
    - Inequality: `<=`
    - Value of `b`: `80`

After entering these values, the program will solve the problem and show you the optimal solution. In this case, the optimal solution is to produce 20 units of product A and 30 units of product B to obtain a maximum profit of $180.

- Number of variables: `2`
- Objective function coefficients: `4` and `1`
- Maximize or minimize: `0` (minimize)
- Number of constraints: `3`
- Constraint 1:
    - Coefficients: `3` and `1`
    - Inequality: `=`
    - Value of `b`: `3`
- Constraint 2:
    - Coefficients: `4` and `3`
    - Inequality: `>=`
    - Value of `b`: `6`
- Constraint 3:
    - Coefficients: `1` and `2`
    - Inequality: `<=`
    - Value of `b`: `4`


Sure, here is the problem in the format you requested:

- Number of variables: `4`
- Objective function coefficients: `2`, `4`, `4` and `-3`
- Maximize or minimize: `1` (maximize)
- Number of constraints: `2`
- Constraint 1:
    - Coefficients: `1`, `1`, `1` and `0`
    - Inequality: `=`
    - Value of `b`: `4`
- Constraint 2:
    - Coefficients: `1`, `4`, `0` and `1`
    - Inequality: `=`
    - Value of `b`: `8`
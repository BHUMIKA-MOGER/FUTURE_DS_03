import math

def factorial_builtin(n):
    """Calculates factorial using the math module's built-in function."""
    if n < 0:
        return "Error: Factorial does not exist for negative numbers."
    return math.factorial(n)

# Example usage
number = 5
print(f"The factorial of {number} is: {factorial_builtin(number)}")
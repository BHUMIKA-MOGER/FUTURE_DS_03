# 1. Get input from the user (input returns strings)
# Using float() allows for decimal numbers
num1_str = input("Enter the first number: ")
num2_str = input("Enter the second number: ")

# 2. Convert to float and perform addition
# The float() function converts the text input into a number
sum_result = float(num1_str) + float(num2_str)

# 3. Display the result
print(f"The sum is: {sum_result}")
# Example Output:
# Enter the first number: 45
# Enter the second number: 12.5
# The sum is: 57.5
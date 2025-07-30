"""
Simple Calculator Package
A basic calculator with essential mathematical operations.
"""

import math

def add(a, b):
    """
    Add two numbers.
    
    Args:
        a (float): First number
        b (float): Second number
    
    Returns:
        float: Sum of a and b
    """
    return a + b

def subtract(a, b):
    """
    Subtract second number from first number.
    
    Args:
        a (float): First number
        b (float): Second number
    
    Returns:
        float: Difference of a and b
    """
    return a - b

def multiply(a, b):
    """
    Multiply two numbers.
    
    Args:
        a (float): First number
        b (float): Second number
    
    Returns:
        float: Product of a and b
    """
    return a * b

def divide(a, b):
    """
    Divide first number by second number.
    
    Args:
        a (float): Dividend
        b (float): Divisor
    
    Returns:
        float: Quotient of a divided by b
    
    Raises:
        ValueError: If divisor is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(base, exponent):
    """
    Calculate base raised to the power of exponent.
    
    Args:
        base (float): Base number
        exponent (float): Exponent
    
    Returns:
        float: base^exponent
    """
    return base ** exponent

def root(number, n=2):
    """
    Calculate the nth root of a number.
    
    Args:
        number (float): Number to find root of
        n (float): Root degree (default is 2 for square root)
    
    Returns:
        float: nth root of the number
    
    Raises:
        ValueError: If trying to find even root of negative number
    """
    if n % 2 == 0 and number < 0:
        raise ValueError("Cannot find even root of negative number")
    
    if number < 0:
        return -(abs(number) ** (1/n))
    return number ** (1/n)

def square_root(number):
    """
    Calculate square root of a number.
    
    Args:
        number (float): Number to find square root of
    
    Returns:
        float: Square root of the number
    
    Raises:
        ValueError: If number is negative
    """
    if number < 0:
        raise ValueError("Cannot find square root of negative number")
    return math.sqrt(number)

def cube_root(number):
    """
    Calculate cube root of a number.
    
    Args:
        number (float): Number to find cube root of
    
    Returns:
        float: Cube root of the number
    """
    return root(number, 3)

def percentage(part, whole):
    """
    Calculate percentage.
    
    Args:
        part (float): Part value
        whole (float): Whole value
    
    Returns:
        float: Percentage value
    
    Raises:
        ValueError: If whole is zero
    """
    if whole == 0:
        raise ValueError("Cannot calculate percentage with zero as whole")
    return (part / whole) * 100

def factorial(n):
    """
    Calculate factorial of a number.
    
    Args:
        n (int): Non-negative integer
    
    Returns:
        int: Factorial of n
    
    Raises:
        ValueError: If n is negative or not an integer
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("Factorial requires non-negative integer")
    return math.factorial(n)

def absolute(number):
    """
    Get absolute value of a number.
    
    Args:
        number (float): Input number
    
    Returns:
        float: Absolute value
    """
    return abs(number)

def modulo(a, b):
    """
    Calculate modulo (remainder) of division.
    
    Args:
        a (float): Dividend
        b (float): Divisor
    
    Returns:
        float: Remainder of a divided by b
    
    Raises:
        ValueError: If divisor is zero
    """
    if b == 0:
        raise ValueError("Cannot perform modulo with zero divisor")
    return a % b

def main():
    """
    Interactive calculator main function.
    Provides a command-line interface for the calculator.
    """
    
    while True:
        try:
            choice = input("\nEnter your choice (0-12): ").strip()
            
            if choice == '0':
                print("Thank you for using Calculator!")
                break
            elif choice == '1':
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))
                result = add(a, b)
                print(f"Result: {a} + {b} = {result}")
                
            elif choice == '2':
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))
                result = subtract(a, b)
                print(f"Result: {a} - {b} = {result}")
                
            elif choice == '3':
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))
                result = multiply(a, b)
                print(f"Result: {a} × {b} = {result}")
                
            elif choice == '4':
                a = float(input("Enter dividend: "))
                b = float(input("Enter divisor: "))
                result = divide(a, b)
                print(f"Result: {a} ÷ {b} = {result}")
                
            elif choice == '5':
                base = float(input("Enter base: "))
                exp = float(input("Enter exponent: "))
                result = power(base, exp)
                print(f"Result: {base}^{exp} = {result}")
                
            elif choice == '6':
                num = float(input("Enter number: "))
                result = square_root(num)
                print(f"Result: √{num} = {result}")
                
            elif choice == '7':
                num = float(input("Enter number: "))
                result = cube_root(num)
                print(f"Result: ∛{num} = {result}")
                
            elif choice == '8':
                num = float(input("Enter number: "))
                n = float(input("Enter root degree: "))
                result = root(num, n)
                print(f"Result: {num}^(1/{n}) = {result}")
                
            elif choice == '9':
                part = float(input("Enter part value: "))
                whole = float(input("Enter whole value: "))
                result = percentage(part, whole)
                print(f"Result: {part} is {result}% of {whole}")
                
            elif choice == '10':
                num = int(input("Enter non-negative integer: "))
                result = factorial(num)
                print(f"Result: {num}! = {result}")
                
            elif choice == '11':
                num = float(input("Enter number: "))
                result = absolute(num)
                print(f"Result: |{num}| = {result}")
                
            elif choice == '12':
                a = float(input("Enter dividend: "))
                b = float(input("Enter divisor: "))
                result = modulo(a, b)
                print(f"Result: {a} mod {b} = {result}")
                
            else:
                print("Invalid choice! Please enter a number between 0-12.")
                
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        # Ask if user wants to continue
        if choice != '0':
            continue_calc = input("\nDo you want to perform another calculation? (y/n): ").lower()
            if continue_calc not in ['y', 'yes']:
                print("Thank you for using Calculator!")
                break


# Entry point for the package
if __name__ == "__main__":
    main()

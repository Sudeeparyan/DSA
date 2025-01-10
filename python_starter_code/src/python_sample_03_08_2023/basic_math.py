"""
Basic mathematical operations.

This module provides useful functions for performing math operations.

Functions:
    - add(arg1, arg2): Perform addition of two numbers.
    - sub(arg1, arg2): Perform subtraction of two numbers.
    - multiply(arg1, arg2): Perform multiplication of two numbers.
    - divide(arg1, arg2): Perform division of two numbers.
    - squareroot(arg): Perform square root of the given number.
"""

from math import sqrt


def add(num1: float, num2: float) -> float:
    """Perform addition of two numbers.

    Parameters:
    num1 (float): The first number.
    num2 (float): The second number.

    Returns:
    float: The sum of the two input numbers.
    """
    return num1+num2


def sub(num1: float, num2: float) -> float:
    """Perform subtraction of two numbers.

    Parameters:
    num1 (float): The first number.
    num2 (float): The second number.

    Returns:
    float: The subtraction of the two input numbers.
    """
    return num1-num2


def multiply(num1: float, num2: float) -> float:
    """Perform multiplication of two numbers.

    Parameters:
    num1 (float): The first number.
    num2 (float): The second number.

    Returns:
    float: The product of the two input numbers.
    """
    return num1*num2


def divide(num1: float, num2: float) -> float:
    """Perform division of two numbers.

    Parameters:
    num1 (float): The first number.
    num2 (float): The second number.

    Returns:
    float: The division of the two input numbers.
    """
    return num1/num2


def square_root(num1: float) -> float:
    """Perform square root of the given number.

    Parameters:
    num1 (float): The first number.

    Returns:
    float: The square root of the input number.
    """
    return sqrt(num1)

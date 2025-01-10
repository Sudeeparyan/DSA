"""Test Functions"""
import pytest
from python_sample_03_08_2023.basic_math import add, \
    sub, multiply, divide


def test_addition(number_1, number_2):
    """Tests addition operation

    Args:
        number_1 (float): number
        number_2 (float): number
    """
    assert add(number_1, number_2) == number_1 + number_2


def test_subtraction(number_1, number_2):
    """Tests subtraction operation

    Args:
        number_1 (float): number
        number_2 (float): number
    """
    assert sub(number_1, number_2) == number_1 - number_2


@pytest.mark.multiply
def test_multiplication_with_positive_values():
    """Tests multiplication operation

    Args:
        number_1 (float): number
        number_2 (float): number
    """
    assert multiply(5, 5) == 5*5


@pytest.mark.multiply
def test_multiplication_with_negative_values():
    """Tests multiplication operation with negative values"""
    assert multiply(-5, 5) == -5 * 5


@pytest.mark.multiply
def test_multiplication_with_zero():
    """Tests multiplication operation against zero"""
    assert multiply(0, 5) == 0


@pytest.mark.parametrize("dividend, divisor, quotient", [(10, 2, 5), (15, -3, -5),
                                                         (-22, 11, -2), (-25, -5, 5)])
def test_division(divisor, dividend, quotient):
    """Tests division operation

    Args:
        divisor (float): divisor
        dividend (float): dividend
        quotient (float): expected quotient
    """
    assert divide(dividend, divisor) == quotient


@pytest.mark.zerodivision
def test_zero_division():
    """Tests division operation by zero"""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

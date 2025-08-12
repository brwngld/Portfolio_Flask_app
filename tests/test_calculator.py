import pytest

def calculate(first_number, second_number, operation):
    if operation == "add":
        return first_number + second_number
    elif operation == "subtract":
        return first_number - second_number
    elif operation == "multiply":
        return first_number * second_number
    elif operation == "divide":
        if second_number == 0:
            raise ZeroDivisionError("Division by zero")
        return first_number / second_number
    elif operation == "power":
        return first_number ** second_number
    elif operation == "modulus":
        if second_number == 0:
            raise ZeroDivisionError("Modulus by zero")
        return first_number % second_number
    elif operation == "sqrt":
        if first_number < 0:
            raise ValueError("Square root of negative number")
        return first_number ** 0.5
    else:
        raise ValueError("Unknown operation")

def test_add():
    assert calculate(2, 3, "add") == 5

def test_subtract():
    assert calculate(5, 2, "subtract") == 3

def test_multiply():
    assert calculate(4, 3, "multiply") == 12

def test_divide():
    assert calculate(10, 2, "divide") == 5

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate(10, 0, "divide")

def test_power():
    assert calculate(2, 3, "power") == 8

def test_modulus():
    assert calculate(10, 3, "modulus") == 1

def test_modulus_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate(10, 0, "modulus")

def test_sqrt():
    assert calculate(9, None, "sqrt") == 3

def test_sqrt_negative():
    with pytest.raises(ValueError):
        calculate(-4, None, "sqrt")

def test_unknown_operation():
    with pytest.raises(ValueError):
        calculate(1, 2, "unknown")
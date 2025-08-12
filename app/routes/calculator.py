from datetime import datetime

from flask import Blueprint, render_template, request

calculator_bp = Blueprint("calculator", __name__)


@calculator_bp.route("/", methods=["GET"])
def calculator():
    error = None
    result = None
    first_number = request.args.get("first_number", type=float)
    second_number = request.args.get("second_number", type=float)
    operation = request.args.get("operation", default="add")

    if request.args:
        # For sqrt, only first_number is required
        if operation == "sqrt":
            if first_number is None:
                error = "Please enter a number for square root."
            elif first_number < 0:
                error = "Error: Cannot take square root of a negative number."
            else:
                result = first_number**0.5
        else:
            if first_number is None or second_number is None:
                error = "Please enter both numbers."
            else:
                try:
                    if operation == "add":
                        result = first_number + second_number
                    elif operation == "subtract":
                        result = first_number - second_number
                    elif operation == "multiply":
                        result = first_number * second_number
                    elif operation == "divide":
                        if second_number == 0:
                            error = "Error: Division by zero is not allowed."
                        else:
                            result = first_number / second_number
                    elif operation == "power":
                        result = first_number**second_number
                    elif operation == "modulus":
                        if second_number == 0:
                            error = "Error: Modulus by zero is not allowed."
                        else:
                            result = first_number % second_number
                except Exception as e:
                    error = f"Invalid input: {e}"

    current_year = datetime.now().year
    return render_template(
        "calculator.html",
        first_number=first_number if first_number is not None else "",
        second_number=second_number if second_number is not None else "",
        operation=operation,
        result=result,
        error=error,
        current_year=current_year,
    )

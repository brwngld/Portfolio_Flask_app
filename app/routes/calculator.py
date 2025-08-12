from datetime import datetime

from flask import Blueprint, render_template

calculator_bp = Blueprint("calculator", __name__)


@calculator_bp.route("/")
def calculator():
    current_year = datetime.now().year
    return render_template("calculator.html", current_year=current_year)

import random
from datetime import datetime

from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)

# Main guess game blueprint
guess_bp = Blueprint("guess", __name__)


@guess_bp.route("/guess/", methods=["GET", "POST"])
def guess_game():
    # Difficulty settings
    difficulties = {
        "easy": {"max": 10, "tries": None},
        "medium": {"max": 50, "tries": 3},
        "hard": {"max": 100, "tries": 3},
    }

    # Get selected difficulty
    difficulty = request.form.get("difficulty", session.get("difficulty", "easy"))
    max_number = difficulties[difficulty]["max"]
    max_tries = difficulties[difficulty]["tries"]

    # Initialize game state in session
    if (
        "target" not in session
        or request.method == "POST"
        and request.form.get("difficulty") != session.get("difficulty")
    ):
        session["target"] = random.randint(0, max_number)
        session["difficulty"] = difficulty
        session["tries_left"] = max_tries if max_tries else None

    message = None
    hint = None
    tries_left = session.get("tries_left")

    if request.method == "POST":
        guess = request.form.get("guess", type=int)
        target = session["target"]

        if guess is None:
            message = "Please enter a valid number."
        elif guess == target:
            message = f"🎉 Correct! The number was {target}. Starting a new game."
            session.pop("target", None)
            session.pop("tries_left", None)
        else:
            if guess < target:
                hint = "Try a higher number."
            else:
                hint = "Try a lower number."
            if max_tries:
                session["tries_left"] = tries_left - 1 if tries_left else max_tries - 1
                tries_left = session["tries_left"]
                if tries_left <= 0:
                    message = f"❌ Out of tries! The number was {target}. Starting a new game."
                    session.pop("target", None)
                    session.pop("tries_left", None)
            else:
                message = "Wrong guess! Try again."

    current_year = datetime.now().year
    return render_template(
        "guess_game.html",
        difficulty=difficulty,
        max_number=max_number,
        message=message,
        hint=hint,
        tries_left=tries_left,
        form=request.form,
        current_year=current_year,
    )

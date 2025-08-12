from datetime import datetime

from flask import Blueprint, render_template, request

guess = Blueprint("guess", __name__)


@guess.route("/")
def guess_home():
    current_year = datetime.now().year
    return render_template("guess_game.html", current_year=current_year)


@guess.route("/play", methods=["POST"])
def play():
    # your game logic here
    current_year = datetime.now().year

    # Return a template or redirect after processing
    return render_template("guess_result.html", current_year=current_year)

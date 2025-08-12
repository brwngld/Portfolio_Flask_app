import json
import os
import traceback
from datetime import datetime

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, url_for)
from flask_login import current_user
from flask_mail import Message

from app import limiter
from app.forms import ContactForm

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def index():
    current_year = datetime.now().year
    json_path = os.path.join(current_app.root_path, "static", "projects.json")
    with open(json_path) as f:
        projects = json.load(f)

    # If link_url missing or None, set it to '#' so button is clickable (or replace with any valid URL)
    for project in projects:
        project["image_url"] = url_for("static", filename=project["image"])
        if not project.get("endpoint"):
            project["link_url"] = "#"
        else:
            project["link_url"] = url_for(project["endpoint"])

    return render_template("index.html", projects=projects, current_year=current_year)


@main.route("/about")
def about():
    current_year = datetime.now().year
    return render_template("about.html", current_year=current_year)


@main.route("/projects")
def projects():
    current_year = datetime.now().year
    json_path = os.path.join(current_app.root_path, "static", "projects.json")
    with open(json_path) as f:
        projects = json.load(f)

    # Get search query from request args
    from flask import request

    query = request.args.get("q", "").strip().lower()
    if query:
        projects = [
            p
            for p in projects
            if query in p["name"].lower() or query in p["description"].lower()
        ]

    for project in projects:
        project["image_url"] = url_for("static", filename=project["image"])
        if not project.get("endpoint"):
            project["link_url"] = "#"
        else:
            project["link_url"] = url_for(project["endpoint"])

    return render_template(
        "projects.html",
        projects=projects,
        current_year=current_year,
        search_query=query,
    )


@main.route("/contact", methods=["GET", "POST"])
@limiter.limit("5 per hour")
def contact():
    current_year = datetime.now().year

    # Grab env vars for contact info
    contact_email = os.environ.get("CONTACT_EMAIL", "your@email.com")
    contact_phone = os.environ.get("CONTACT_PHONE", "+123 456 7890")
    contact_location = os.environ.get("CONTACT_LOCATION", "Your City, Country")

    form = ContactForm()
    if form.validate_on_submit():
        name = (form.name.data or "").strip()
        email = (form.email.data or "").strip()
        message = (form.message.data or "").strip()
        try:
            mail = current_app.extensions.get("mail")
            if mail is None:
                flash("Email service not configured.", "danger")
            else:
                msg = Message(
                    subject=f"New Contact Message from {name}",
                    sender=contact_email,
                    recipients=[contact_email],
                    body=f"Name: {name}\nEmail: {email}\nMessage:\n{message}",
                    reply_to=email,
                )
                mail.send(msg)
                flash("Your message has been sent successfully!", "success")
                return redirect(request.url)
        except Exception as e:
            print("Email send error:", e)
            traceback.print_exc()
            flash(
                "There was an error sending your message. Please try again later.",
                "danger",
            )

    return render_template(
        "contact.html",
        current_year=current_year,
        contact_email=contact_email,
        contact_phone=contact_phone,
        contact_location=contact_location,
        form=form,
    )

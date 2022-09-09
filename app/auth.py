from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session
import os
from dotenv import load_dotenv

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates/auth')

@auth_bp.route("/login",methods=["GET"])
def login():
    if session.get("isAdmin"):
        return redirect(url_for("admin_bp.dash"))
    return render_template("login_page.html")

@auth_bp.route("/verify",methods=["POST"])
def verify():
    if session.get("isAdmin"):
        return redirect(url_for("admin_bp.dash"))
    user = request.form.get("user")
    password = request.form.get("pwd")
    load_dotenv()
    if user == os.getenv("ADMIN_USERNAME") and password == os.getenv("ADMIN_PASSWORD"):
        session["isAdmin"] = 1
        flash("Successfully logged in!")
        return redirect(url_for("general_bp.welcome"))
    else:
        flash("Invalid login, try again")
        return redirect(url_for("auth_bp.login"))

@auth_bp.route("/logout",methods=["GET"])
def logout():
    if session.get("isAdmin"):
        session.pop("isAdmin")
        flash("Logged out successfully!")
    return redirect(url_for("general_bp.welcome"))
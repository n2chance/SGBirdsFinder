from flask import Blueprint, render_template

general_bp = Blueprint('general_bp', __name__, template_folder='templates/general')

@general_bp.route("/",methods=["GET"])
def welcome():
    return render_template("index.html")

@general_bp.route("/about",methods=["GET"])
def about():
    return render_template("about.html")

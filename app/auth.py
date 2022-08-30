from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates/auth')

DATABASE = 'Birds.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

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
    '''
    cur = get_db().cursor()
    cur.execute("SELECT AdminID FROM Admin WHERE Username=? AND Password=?",(user, password))
    adminID = cur.fetchone()
    '''
    if user == "aaa" and password == "bbbc":
        adminID = True
    else:
        adminID = False
        
    if adminID:
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

@auth_bp.teardown_request
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

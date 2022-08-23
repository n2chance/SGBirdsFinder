from flask import Blueprint, render_template, request, redirect, url_for, flash, g

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates/auth')

DATABASE = 'Birds.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@auth_bp.route("/login",methods=["GET"])
def login():
    return render_template("login_page.html")

@auth_bp.route("/verify",methods=["POST"])
def verify():
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
        flash("Successfully logged in!")
        return redirect(url_for("general_bp.welcome"))
    else:
        flash("Invalid login, try again")
        return redirect(url_for("auth_bp.login"))

@auth_bp.teardown_request
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

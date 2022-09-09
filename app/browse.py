from flask import Blueprint, render_template, g, request
import sqlite3

browse_bp = Blueprint('browse_bp', __name__, template_folder='templates/browse')

DATABASE = 'app/Birds.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@browse_bp.route("")
def browse():
    cur = get_db().cursor()
    if request.args.get("query"): # If search query is given
        q = "%" + request.args.get("query") + "%"
        cur.execute("SELECT Num, EngName, SciName, Family FROM Birds WHERE EngName LIKE ? OR SciName LIKE ? OR Family LIKE ?",(q,q,q))
    else:
        cur.execute("SELECT Num, EngName, SciName, Family FROM Birds")
    
    allbirds = cur.fetchall()
    return render_template("browse_birds.html", allbirds=allbirds)


@browse_bp.teardown_request
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

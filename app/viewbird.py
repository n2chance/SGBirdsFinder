from flask import Blueprint, render_template, g
import sqlite3

viewbird_bp = Blueprint('viewbird_bp', __name__, template_folder='templates/viewbird')

DATABASE = 'Birds.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@viewbird_bp.route("/<int:birdNum>",methods=["GET"])
def viewbird(birdNum):
    cur = get_db().cursor()
    cur.execute("SELECT count(num) from Birds")
    if birdNum >= 1 and birdNum <= int(cur.fetchone()[0]):
        cur.execute("SELECT * from Birds WHERE num = ?",(birdNum,))
        birdInfo = list(cur.fetchone()[:-3])
        if birdInfo[12] and birdInfo[12] % 1 == 0:
            birdInfo[12] = int(birdInfo[12])
        if birdInfo[13] and birdInfo[13] % 1 == 0:
            birdInfo[13] = int(birdInfo[13])
        localStat = {"I":"Introduced","M":"Migrant","R":"Resident","Va":"Vagrant","Vi":"Visitor","E":"Extirpated"}
        return render_template("bird_info.html",birdInfo=birdInfo,localStat=localStat)
    else:
        return render_template("bird_not_found.html"), 404

@viewbird_bp.teardown_request
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

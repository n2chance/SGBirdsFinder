from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session
import sqlite3

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates/admin')

DATABASE = 'Birds.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

class Question():
    def __init__(self, name, askQn, numSelect, options):
        self.name = name
        self.askQn = askQn
        self.options = options
        self.numSelect = numSelect

q1 = Question("place", "Where did you see the bird?", 1, \
    {"resd":"Residential/Urban Area",
    "pnr":"Park/Nature Reserve",
    "fst":"Forest",
    "wet":"Wetland/Lake/River",
    "oc":"Ocean",
    "sea":"Sea Coast",
    "open":"Clearing/Grassland"})
q3 = Question("colour", "What were the main colours of the bird?", 3, \
    {"Black":"Black",
    "Grey":"Grey",
    "Brown":"Brown",
    "White":"White",
    "Red":"Red",
    "Orange":"Orange",
    "Yellow":"Yellow",
    "Green":"Green",
    "Blue":"Blue"})
q4 = Question("action", "What was the bird doing when you found it?", 1, \
    {"feed":"Feeding on the ground", 
    "swim":"Swimming or wading",
    "ground":"On the ground",
    "trees":"In trees or bushes",
    "branch":"On a branch or structure",
    "fly":"Soaring or flying",
    "fish":"Fishing"
    })

@admin_bp.route("")
def dash():
    if session.get("isAdmin"):
        return render_template("dashboard.html")
    
    else:
        flash("Login required")
        return redirect(url_for("auth_bp.login")) 

@admin_bp.route("/new",methods=["GET","POST"])
def new():
    if session.get("isAdmin"):
        if request.method == "GET":
            qns = [q1,q3,q4]
            localStat = {"I":"Introduced","M":"Migrant","R":"Resident","Va":"Vagrant","Vi":"Visitor","E":"Extirpated"}
            return render_template("new_bird.html",qns=qns,localStat=localStat)
        
        elif request.method == "POST":
            pass
    
    else:
        flash("Login required")
        return redirect(url_for("auth_bp.login"))

@admin_bp.route("/update",methods=["GET","POST"])
def update():
    if session.get("isAdmin"):
        cur = get_db().cursor()
        if request.method == "GET":
            birdNum = request.args.get("num")
            cur.execute("SELECT count(num) from Birds")
            if not birdNum or (not birdNum.isnumeric() or int(birdNum) < 1 or int(birdNum) > int(cur.fetchone()[0])):
                flash("Invalid/missing bird number")
                return redirect(url_for("browse_bp.browse"))
            else:
                cur.execute("SELECT * FROM Birds WHERE Num=?",birdNum)
                birdInfo = cur.fetchone()
                qns = [q1,q3,q4]
                localStat = {"I":"Introduced","M":"Migrant","R":"Resident","Va":"Vagrant","Vi":"Visitor","E":"Extirpated"}
                return render_template("update_bird.html",birdInfo=birdInfo,qns=qns,localStat=localStat)
        
        elif request.method == "POST":
            birdNum = request.form.get("birdNum")
            return birdNum
    
    else:
        flash("Login required")
        return redirect(url_for("auth_bp.login")) 

@admin_bp.route("/delete",methods=["GET","POST"])
def delete():
    if session.get("isAdmin"):
        cur = get_db().cursor()
        if request.method == "GET":
            birdNum = request.args.get("num")
            cur.execute("SELECT count(num) from Birds")
            if not birdNum or (not birdNum.isnumeric() or int(birdNum) < 1 or int(birdNum) > int(cur.fetchone()[0])):
                flash("Invalid/missing bird number")
                return redirect(url_for("browse_bp.browse"))
            else:
                cur.execute("SELECT Num, EngName, SciName, Family FROM Birds WHERE Num=?",birdNum)
                birdInfo = cur.fetchone()
                return render_template("delete_bird.html",birdInfo=birdInfo)
        
        elif request.method == "POST":
            flash("Bird deleted successfully")
            return redirect(url_for())
    
    else:
        flash("Login required")
        return redirect(url_for("auth_bp.login"))

@admin_bp.teardown_request
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
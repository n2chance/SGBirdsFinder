from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session
import sqlite3

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates/admin')

DATABASE = 'app/Birds.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

class Question():
    def __init__(self, name, askQn, numSelect, options):
        self.name = name
        self.askQn = askQn
        self.options = options
        self.numSelect = numSelect

# Might move this to a json file
q1 = Question("place", "Where did you see the bird?", 1, \
    {"resd":"Residential/Urban Area",
    "pnr":"Park/Nature Reserve",
    "fst":"Forest",
    "wet":"Wetland/Lake/River",
    "oc":"Ocean",
    "sea":"Sea Coast",
    "open":"Clearing/Grassland"})
q3 = Question("colour", "What were the main colours of the bird?", 3, \
    {"black":"Black",
    "grey":"Grey",
    "brown":"Brown",
    "white":"White",
    "red":"Red",
    "orange":"Orange",
    "yellow":"Yellow",
    "green":"Green",
    "blue":"Blue"})
q4 = Question("action", "What was the bird doing when you found it?", 1, \
    {"feed":"Feeding on the ground", 
    "swim":"Swimming or wading",
    "ground":"On the ground",
    "trees":"In trees or bushes",
    "branch":"On a branch or structure",
    "fly":"Soaring or flying",
    "fish":"Fishing"
    })

# Validate responses
def checkAndParse(responses, columns, tableInfo):
    colInfoDict = {}
    for i in tableInfo:
        colInfoDict[i["name"]] = i["notnull"]
    localStat = {"I":"Introduced","M":"Migrant","R":"Resident","Va":"Vagrant","Vi":"Visitor","E":"Extirpated"}
    params = []
    for col in columns:
        val = responses.get(col) 

        if col == "LocalStatus":
            stats = ""
            for i in range(1,len(localStat)+1):
                stat = responses.get(f"status{i}")
                if stat in localStat:
                    stats += stat + "/"
                elif stat is not None:
                    return False, "Invalid local status"
            params.append(stats[:-1])
        
        # Check if column has NOT NULL constraint in db and the associated response is empty
        elif (val is None or val == "") and colInfoDict[col] == 1:
            return False, "Please enter compulsory fields"
        
        elif col == "RarityStatus":
            if val in ["0","1"]:
                if val == 0:
                    params.append("Non-rarity")
                else:
                    params.append("Rarity")
            else:
                return False, "Invalid rarity status"
        
        elif col == "MinSize":
            if val == "":
                params.append(None)
            else:
                try:
                    assert float(val) and float(val) > 0 and float(val) >= float(responses.get("MinSize"))
                except:
                    return False, "Invalid minimum size"
                else:
                    params.append(float(val))
        
        elif col == "MaxSize":
            if val == "":
                params.append(None)
            else:
                try:
                    assert float(val) and float(val) > 0 and float(val) >= float(responses.get("MinSize"))
                except:
                    return False,"Invalid minimum size"
                else:
                    params.append(float(val))
        elif col in ("Place","Colour","Action"):
            temp = []
            lenOpts = {"Place":len(q1.options),"Colour":len(q3.options),"Action":len(q4.options)}
            for i in range(1,lenOpts[col]+1):
                val = responses.get(f"{col.lower()}{i}")
                if val:
                    temp.append(val)
            params.append("/".join(temp))
        else:
            if val == "" or val == None:
                params.append(None)
            else:
                params.append(val)
    return True, params

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
            con = get_db()
            cur = con.cursor()
            cur.execute("SELECT * FROM Birds")
            cols = cur.fetchone().keys()
            cols.remove("Num")
            cols = tuple(cols)
            cur.execute("PRAGMA table_info(Birds)")
            tableInfo = cur.fetchall()

            print(request.form)
            check = checkAndParse(request.form, cols, tableInfo)
            if check[0]:
                params = tuple(check[1])
                sqlStatement = f"INSERT INTO Birds {cols} VALUES (" + "?, "*len(params)
                sqlStatement = sqlStatement[:-2] + ")"
                try:
                    cur.execute(sqlStatement,params)
                    con.commit()
                    flash(f"Bird \'{request.form.get('EngName')}\' added successfully!")
                    
                except:
                    flash("Error adding bird to database")
                return redirect(url_for("admin_bp.new"))
            else:
                flash(check[1])
                return redirect(url_for("admin_bp.new"))

    else:
        flash("Login required")
        return redirect(url_for("auth_bp.login"))

@admin_bp.route("/update",methods=["GET","POST"])
def update():
    if session.get("isAdmin"):
        con = get_db()
        cur = con.cursor()
        if request.method == "GET":
            birdNum = request.args.get("num")
            cur.execute("SELECT * FROM Birds WHERE Num = ?",(birdNum,))
            birdInfo = cur.fetchone()
            if birdInfo:
                qns = [q1,q3,q4]
                localStat = {"I":"Introduced","M":"Migrant","R":"Resident","Va":"Vagrant","Vi":"Visitor","E":"Extirpated"}
                opts = []
                for i in (birdInfo['Place'],birdInfo['Colour'],birdInfo['Action']):
                    if type(i) == str:
                        opts.append(i.split("/"))
                    else:
                        opts.append([])
                return render_template("update_bird.html",birdInfo=birdInfo,qns=qns,localStat=localStat,opts=opts)
            else:
                flash("Invalid/missing bird number")
                return redirect(url_for("browse_bp.browse"))
        
        elif request.method == "POST":
            cur.execute("SELECT * FROM Birds")
            cols = cur.fetchone().keys()
            cols.remove("Num")
            cols = tuple(cols)
            cur.execute("PRAGMA table_info(Birds)")
            tableInfo = cur.fetchall()
            
            check = checkAndParse(request.form, cols, tableInfo)
            if check[0]:
                params = check[1]
                sqlStatement = "UPDATE Birds SET "
                for col in cols:
                    sqlStatement += f"{col} = ?, "
                sqlStatement = sqlStatement[:-2] + " WHERE Num = ?"
                params.append(request.form.get("birdNum"))
                try:
                    cur.execute(sqlStatement,tuple(params))
                    con.commit()
                    flash(f"Bird \'{request.form.get('EngName')}\' updated successfully!")
                except:
                    flash("Error adding bird to database")
                finally:
                    return redirect(url_for("browse_bp.browse"))
            else:
                flash(check[1])
                return redirect(url_for("browse_bp.browse"))
    
    else:
        flash("Login required")
        return redirect(url_for("auth_bp.login")) 

@admin_bp.route("/delete",methods=["GET","POST"])
def delete():
    if session.get("isAdmin"):
        con = get_db()
        cur = con.cursor()
        if request.method == "GET":
            birdNum = request.args.get("num")
            cur.execute("SELECT Num, EngName, SciName, Family FROM Birds WHERE Num = ?",(birdNum,))
            birdInfo = cur.fetchone()
            if birdInfo:
                return render_template("delete_bird.html",birdInfo=birdInfo)
            else:
                flash("Invalid/missing bird number")
                return redirect(url_for("browse_bp.browse"))
        
        elif request.method == "POST":
            birdNum = request.form.get("birdNum")
            try:
                cur.execute("SELECT EngName FROM Birds WHERE Num=?",(birdNum,))
                name = cur.fetchone()['EngName']
                cur.execute("DELETE FROM Birds WHERE Num=?",(birdNum,))
                
                con.commit()
                flash(f"Bird \'{name}\' deleted successfully!")
            except:
                flash("Error deleting bird from database")
            finally:
                return redirect(url_for("browse_bp.browse"))
    
    else:
        flash("Login required")
        return redirect(url_for("auth_bp.login"))

@admin_bp.teardown_request
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
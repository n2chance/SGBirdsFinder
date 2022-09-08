from flask import Blueprint, render_template, request, redirect, url_for, g, session, flash
import sqlite3

id_bp = Blueprint('id_bp', __name__, template_folder='templates/identify')

DATABASE = 'Birds.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Function to find bird in db
def findBird(criteria,connection):
    SQLSTATEMENTP1 = "SELECT Num FROM Birds WHERE "
    sqlStatementP2 = ""
    params = []
    for criterion in criteria:
        colName = eval(f"q{criterion[0]}.name").capitalize()
        criterionVal = criterion[1]
        if colName == "Size":
            sizeMap = {"l15":[0,15],"15t25":[15,20],"25t30":[25,30],"30t40":[30,40],"40t45":[40,45],"m45":[45,float("inf")]}
            sqlStatementP2 += "((MinSize <= ? AND MaxSize >= ?) OR (MinSize <= ? AND MaxSize >= ?)) AND "
            lowR, highR = sizeMap.get(criterionVal)[0], sizeMap.get(criterionVal)[1]
            params += [highR,lowR,lowR,highR]
        elif type(criterionVal) == list:
            for critNested in criterionVal:
                sqlStatementP2 += f"{colName} LIKE ? AND "
                params.append(f"%{critNested}%")
        else:
            sqlStatementP2 += f"{colName} LIKE ? AND "
            params.append(f"%{criterionVal}%")
    
    sqlStatementP2 = sqlStatementP2[:-5]
    cur = connection.cursor()
    cur.execute(SQLSTATEMENTP1+sqlStatementP2,params)
    toRet = []
    for tupNum in cur.fetchall():
        toRet.append(tupNum[0])
    return toRet
    
class Question():
    def __init__(self, name, askQn, numSelect, options):
        self.name = name
        self.askQn = askQn
        self.numSelect = numSelect
        self.options = options

# Might move this to a json file
q1 = Question("place", "Where did you see the bird?", 1, \
    {"resd":"Residential/Urban Area",
    "pnr":"Park/Nature Reserve",
    "fst":"Forest",
    "wet":"Wetland/Lake/River",
    "oc":"Ocean",
    "sea":"Sea Coast",
    "open":"Clearing/Grassland"})
q2 = Question("size", "How large is the bird? (length)", 1, \
    {"l15":"Sparrow-sized or smaller (less than 15cm)",
    "15t25":"Between sparrow and myna (15 - 25cm)",
    "25t30":"Myna-sized (25 - 30cm)",
    "30t40":"Between myna and crow (30 - 40cm)",
    "40t45":"Crow-sized (40 - 45cm)",
    "m45":"Larger than crow (more than 45cm)"
    })
q3 = Question("colour", "What were the main colours of the bird? (max 3)", 3, \
    {"black":"Black",
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

@id_bp.get("")
def identify_get():
    qns = [q1,q2,q3,q4]
    return render_template("identify_bird.html", qns=qns)

@id_bp.post("")
def identify_post():
    # Get inputs from form
    place = [1,request.form.get("place")]
    size = [2,request.form.get("size")]
    colours = [3,[]]
    for colCount in range(1,len(q3.options)+1):
        currColour = request.form.get(f"colour{colCount}")
        if currColour:
            colours[1].append(currColour)
    action = [4,request.form.get("action")]
    
    # Validating inputs
    criteria = []
    count = 1
    for crit in (place,size,colours,action):
        if crit[1] is not None and len(crit[1]) >= 1:
            qn = eval(f"q{count}")
            if type(crit[1]) == list and len(crit[1])> qn.numSelect:
                flash(f"Choose a maximum of {qn.numSelect} options for {qn.name}")
                return redirect(url_for("id_bp.identify_get"))
            elif crit[0] == 3:
                validColours = []
                for colour in crit[1]:
                    if colour in q3.options:
                        validColours.append(colour)
                criteria.append([3,validColours])
            else:
                if crit[1] in qn.options:
                    criteria.append(crit)
        count += 1

    if len(criteria) < 2:
        flash("Fill in at least 2 criteria")
        return redirect(url_for("id_bp.identify_get"))
    
    # Find bird, then find with 1 less criteria if no birds are found
    possBirds = findBird(criteria,get_db())
    if len(possBirds) == 0:
        for toPop in range(0,len(criteria)):
            criteriaNew = criteria[:]
            criteriaNew.pop(toPop)
            possBirdsNew = findBird(criteriaNew)
            if possBirdsNew:
                possBirds += possBirdsNew

    session["possBirds"] = possBirds
    return redirect(url_for("id_bp.possible_birds"))

@id_bp.route("/possible-birds",methods=["GET"])
def possible_birds():
    if session.get("possBirds") is not None:
        if len(session["possBirds"]) == 0:
            return render_template("no_birds.html")

        elif len(session["possBirds"]) >= 1:
            birdCount = len(session["possBirds"])
            cur = get_db().cursor()
            localStat = ""
            possBirds = []
            if birdCount == 1:
                cur.execute("SELECT * FROM Birds WHERE Num=?", session["possBirds"])
                possBirds = list(cur.fetchone())[:-5]
                localStat = {"I":"Introduced","M":"Migrant","R":"Resident","Va":"Vagrant","Vi":"Visitor","E":"Extirpated"}
            else:
                statement = "SELECT Num, EngName, Family, SciName FROM Birds WHERE "
                params = []
                for i in session["possBirds"]:
                    statement += "Num=? OR "
                    params.append(i)
                cur.execute(statement[:-4], params)
                possBirds = cur.fetchall()
            return render_template("possible_birds.html", possBirds=possBirds, birdCount=birdCount, localStat=localStat)
    
    else:
        return redirect(url_for("id_bp.identify_get"))

@id_bp.teardown_request
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

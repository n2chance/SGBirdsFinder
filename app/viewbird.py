from flask import Blueprint, render_template, g
import sqlite3
import requests

viewbird_bp = Blueprint('viewbird_bp', __name__, template_folder='templates/viewbird')

DATABASE = 'app/Birds.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@viewbird_bp.route("/<int:birdNum>",methods=["GET"])
def viewbird(birdNum):
    cur = get_db().cursor()
    cur.execute("SELECT Family, Num, EngName, SciName, MalName, ChName, RarityStatus, LocalStatus, Identification, Habitat, Behaviour, MinSize, MaxSize FROM Birds WHERE Num = ?",(birdNum,))
    birdInfo = cur.fetchone()
    if birdInfo:
        # Create links for the bird        
        engNamel = list(birdInfo["EngName"])
        invalidChar = "\'"
        while invalidChar in engNamel:
            engNamel.remove(invalidChar)
        sgBirdsName = "".join(engNamel)

        sciNamel = list(birdInfo["SciName"])
        invalidChar = " "
        while invalidChar in sciNamel:
            sciNamel[sciNamel.index(invalidChar)] = "-"
        xenoName = "".join(sciNamel)

        sgBirdsLink = f"https://singaporebirds.com/species/{sgBirdsName}"
        iucnLink = f"https://apiv3.iucnredlist.org/api/v3/website/{birdInfo['SciName'].lower()}"
        xenoLink = f"https://xeno-canto.org/species/{xenoName}"
        
        links = {"More Information & Photos (Singapore Birds Project)":sgBirdsLink,"Conservation Status (IUCN Red List)":iucnLink,"Sound Recordings (xeno-canto)":xenoLink}
        for link in links:
            try:
                if link == "Conservation Status (IUCN Red List)":
                    continue # IUCN API takes too long to respond
                else:
                    resp = requests.get(links[link],timeout=0.01)
                    if response.status_code != requests.codes.ok:
                        links.pop(link)
            except:
                continue

        localStat = {"I":"Introduced","M":"Migrant","R":"Resident","Va":"Vagrant","Vi":"Visitor","E":"Extirpated"}

        return render_template("bird_info.html",birdInfo=birdInfo,localStat=localStat,links=links)
    else:
        return render_template("bird_not_found.html"), 404

@viewbird_bp.teardown_request
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Script to setup/reset the environment and files
import os
import secrets
import string
import sqlite3

def generateCred():
    chars = string.ascii_letters + string.digits
    username = "admin-" + ''.join(secrets.choice(chars) for i in range(3))
    while True:
        password = ''.join(secrets.choice(chars) for i in range(10))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return username, password

def setupEnv():
    user, pw = generateCred()
    with open(".env","w") as env:
        env.write(f"APP_SECRET_KEY={secrets.token_hex()}\n")
        env.write(f"ADMIN_USERNAME={user}\n")
        env.write(f"ADMIN_PASSWORD={pw}")
    print("Admin Credentials")
    print(f"Username: {user}")
    print(f"Password: {pw}")

def initdb(sqlFileN,dbName):
    with open(sqlFileN) as sqlFile:
        sqlScript = sqlFile.read()
    if os.access(dbName,os.F_OK):
        os.remove(dbName)
    db = sqlite3.connect(dbName)
    cur = db.cursor()
    cur.executescript(sqlScript)
    db.commit()
    db.close()
    print("Database successfully created")

# Ensure script is running from 'app' directory
APP_FOLDER_NAME = "app"
if os.getcwd().endswith(APP_FOLDER_NAME):
    pass
elif APP_FOLDER_NAME in os.listdir():
    os.chdir(APP_FOLDER_NAME)
else:
    raise Exception(f"{APP_FOLDER_NAME} folder not found")
    
setupEnv()
initdb("Birds.sql","Birds.db")

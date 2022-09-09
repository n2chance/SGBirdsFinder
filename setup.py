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
    # Generate .env file with secret key, username, password
    user, pw = generateCred()
    with open(".env","w") as env:
        env.write(f"APP_SECRET_KEY={secrets.token_hex()}\n")
        env.write(f"ADMIN_USERNAME={user}\n")
        env.write(f"ADMIN_PASSWORD={pw}")
    print("Admin Credentials")
    print(f"Username: {user}")
    print(f"Password: {pw}")

def initdb(sqlFileN,dbName):
    # Initialise database
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

inp = input("Generate credentials? (y/n): ")
if inp == "y":
    setupEnv()

os.chdir("app")
inp = input("Generate db? (y/n): ")
if inp == 'y':
    initdb("Birds.sql","Birds.db")
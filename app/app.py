from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

# Ensure app is running from 'app' directory
APP_FOLDER_NAME = "app"
if os.getcwd().endswith(APP_FOLDER_NAME):
    pass
elif APP_FOLDER_NAME in os.listdir():
    os.chdir(APP_FOLDER_NAME)
else:
    raise Exception(f"{APP_FOLDER_NAME} folder not found")

from general import general_bp
from auth import auth_bp
from identify import id_bp
from viewbird import viewbird_bp
from browse import browse_bp
from errors import errorhandler_bp
from admin import admin_bp

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")

# Each part of the app is a blueprint
app.register_blueprint(general_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(id_bp, url_prefix='/identify')
app.register_blueprint(viewbird_bp, url_prefix='/bird')
app.register_blueprint(browse_bp, url_prefix='/browse')
app.register_blueprint(errorhandler_bp)

if __name__ == "__main__":
    app.run()

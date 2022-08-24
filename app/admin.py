from flask import Blueprint, render_template, request, redirect, url_for, flash, g

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates/admin')

DATABASE = 'Birds.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db



@auth_bp.teardown_request
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
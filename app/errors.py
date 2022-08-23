from flask import Blueprint, render_template

errorhandler_bp = Blueprint('errorhandler_bp', __name__, template_folder='templates/errors')

@errorhandler_bp.app_errorhandler(404)
def notfound(error):
    return render_template("page_not_found.html"), 404

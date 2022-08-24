from flask import Flask

from general import general_bp
from auth import auth_bp
from identify import id_bp
from viewbird import viewbird_bp
from browse import browse_bp
from errors import errorhandler_bp
from admin import admin_bp

app = Flask(__name__)
app.secret_key = "1d997c309e2fa8d2993c120ab51459f8b421f89c65a496410b17508e18c4a6ea"

app.register_blueprint(general_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(id_bp, url_prefix='/identify')
app.register_blueprint(viewbird_bp, url_prefix='/bird')
app.register_blueprint(browse_bp, url_prefix='/browse')
app.register_blueprint(errorhandler_bp)

if __name__ == "__main__":
    app.run()

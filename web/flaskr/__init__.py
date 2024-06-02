from flask import Flask
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
    app.config.from_object(config_class)
    init_extensions(app)
    register_blueprints(app)
    return app

def register_blueprints(app: Flask):
    from flaskr.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    from flaskr.frontend import frontend_bp
    app.register_blueprint(frontend_bp, url_prefix='')

def init_extensions(app: Flask):
    # SQLAlchemy database, Flask Login
    from flaskr.extensions import db, login_manager
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Please login first.'
    login_manager.login_message_category = 'info'

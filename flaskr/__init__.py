from flask import Flask

from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here

    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    # admin blueprint
    from flaskr.admin import admin_bp
    app.register_blueprint(admin_bp)

	# frontend blueprint
    from flaskr.frontend import frontend_bp
    app.register_blueprint(frontend_bp)
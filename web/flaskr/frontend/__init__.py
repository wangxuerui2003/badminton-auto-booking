from flask import Blueprint

frontend_bp = Blueprint('frontend', __name__)

from flaskr.frontend import routes
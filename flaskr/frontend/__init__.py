from flask import Blueprint

frontend_bp = Blueprint('frontend', __name__, url_prefix='')

from flaskr.frontend import routes
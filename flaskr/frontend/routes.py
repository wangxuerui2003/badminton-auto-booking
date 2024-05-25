from flask import render_template
from flaskr.frontend import frontend_bp


@frontend_bp.route('/')
def index():
    return render_template('frontend/index.html')
from flask import render_template
from flask_login import login_required
from flaskr.admin import admin_bp
from .auth import routes


@admin_bp.route('/')
@login_required
def index():
    # TODO: display a UI for admin to adjust the desired court time in day, day in week
    return render_template('admin/index.html')


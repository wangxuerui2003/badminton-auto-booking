from flask import render_template
from flaskr.admin import admin_bp


@admin_bp.route('/')
def index():
    return render_template('admin/index.html')
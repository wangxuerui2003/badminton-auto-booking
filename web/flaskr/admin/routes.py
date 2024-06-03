from flask import abort, jsonify, redirect, render_template, request, url_for
from flask_login import login_required
from flaskr.admin import admin_bp
from flaskr.admin.forms.NewTaskForm import NewTaskForm
from .auth import routes
from flaskr.models.booking import Booking
from flaskr.extensions import db
import redis
import json
import os


REDIS_HOST = os.environ.get('REDIS_HOST') or 'localhost'
REDIS_PORT = os.environ.get('REDIS_PORT') or 6379
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

REDIS_QUEUE_KEY = os.environ.get('REDIS_QUEUE_KEY') or "1234"


@admin_bp.route('/')
@login_required
def index():
    # TODO: read jobs history and status from bot and display
    # TODO: add navbar for adding and removing tasks
    tasks = Booking.query.all()
    return render_template('admin/index.html', tasks=tasks)

@admin_bp.route('/new_task', methods=["GET", "POST"])
@login_required
def new_task():
    if request.method == 'GET':
        return render_template('admin/new_task.html')
    form: NewTaskForm = NewTaskForm()
    if form.validate_on_submit():
        booking = Booking(date=form.date.data,
                          weekday=form.weekday.data, time_from=form.time_from.data, time_to=form.time_to.data)
        db.session.add(booking)
        db.session.commit()
        r.rpush(REDIS_QUEUE_KEY, json.dumps(booking.to_dict()))
        return redirect(url_for('admin.index'))
    return 'Error', 400




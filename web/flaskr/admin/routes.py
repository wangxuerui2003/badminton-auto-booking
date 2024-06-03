from flask import jsonify, render_template, request
from flask_login import login_required
from flaskr.admin import admin_bp
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
    # TODO: display a UI for admin to adjust the desired court time in day, day in week
    return render_template('admin/index.html')

@admin_bp.route('/new_task', methods=["POST"])
@login_required
def new_task():
    data = request.form
    # booking = Booking(date='2024-06-02', time_from=11, time_to=13)
    # db.session.add(booking)
    # db.session.commit()
    # r.rpush(REDIS_QUEUE_KEY, json.dumps(booking.to_dict()))
    return jsonify(data)



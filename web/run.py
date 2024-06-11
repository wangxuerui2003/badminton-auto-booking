import os
from flaskr import create_app
from flaskr.extensions import db, redis_conn, REDIS_JOBS_QUEUE_KEY
from flaskr.models.admin import Admin
from flaskr.models.booking import Booking
from flaskr.models.booking_history import BookingHistory
import json
import logging


app = create_app()

def create_super_admin():
    if Admin.query.first():
        return
    super_admin = Admin(username=os.environ.get('SUPER_ADMIN_USERNAME'))
    super_admin.set_password(os.environ.get('SUPER_ADMIN_PASSWORD'))
    db.session.add(super_admin)
    db.session.commit()

def init_tasks():
    tasks = Booking.filter_ongoing_tasks()
    for task in tasks:
        redis_conn.rpush(REDIS_JOBS_QUEUE_KEY, json.dumps(task.to_dict()))

# create all tables for models if not exist
with app.app_context():
    db.create_all()
    create_super_admin()
    init_tasks()


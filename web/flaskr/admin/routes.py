from flask import abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required
from flaskr.admin import admin_bp
from flaskr.admin.forms.NewTaskForm import NewTaskForm
from .auth import routes
from flaskr.models.booking import Booking
from flaskr.extensions import db, redis_conn, REDIS_JOBS_QUEUE_KEY
import json


@admin_bp.route('/')
@login_required
def index():
    # TODO: read jobs history and status from bot and display
    tasks = Booking.query.all()
    return render_template('admin/index.html', tasks=tasks)

@admin_bp.route('/new-task', methods=["GET", "POST"])
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
        redis_conn.rpush(REDIS_JOBS_QUEUE_KEY, json.dumps(booking.to_dict()))
        return redirect(url_for('admin.index'))
    return 'Error', 400

@admin_bp.route('/delete-task', methods=["POST"])
@login_required
def delete_task():
    task_id = request.form.get('task_id')
    booking = Booking.query.get(task_id)
    if booking:
        db.session.delete(booking)
        db.session.commit()
        flash(f'Successfully deleted task {booking}', 'success')
        return redirect(url_for('admin.index'))
    flash('Task not found', 'danger')
    return redirect(url_for('admin.index'))
    



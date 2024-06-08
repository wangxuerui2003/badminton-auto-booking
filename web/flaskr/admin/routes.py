from urllib.parse import urljoin
from flask import abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required
from flaskr.admin import admin_bp
from flaskr.admin.forms.NewTaskForm import NewTaskForm
from flaskr.models.booking_history import BookingHistory
from .auth import routes
from flaskr.models.booking import Booking
from flaskr.extensions import db, redis_conn, REDIS_JOBS_QUEUE_KEY, REDIS_HISTORY_QUEUE_KEY
import json
from datetime import datetime
import requests
import os


def delete_job_from_bot(job_id):
    url = urljoin(os.environ.get('BOT_HOST'), '/remove-job')
    res = requests.post(url, data={
        "id": job_id
    })

@admin_bp.route('/')
@login_required
def index():
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
        delete_job_from_bot(booking.id)
        db.session.delete(booking)
        db.session.commit()
        flash(f'Successfully deleted task {booking}', 'success')
        return redirect(url_for('admin.index'))
    flash('Task not found', 'danger')
    return redirect(url_for('admin.index'))

@admin_bp.route('/booking/<int:booking_id>/histories')
def booking_histories(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    histories = booking.histories  # Accessing the related histories
    return render_template('admin/booking_histories.html', booking=booking, histories=histories)

@admin_bp.route('/history', methods=['GET'])
@login_required
def history():
    history_str = redis_conn.lpop(REDIS_HISTORY_QUEUE_KEY)
    while history_str:
        history = json.loads(history_str)
        booking_history = BookingHistory(
            target_date=datetime.strptime(history['target_date'], "%Y-%m-%d"),
            booking_id=history['booking_id'],
            status=history['status'])
        db.session.add(booking_history)
        db.session.commit()
        history_str = redis_conn.lpop(REDIS_HISTORY_QUEUE_KEY)
    histories = BookingHistory.query.order_by(BookingHistory.created_at.desc()).all()
    return render_template('admin/history.html', histories=histories)
    



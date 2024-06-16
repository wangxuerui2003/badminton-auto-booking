import time
from datetime import datetime, timedelta
import schedule
from threading import Thread, Event
from scraper import BookingStatus, Scraper
import os
import redis
import json
import sys
import logging


logging.basicConfig(
	format='%(asctime)s %(levelname)-8s %(message)s', 
	level=logging.INFO,
	datefmt='%Y-%m-%d %H:%M:%S')


REDIS_HOST = os.environ.get('REDIS_HOST') or 'localhost'
REDIS_PORT = os.environ.get('REDIS_PORT') or 6379
REDIS_JOBS_QUEUE_KEY = os.environ.get('REDIS_JOBS_QUEUE_KEY') or "1234"
REDIS_HISTORY_QUEUE_KEY = os.environ.get('REDIS_HISTORY_QUEUE_KEY') or "1234"
BOOKING_INTERVAL_MINUTES = int(os.environ.get('BOOKING_INTERVAL_MINUTES') or '1')

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


class BookingInfo:
	def __init__(self, booking_dict: dict):
		self.id = booking_dict.get('id', None)
		self.date = booking_dict.get('date', None)
		self.weekday = booking_dict.get('weekday', None)
		self.time_from = booking_dict.get('time_from', None)
		self.time_to = booking_dict.get('time_to', None)

	def is_past(self):
		if self.date is None:
			return True
		date = datetime.strptime(self.date, '%Y-%m-%d')
		return date.date() < datetime.now().date()

	def __str__(self) -> str:
		if self.weekday:
			return f"Repeat every {self.weekday} from {self.time_from} to {self.time_to}"
		return f"Single time job {self.date} from {self.time_from} to {self.time_to}"


class BookingBot(Thread):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.jobs: dict[str, schedule.Job] = {}
		self.repeated_jobs: dict[str, BookingInfo] = {}
		self.stop_run = Event()
		self.interval = kwargs.get('interval', 1)

	def read_job(self):
		''' Read jobs from redis and add to bot '''
		booking_str = r.lpop(REDIS_JOBS_QUEUE_KEY)
		if not booking_str:
			return
		booking_dict = json.loads(booking_str)
		booking = BookingInfo(booking_dict)
		if self.jobs.get(booking.id, None) is not None:
			return
		elif self.repeated_jobs.get(booking.id, None) is not None:
			return
		if booking.weekday is not None:
			self.repeated_jobs[booking.id] = booking
		else:
			self.add_job(booking)
		logging.info(f"Received job {booking}")

	def add_job(self, booking: BookingInfo):
		''' Add a job to bot '''
		# TODO: optimize this in the future with _calculate_job_exe_time
		job = schedule.every(BOOKING_INTERVAL_MINUTES).minutes.do(self._job, booking)
		self.jobs[booking.id] = job

	def remove_job(self, id):
		''' Remove a job from bot '''
		if self.jobs.get(id):
			job = self.jobs.pop(id)
			schedule.cancel_job(job)
			return True
		elif self.repeated_jobs.get(id):
			self.repeated_jobs.pop(id)
			return True
		return False

	def schedule_repeated_jobs(self):
		for id, repeated_job in self.repeated_jobs.items():
			if repeated_job.is_past():
				self.repeated_jobs[id].date = get_next_weekday(repeated_job.weekday).strftime('%Y-%m-%d') 
				self.add_job(self.repeated_jobs[id])
				logging.info(f"Scheduled single time job {self.repeated_jobs[id].date} from {repeated_job.time_from} to {repeated_job.time_to} to for repeated job.")

	def _job(self, booking: BookingInfo):
		''' The core court booking bot function '''
		date = booking.date
		if datetime.strptime(date, '%Y-%m-%d').date() < datetime.now().date():
			r.rpush(REDIS_HISTORY_QUEUE_KEY, json.dumps({
				"booking_id": booking.id,
				"target_date": booking.date,
				"status": 'fail'
			}))
			self.remove_job(booking.id)
			return schedule.CancelJob
		bot = Scraper()
		booking_status = bot.book_court(date, booking.time_from, booking.time_to)
		logging.info(f'Booking court at date {date}, from {booking.time_from} to {booking.time_to}. Status [{booking_status.name}]')
		# r.rpush(REDIS_HISTORY_QUEUE_KEY, json.dumps({
		# 		"booking_id": booking.id,
		# 		"target_date": booking.date,
		# 		"status": booking_status.name
		# 	}))
		if booking_status != BookingStatus.BOOKED and booking_status != BookingStatus.SUCCESS:
			return;
		r.rpush(REDIS_HISTORY_QUEUE_KEY, json.dumps({
			"booking_id": booking.id,
			"target_date": booking.date,
			"status": 'success'
		}))
		self.remove_job(booking.id)
		return schedule.CancelJob

	def run(self):
		''' Start the bot '''
		while not self.stop_run.is_set():
			self.read_job()
			self.schedule_repeated_jobs()
			schedule.run_pending()
			time.sleep(self.interval)

	def stop(self):
		''' Stop the bot '''
		self.stop_run.set()

	def _calculate_job_exe_time(self):
		pass


def get_next_weekday(weekday: int):
    today = datetime.now()
    today_weekday = today.weekday()
    days_until_next = (weekday - today_weekday + 7) % 7
    next_weekday_date = today + timedelta(days=days_until_next)
    return next_weekday_date.date()

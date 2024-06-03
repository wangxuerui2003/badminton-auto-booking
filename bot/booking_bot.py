import time
from datetime import datetime, timedelta
import schedule
from threading import Thread, Event
from scraper import Scraper
import os
import redis
import json
from scraper import BookingStatus


REDIS_HOST = os.environ.get('REDIS_HOST') or 'localhost'
REDIS_PORT = os.environ.get('REDIS_PORT') or 6379
REDIS_QUEUE_KEY = os.environ.get('REDIS_QUEUE_KEY') or "1234"

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


class BookingInfo:
	def __init__(self, booking_dict: dict):
		self.id = booking_dict.get('id', None)
		self.date = booking_dict.get('date', None)
		self.day_in_week = booking_dict.get('day_in_week', None)
		self.time_from = booking_dict.get('time_from', None)
		self.time_to = booking_dict.get('time_to', None)


class BookingBot(Thread):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.jobs: dict[str, schedule.Job] = {}
		self.stop_run = Event()
		self.interval = kwargs.get('interval', 1)

	def read_job(self):
		''' Read jobs from redis and add to bot '''
		booking_str = r.lpop(REDIS_QUEUE_KEY)
		if not booking_str:
			return
		booking_dict = json.loads(booking_str)
		booking = BookingInfo(booking_dict)
		self.add_job(booking)

	def add_job(self, booking: BookingInfo):
		''' Add a job to bot '''
		is_repeated = booking.day_in_week is not None
		# TODO: optimize this in the future with _calculate_job_exe_time
		job = schedule.every(10).seconds.do(self._job, is_repeated, booking)
		if is_repeated:
			self.jobs[booking.id] = job

	def remove_job(self, id):
		''' Remove a job from bot '''
		if self.jobs.get(id):
			job = self.jobs.pop(id)
			schedule.cancel_job(job)

	def _job(self, repeat: bool, booking: BookingInfo):
		''' The core court booking bot function '''
		date = booking.date
		if repeat:
			date = get_next_weekday(booking.day_in_week)
		bot = Scraper()
		booking_status = bot.book_court(date, booking.time_from, booking.time_to)
		if booking_status == BookingStatus.FAILED:
			return
		if repeat:
			return
		self.remove_job(booking.id)
		return schedule.CancelJob

	def run(self):
		''' Start the bot '''
		while not self.stop_run.is_set():
			self.read_job()
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

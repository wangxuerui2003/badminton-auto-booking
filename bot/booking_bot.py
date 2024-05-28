import time
from datetime import datetime, timedelta
import schedule
from threading import Thread, Event
from flaskr.models.booking import Booking
from bot.scraper import Scraper


class BookingBot:
	def __init__(self, bookings: list[Booking] = []):
		self.repeated_jobs: dict[str, schedule.Job] = {}
		self.jobs: dict[str, schedule.Job] = {}
		self.stop_run = Event()
		self.thread = None
		for booking in bookings:
			self.add_job(booking)

	def add_job(self, booking: Booking):
		''' Add a job to bot '''
		is_repeated = booking.day_in_week is not None
		# TODO: optimize this in the future with _calculate_job_exe_time
		job = schedule.every(10).seconds.do(self._job, is_repeated, booking)
		if is_repeated:
			self.repeated_jobs[booking.id] = job
		else:
			self.jobs[booking.id] = job

	def remove_job(self, id):
		''' Remove a job from bot '''
		if self.repeated_jobs.get(id):
			job = self.repeated_jobs.pop(id)
		elif self.jobs.get(id):
			job = self.jobs.pop(id)
		else:
			return
		schedule.cancel_job(job)
		

	def run_jobs(self, interval=1):
		''' Infinite loop that runs schedule pending jobs '''
		while not self.stop_run.is_set():
			schedule.run_pending()
			time.sleep(interval)

	def _job(self, repeat: bool, booking: Booking):
		''' The core court booking bot function '''
		print("Running job...")
		date = booking.date
		if repeat:
			date = get_next_weekday(booking.day_in_week)
		bot = Scraper(date, booking.time_from, booking.time_to)
		if not bot.book_court():
			return
		if repeat:
			return
		self.remove_job(booking.id)
		return schedule.CancelJob

	def start(self, interval=1):
		''' Start the bot '''
		if self.thread is None:
			self.stop_run.clear()
			self.thread = Thread(target=self.run_jobs, args=(interval,))
			self.thread.start()

	def stop(self):
		''' Stop the bot '''
		self.stop_run.set()
		if self.thread is not None:
			self.thread.join()
			self.thread = None

	def _calculate_job_exe_time(self):
		pass


def get_next_weekday(weekday: int):
    today = datetime.now()
    today_weekday = today.weekday()
    days_until_next = (weekday - today_weekday + 7) % 7
    next_weekday_date = today + timedelta(days=days_until_next)
    return next_weekday_date.date()

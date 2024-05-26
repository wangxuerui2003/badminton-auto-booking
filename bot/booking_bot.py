import time
import datetime
import schedule
from threading import Thread, Event
from flaskr.models.booking import Booking


class BookingBot:
	def __init__(self, bookings: list[Booking] = []):
		self.repeated_jobs: schedule.Job = []
		self.jobs = schedule.Job = []
		self.stop_run = Event()
		self.thread = None

		# TODO: init jobs from bookings

	def add_job(self, booking: Booking):
		''' Add a job to bot '''
		pass

	def remove_job(self, id):
		''' Remove a job from bot '''
		pass

	def run_jobs(self):
		''' Infinite loop that runs schedule pending jobs '''
		pass

	def _job(self):
		''' The core court booking bot function '''
		pass

	def start(self, interval=1):
		''' Start the bot '''
		pass

	def stop(self):
		''' Stop the bot '''
		pass

	def _calculate_job_exe_time(self):
		pass

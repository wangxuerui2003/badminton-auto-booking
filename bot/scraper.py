from requests import Session
from bs4 import BeautifulSoup
from datetime import datetime
import os
from urllib.parse import urljoin, urlparse


def get_host(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

WEBSITE_URL = os.environ.get('WEBSITE_URL')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Referer': 'https://www.google.com/',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
	'Host': get_host(WEBSITE_URL),
	'Origin': WEBSITE_URL,
	'Referer': WEBSITE_URL
}


class Scraper:
	def __init__(self):
		self.session = Session()
		self.url = WEBSITE_URL
		self.login_url = os.environ.get('LOGIN_URL')
		self.court_booking_path = os.environ.get('COURT_BOOKING_PATH')
		self.num_courts = int(os.environ.get('NUM_COURTS'))
		self.login()

	def login(self):
		self.session.post(self.login_url, headers=HEADERS, timeout=5, data={
			'login_type': '1',
			'username': os.environ.get('WEBSITE_USERNAME'),
			'password': os.environ.get('WEBSITE_PASSWORD')
		})

	def get_booked_courts(self):
		# TODO
		pass

	def time_booked(self, date_str: str, time_from: int, time_to: int):
		# TODO
		return True

	def book_court(self, date: datetime, time_from: int, time_to: int):
		date_str = date.strftime('%Y-%m-%d')
		booking_url = urljoin(self.url, self.court_booking_path)
		for i in range(1, self.num_courts + 1):
			court_booking_url = urljoin(booking_url, str(i))
			res = self.session.post(court_booking_url, headers=HEADERS, timeout=5, params={
				'Date': datetime.now().strftime('%Y-%m-%d')
			}, data={
				'DateFrom': date_str,
				'TimeFrom': str(time_from),
				'TimeTo': str(time_to),
				'accept_terms_checkbox': 'on',
				'accept_terms_checkbox2': 'on',
			})
			
			if self.time_booked(date_str, time_from, time_to):
				return True
		
		return False
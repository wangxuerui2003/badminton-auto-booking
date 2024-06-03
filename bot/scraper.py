from requests import Session
from bs4 import BeautifulSoup
from datetime import datetime
import os
from urllib.parse import urljoin, urlparse
from enum import Enum


class BookingStatus(Enum):
	SUCCESS = 1
	FAILED = 2
	NOT_AVAILABLE = 3
	TOO_EARLY = 4


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
		self.court_booking_path = urljoin(self.url, os.environ.get('COURT_BOOKING_PATH'))
		self.current_courts_path = urljoin(self.url, os.environ.get('CURRENT_COURTS_PATH'))
		self.num_courts = int(os.environ.get('NUM_COURTS'))
		self.login()

	def login(self):
		self.session.post(self.login_url, headers=HEADERS, timeout=5, data={
			'login_type': '1',
			'username': os.environ.get('WEBSITE_USERNAME'),
			'password': os.environ.get('WEBSITE_PASSWORD')
		})

	def get_booked_courts(self):
		r = self.session.get(self.current_courts_path, headers=HEADERS)
		if not r.ok:
			return []
		soup = BeautifulSoup(r.text, 'html.parser')
		booking_table = soup.select_one('.kt-portlet__body .table')
		headers = ['facility', '', 'date', 'time_from', 'time_to', '', '']
		data = []
		for row in booking_table.find_all('tr')[1:]:  # Skip the header row
			cells = row.find_all('td')
			if len(cells) > 0:
				row_data = {}
				for i, cell in enumerate(cells):
					if headers[i] == '':
						continue
					row_data[headers[i]] = cell.text.strip()
				if row_data['facility'].lower().startswith('badminton'):
					row_data['date'] = datetime.strptime(row_data['date'], '%d-%m-%Y').strftime('%Y-%m-%d')
					data.append(row_data)
		return data

	def time_available(self, date: str, time_from: int, time_to: int):
		if time_to - time_from > 2 or time_to - time_from < 1:
			return False
		for i in range(1, self.num_courts + 1):
			court_booking_url = urljoin(self.court_booking_path, str(i))
			r = self.session.get(court_booking_url, headers=HEADERS, timeout=5, params={
				'Date': date
			})
			if not r.ok:
				return False
			soup = BeautifulSoup(r.text, 'html.parser')
			booking_table = soup.select_one('.kt-portlet__body .table')
			avaibale = True
			for time, row in enumerate(booking_table.find_all('tr')[1:], start=7):  # Skip the header row
				if time != time_from and time != time_to - 1:
					continue
				cells = row.find_all('td')
				if len(cells) <= 0:
					avaibale = False
				if cells[1].text.strip() != 'Available':
					avaibale = False
					break
			if avaibale:
				return True
		return False

	def time_booked(self, date: str, time_from: int, time_to: int):
		booked_courts = self.get_booked_courts()
		for booked_court in booked_courts:
			booked_court['time_from'] = datetime.strptime(booked_court['time_from'], "%I:%M %p").hour
			booked_court['time_to'] = datetime.strptime(booked_court['time_to'], "%I:%M %p").hour
			if booked_court['date'] == date and booked_court['time_from'] == time_from and booked_court['time_to'] == time_to:
				return True
		return False

	def book_court(self, date: str, time_from: int, time_to: int) -> BookingStatus:
		if not self.time_available(date, time_from, time_to):
			return BookingStatus.NOT_AVAILABLE
		if self.time_booked(date, time_from, time_to):
			return BookingStatus.SUCCESS
		for i in range(1, self.num_courts + 1):
			court_booking_url = urljoin(self.court_booking_path, str(i))
			res = self.session.post(court_booking_url, headers=HEADERS, timeout=5, params={
				'Date': datetime.now().strftime('%Y-%m-%d')
			}, data={
				'DateFrom': date,
				'TimeFrom': str(time_from),
				'TimeTo': str(time_to),
				'accept_terms_checkbox': 'on',
				'accept_terms_checkbox2': 'on',
			})
			
			if self.time_booked(date, time_from, time_to):
				return BookingStatus.SUCCESS
		
		return BookingStatus.FAILED
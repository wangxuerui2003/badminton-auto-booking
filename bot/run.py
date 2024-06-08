from fastapi import FastAPI
from scraper import Scraper
from booking_bot import BookingBot

bot = BookingBot()
bot.setDaemon(True)
bot.start()

app = FastAPI()

@app.get('/booked-courts')
async def get_booked_courts():
	scraper = Scraper()
	return scraper.get_booked_courts()

@app.get('/task_ids')
async def get_task_ids():
	return list(bot.jobs.keys())

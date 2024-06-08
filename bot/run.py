from fastapi import FastAPI, HTTPException
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

@app.post('/remove-job')
async def remove_job(id: str):
	if bot.remove_job(id):
		return 'OK'
	return HTTPException(status_code=404, detail="Job not found")

@app.get('/task-ids')
async def get_task_ids():
	return list(bot.jobs.keys())

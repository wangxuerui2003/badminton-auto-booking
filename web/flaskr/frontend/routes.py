from flask import render_template
from flaskr.frontend import frontend_bp
import requests
from urllib.parse import urljoin
import os

bot_get_booked_courts_url = urljoin(os.environ.get('BOT_HOST'), '/get-booked-courts')

def get_booked_courts_from_bot():
    url = bot_get_booked_courts_url
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


@frontend_bp.route('/')
def index():
    booked_courts = get_booked_courts_from_bot()
    return render_template('frontend/index.html', booked_courts=booked_courts)
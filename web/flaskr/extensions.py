from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import redis


db = SQLAlchemy()

login_manager = LoginManager()

REDIS_HOST = os.environ.get('REDIS_HOST') or 'localhost'
REDIS_PORT = os.environ.get('REDIS_PORT') or 6379
REDIS_JOBS_QUEUE_KEY = os.environ.get('REDIS_JOBS_QUEUE_KEY') or "1234"
REDIS_HISTORY_QUEUE_KEY = os.environ.get('REDIS_HISTORY_QUEUE_KEY') or "1234"
redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

import os

basedir = os.path.abspath(os.path.dirname(__file__))

db_uri = "postgresql://{user}:{password}@{host}/{database}".format(
    user=os.environ.get('POSTGRES_USER'),
    password=os.environ.get('POSTGRES_PASSWORD'),
    host=os.environ.get('POSTGRES_HOST'),
    database=os.environ.get('POSTGRES_DB')
)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False

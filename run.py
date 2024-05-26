import os
from flaskr import create_app
from flaskr.extensions import db
from dotenv import load_dotenv


load_dotenv()

app = create_app()


if __name__ == "__main__":
    # create all tables for models if not exist
    with app.app_context():
        db.create_all()

    if os.environ.get('APP_ENV') == 'local':
        app.run(debug=True)
    else:
        app.run()

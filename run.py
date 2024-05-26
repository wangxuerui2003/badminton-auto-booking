import os
from flaskr import create_app
from flaskr.extensions import db
from dotenv import load_dotenv
from flaskr.models.admin import Admin


load_dotenv()

app = create_app()

def create_super_admin():
    if Admin.query.first():
        return
    super_admin = Admin(username=os.environ.get('SUPER_ADMIN_USERNAME'))
    super_admin.set_password(os.environ.get('SUPER_ADMIN_PASSWORD'))
    db.session.add(super_admin)
    db.session.commit()


if __name__ == "__main__":
    # create all tables for models if not exist
    with app.app_context():
        db.create_all()
        create_super_admin()

    if os.environ.get('APP_ENV') == 'local':
        app.run(debug=True)
    else:
        app.run()

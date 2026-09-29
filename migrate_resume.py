"""Create the table used to store the Google Drive resume setting.

Run once (or safely re-run) in the environment connected to the production database:
    python migrate_resume.py
"""

from app import app
from models import ResumeSetting, db


def migrate_resume(flask_app=app):
    with flask_app.app_context():
        ResumeSetting.__table__.create(bind=db.engine, checkfirst=True)
        print('Resume settings table is ready. Add the first link from the admin dashboard.')


if __name__ == '__main__':
    migrate_resume()

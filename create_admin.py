import sys
import os
from app import app
from models import db, User

def create_admin(username, password):
    with app.app_context():
        db.create_all()
        # Check if user exists
        if User.query.filter_by(username=username).first():
            print(f"User {username} already exists.")
            return

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        print(f"Admin user {username} created successfully!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python create_admin.py <username> <password>")
    else:
        create_admin(sys.argv[1], sys.argv[2])

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    labels = db.Column(db.ARRAY(db.String), nullable=False)
    image_placeholder = db.Column(db.String(500))
    github = db.Column(db.String(500))

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    id = db.Column(db.String(100), primary_key=True) # UUID from JSON
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    recommendation = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(500))

class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)

class Certification(db.Model):
    __tablename__ = 'certifications'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False) # 'professional' or 'courses'
    title = db.Column(db.String(200), nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(500))
    url = db.Column(db.String(500))
    related_project_url = db.Column(db.String(500))

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tags = db.Column(db.ARRAY(db.String), nullable=False)
    image_url = db.Column(db.String(500))
    post_url = db.Column(db.String(500))
    mode = db.Column(db.String(50), nullable=False) # 'in_person' or 'online'


class ResumeSetting(db.Model):
    """The single, public resume URL displayed across the portfolio."""
    __tablename__ = 'resume_settings'

    id = db.Column(db.Integer, primary_key=True)
    resume_url = db.Column(db.String(500), nullable=False)

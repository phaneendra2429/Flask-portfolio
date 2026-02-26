import json
import os
from app import app
from models import db, Project, Recommendation, Skill, Certification, Event

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def migrate():
    with app.app_context():
        # Create tables
        db.create_all()
        print("Tables created.")

        # Migrate Projects
        projects_data = load_json('templates/json/cards_data.json')
        for item in projects_data:
            if not Project.query.filter_by(title=item['title']).first():
                project = Project(
                    title=item['title'],
                    description=item['description'],
                    labels=item['labels'],
                    image_placeholder=item['image_placeholder'],
                    github=item['github']
                )
                db.session.add(project)
        print("Projects migrated.")

        # Migrate Recommendations
        rec_data = load_json('templates/json/recommendations.json')
        for item in rec_data:
            if not Recommendation.query.filter_by(id=item['id']).first():
                rec = Recommendation(
                    id=item['id'],
                    name=item['name'],
                    title=item['title'],
                    recommendation=item['recommendation'],
                    date=item['date'],
                    image=item['image']
                )
                db.session.add(rec)
        print("Recommendations migrated.")

        # Migrate Skills
        skills_data = load_json('templates/json/skills.json')
        for category, names in skills_data.items():
            for name in names:
                if not Skill.query.filter_by(category=category, name=name).first():
                    skill = Skill(category=category, name=name)
                    db.session.add(skill)
        print("Skills migrated.")

        # Migrate Certifications
        cert_data = load_json('templates/json/certifications.json')
        for category, items in cert_data.items():
            for item in items:
                if not Certification.query.filter_by(title=item['title']).first():
                    cert = Certification(
                        category=category,
                        title=item['title'],
                        platform=item['platform'],
                        date=item['date'],
                        image=item['image'],
                        url=item['url'],
                        related_project_url=item.get('related_project_url')
                    )
                    db.session.add(cert)
        print("Certifications migrated.")

        # Migrate Events
        events_data = load_json('templates/json/events.json')
        for item in events_data:
            if not Event.query.filter_by(title=item['title']).first():
                event = Event(
                    title=item['title'],
                    description=item['description'],
                    tags=item['tags'],
                    image_url=item['image_url'],
                    post_url=item['post_url'],
                    mode=item['mode']
                )
                db.session.add(event)
        print("Events migrated.")

        db.session.commit()
        print("Migration completed successfully!")

if __name__ == '__main__':
    migrate()

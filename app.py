from flask import Flask, render_template, jsonify, request
import json
from routes.certifications import certifications
import os
from models import db, Project, Recommendation, Skill, Certification, User
from flask_login import LoginManager




app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-now-123')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost:5432/portfolio')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# JSON files are now only used for migration
projects_file = "templates/json/cards_data.json"


def load_json(file): 
    with open(file, "r") as f: return json.load(f)

@app.route('/')
def index():
    projects_list = Project.query.all()
    recommendations_list = Recommendation.query.all()
    
    # Structure skills into categories for the template
    skills_query = Skill.query.all()
    skills_data = {}
    for s in skills_query:
        skills_data.setdefault(s.category, []).append(s.name)
        
    # Structure certifications for the template
    certs_query = Certification.query.all()
    certifications_data = {'professional': [], 'courses': []}
    for c in certs_query:
        cert_item = {
            'title': c.title,
            'platform': c.platform,
            'date': c.date,
            'image': c.image,
            'url': c.url,
            'related_project_url': c.related_project_url
        }
        certifications_data[c.category].append(cert_item)

    return render_template(
        'index.html',
        projects=projects_list,
        recommendations=recommendations_list,
        skills_data=skills_data,
        certifications=certifications_data
    )


@app.route('/filter_projects', methods=['POST'])
def filter_projects():
    category = request.json['category']
    # If category is 'all', return all projects
    if category.lower() == 'all':
        projects_data = Project.query.all()
    else:
        # PostgreSQL specific query for ARRAY column
        projects_data = Project.query.filter(Project.labels.any(category)).all()
    
    # Convert to dictionary for JSON response
    result = []
    for p in projects_data:
        result.append({
            'title': p.title,
            'description': p.description,
            'labels': p.labels,
            'image_placeholder': p.image_placeholder,
            'github': p.github
        })
    return jsonify(result)

# Register blueprints
from routes.projects import projects
from routes.recommendations import recommend
from routes.events import events
from routes.skills import skills
from routes.certifications import certifications
from routes.auth import auth
from routes.admin import admin

app.register_blueprint(projects)
app.register_blueprint(recommend)
app.register_blueprint(events)
app.register_blueprint(skills)
app.register_blueprint(certifications)
app.register_blueprint(auth)
app.register_blueprint(admin)

if __name__ == '__main__':
    app.run(debug=True)

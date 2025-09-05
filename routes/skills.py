from flask import Blueprint, render_template, request, redirect, url_for
import json

skills = Blueprint('skills', __name__)
skills_file = "templates/json/skills.json"

def load_json(file): 
    with open(file, "r") as f: return json.load(f)

def save_to_json(data, file): 
    with open(file, "w") as f: json.dump(data, f, indent=4)

@skills.route('/add_skill', methods=['GET', 'POST'])
def add_skill():
    if request.method == 'POST':
        category = request.form['category']
        topics = request.form['topics'].split(',')
        skills_data = load_json(skills_file)
        skills_data.setdefault(category, []).extend(topics)
        save_to_json(skills_data, skills_file)
        return redirect(url_for('index'))
    return render_template('add_skills.html')

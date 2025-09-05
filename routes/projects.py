from flask import Blueprint, render_template, request, redirect, url_for
import json

projects = Blueprint('projects', __name__)
projects_file = "templates/json/cards_data.json"

def load_json(file): 
    with open(file, "r") as f: return json.load(f)

def save_to_json(data, file): 
    with open(file, "w") as f: json.dump(data, f, indent=4)

@projects.route('/add_project', methods=['GET', 'POST'])
def add_project():
    projects_data = load_json(projects_file)
    if request.method == 'POST':
        new_project = {
            "title": request.form['title'],
            "description": request.form['description'],
            "labels": request.form['labels'].split(','),
            "image_placeholder": request.form['image'],
            "github": request.form['github']
        }
        projects_data.append(new_project)
        save_to_json(projects_data, projects_file)
        return redirect(url_for('index'))
    return render_template('add_project.html', projects=projects_data)

@projects.route('/edit_project/<int:project_index>', methods=['GET', 'POST'])
def edit_project(project_index):
    projects_data = load_json(projects_file)
    project = projects_data[project_index]
    if request.method == 'POST':
        project.update({
            "title": request.form['title'],
            "description": request.form['description'],
            "labels": request.form['labels'].split(','),
            "image_placeholder": request.form['image'],
            "github": request.form['github']
        })
        save_to_json(projects_data, projects_file)
        return redirect(url_for('projects.add_project'))
    return render_template('edit_project.html', project=project, project_index=project_index)

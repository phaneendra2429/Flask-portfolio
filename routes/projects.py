from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Project

projects = Blueprint('projects', __name__)

@projects.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        new_project = Project(
            title=request.form['title'],
            description=request.form['description'],
            labels=request.form['labels'].split(','),
            image_placeholder=request.form['image'],
            github=request.form['github']
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('index'))
    projects_data = Project.query.all()
    return render_template('add_project.html', projects=projects_data)

@projects.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        project.title = request.form['title']
        project.description = request.form['description']
        project.labels = request.form['labels'].split(',')
        project.image_placeholder = request.form['image']
        project.github = request.form['github']
        db.session.commit()
        return redirect(url_for('projects.add_project'))
    return render_template('edit_project.html', project=project, project_index=project_id)

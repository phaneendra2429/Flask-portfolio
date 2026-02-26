from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Skill

skills = Blueprint('skills', __name__)

@skills.route('/add_skill', methods=['GET', 'POST'])
def add_skill():
    if request.method == 'POST':
        category = request.form['category']
        topics = request.form['topics'].split(',')
        for topic in topics:
            topic = topic.strip()
            if topic:
                new_skill = Skill(category=category, name=topic)
                db.session.add(new_skill)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_skills.html')

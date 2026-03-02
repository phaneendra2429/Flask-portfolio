from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
import uuid
from models import db, Recommendation

recommend = Blueprint('recommend', __name__)

@recommend.route('/add_recommendation', methods=['GET', 'POST'])
@login_required
def add_recommendation():
    if request.method == 'POST':
        rec_id = request.form.get('id')
        if rec_id:
            # Edit existing
            rec = Recommendation.query.get(rec_id)
            if rec:
                rec.name = request.form['name']
                rec.title = request.form['title']
                rec.recommendation = request.form['recommendation']
                rec.date = request.form['date']
                rec.image = request.form['image']
        else:
            # Add new
            new_rec = Recommendation(
                id=str(uuid.uuid4()),
                name=request.form['name'],
                title=request.form['title'],
                recommendation=request.form['recommendation'],
                date=request.form['date'],
                image=request.form['image']
            )
            db.session.add(new_rec)
        db.session.commit()
        return redirect(url_for('recommend.add_recommendation'))
        
    recommendations_list = [
        {
            'id': r.id,
            'name': r.name,
            'title': r.title,
            'recommendation': r.recommendation,
            'date': r.date,
            'image': r.image
        } for r in Recommendation.query.all()
    ]
    return render_template('add_rec.html', recommendations=recommendations_list)

@recommend.route('/delete_recommendation/<string:rec_id>')
@login_required
def delete_recommendation(rec_id):
    rec = Recommendation.query.get(rec_id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return redirect(url_for('recommend.add_recommendation'))

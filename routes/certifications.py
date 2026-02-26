from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Certification

certifications = Blueprint('certifications', __name__)

@certifications.route('/add_certification', methods=['GET', 'POST'])
def add_certification():
    if request.method == 'POST':
        category = request.form['category']
        new_cert = Certification(
            category=category,
            title=request.form['title'],
            platform=request.form['platform'],
            date=request.form['date'],
            image=request.form['image'],
            url=request.form['url']
        )
        db.session.add(new_cert)
        db.session.commit()
        return redirect(url_for('certifications.add_certification'))
        
    all_certs = Certification.query.order_by(Certification.category, Certification.id.desc()).all()
    return render_template('add_certification.html', certifications=all_certs)

@certifications.route('/edit_certification/<int:cert_id>', methods=['GET', 'POST'])
def edit_certification(cert_id):
    cert = Certification.query.get_or_404(cert_id)
    if request.method == 'POST':
        cert.category = request.form['category']
        cert.title = request.form['title']
        cert.platform = request.form['platform']
        cert.date = request.form['date']
        cert.image = request.form['image']
        cert.url = request.form['url']
        db.session.commit()
        return redirect(url_for('certifications.add_certification'))
    return render_template('edit_certification.html', certification=cert)

@certifications.route('/delete_certification/<int:cert_id>')
def delete_certification(cert_id):
    cert = Certification.query.get(cert_id)
    if cert:
        db.session.delete(cert)
        db.session.commit()
    return redirect(url_for('certifications.add_certification'))

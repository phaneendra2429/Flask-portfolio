import re
from urllib.parse import urlparse

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from models import db, ResumeSetting

admin = Blueprint('admin', __name__, url_prefix='/admin')

GOOGLE_DRIVE_FILE_PATH = re.compile(r'^/file/d/([A-Za-z0-9_-]+)(?:/.*)?$')


def normalize_google_drive_resume_url(value):
    """Validate a public Drive file link and return its canonical preview URL."""
    parsed = urlparse(value.strip())
    if parsed.scheme != 'https' or parsed.hostname not in {'drive.google.com', 'www.drive.google.com'}:
        return None

    match = GOOGLE_DRIVE_FILE_PATH.fullmatch(parsed.path)
    if not match:
        return None

    return f'https://drive.google.com/file/d/{match.group(1)}/view'

@admin.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')


@admin.route('/resume', methods=['GET', 'POST'])
@login_required
def resume():
    setting = db.session.get(ResumeSetting, 1)

    if request.method == 'POST':
        resume_url = normalize_google_drive_resume_url(request.form.get('resume_url', ''))
        if not resume_url:
            flash('Enter a valid HTTPS Google Drive file link.', 'danger')
            return render_template(
                'admin/resume.html',
                resume_url=setting.resume_url if setting else None,
                submitted_url=request.form.get('resume_url', ''),
            )

        if setting is None:
            setting = ResumeSetting(id=1, resume_url=resume_url)
            db.session.add(setting)
        else:
            setting.resume_url = resume_url

        db.session.commit()
        flash('Resume link updated successfully.', 'success')
        return redirect(url_for('admin.resume'))

    return render_template(
        'admin/resume.html',
        resume_url=setting.resume_url if setting else None,
        submitted_url=setting.resume_url if setting else '',
    )

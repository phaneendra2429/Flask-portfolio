from flask import Flask, render_template
from flask_login import LoginManager

from models import ResumeSetting, User, db
from migrate_resume import migrate_resume
from routes.admin import admin
from routes.auth import auth


VALID_URL = 'https://drive.google.com/file/d/abc_123-XYZ/view?usp=sharing'
CANONICAL_URL = 'https://drive.google.com/file/d/abc_123-XYZ/view'


def _make_test_app(database_path):
    test_app = Flask(__name__, template_folder='templates')
    test_app.config.update(
        TESTING=True,
        SECRET_KEY='test-secret',
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{database_path}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    db.init_app(test_app)

    login_manager = LoginManager(test_app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    test_app.register_blueprint(auth)
    test_app.register_blueprint(admin)
    test_app.add_url_rule('/', endpoint='index', view_func=lambda: '')

    with test_app.app_context():
        User.__table__.create(bind=db.engine, checkfirst=True)
        ResumeSetting.__table__.create(bind=db.engine, checkfirst=True)

    return test_app


def test_resume_page_requires_login(tmp_path):
    test_app = _make_test_app(tmp_path / 'resume.db')
    client = test_app.test_client()
    response = client.get('/admin/resume')
    assert response.status_code == 302
    assert '/login?next=%2Fadmin%2Fresume' in response.headers['Location']


def test_admin_can_update_only_valid_drive_urls(tmp_path):
    test_app = _make_test_app(tmp_path / 'resume.db')
    with test_app.app_context():
        user = User(username='admin')
        user.set_password('password')
        db.session.add_all([user, ResumeSetting(id=1, resume_url=CANONICAL_URL)])
        db.session.commit()

    client = test_app.test_client()
    client.post('/login', data={'username': 'admin', 'password': 'password'})

    response = client.post('/admin/resume', data={'resume_url': VALID_URL}, follow_redirects=True)
    assert b'Resume link updated successfully.' in response.data
    with test_app.app_context():
        assert db.session.get(ResumeSetting, 1).resume_url == CANONICAL_URL

    response = client.post('/admin/resume', data={'resume_url': 'http://example.com/resume.pdf'})
    assert b'Enter a valid HTTPS Google Drive file link.' in response.data
    with test_app.app_context():
        assert db.session.get(ResumeSetting, 1).resume_url == CANONICAL_URL


def test_public_templates_use_the_configured_drive_resume_url(tmp_path):
    test_app = _make_test_app(tmp_path / 'resume.db')
    with test_app.app_context():
        db.session.add(ResumeSetting(id=1, resume_url=CANONICAL_URL))
        db.session.commit()

        with test_app.test_request_context('/'):
            index_html = render_template(
                'index.html',
                projects=[],
                recommendations=[],
                skills_data={},
                certifications={'professional': [], 'courses': []},
                resume_url=CANONICAL_URL,
            )
            events_html = render_template(
                'events.html', in_person=[], online=[], resume_url=CANONICAL_URL
            )

    for html in (index_html, events_html):
        assert f'href="{CANONICAL_URL}"' in html
        assert 'target="_blank"' in html
        assert 'rel="noopener"' in html
        assert 'Phaneendra_G.pdf' not in html


def test_resume_migration_creates_an_empty_settings_table(tmp_path):
    test_app = _make_test_app(tmp_path / 'resume.db')
    with test_app.app_context():
        ResumeSetting.__table__.drop(bind=db.engine)

    migrate_resume(test_app)
    with test_app.app_context():
        assert db.session.get(ResumeSetting, 1) is None
        db.session.add(ResumeSetting(id=1, resume_url=CANONICAL_URL))
        db.session.commit()

    migrate_resume(test_app)
    with test_app.app_context():
        assert db.session.get(ResumeSetting, 1).resume_url == CANONICAL_URL

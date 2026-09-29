# Flask Portfolio

A simple, extensible portfolio website built with Flask. It renders content from JSON files, includes lightweight admin-style pages to add/edit content (projects, events, skills, certifications), and ships with a Dockerfile and GitHub Actions workflow for CI/CD and container publishing.

## Features

- Dynamic pages powered by JSON content
- Admin-style forms to add/edit data without a database
- Clean Bootstrap UI with responsive components
- Events listing with in-person/online sections
- Project filtering via AJAX endpoint
- Dockerized app for easy deployment
- CI/CD via GitHub Actions with DockerHub push

## Tech Stack

- Backend: `Flask`, `Jinja2`
- Frontend: `Bootstrap 5`, Font Awesome
- Data: JSON files under `templates/json`
- Container: `Docker`
- CI/CD: GitHub Actions → build/test/push image

## Project Structure

```
flask-project/
├─ app.py                     # Flask app + blueprint registration
├─ routes/                    # Feature blueprints
│  ├─ projects.py             # Add/Edit projects
│  ├─ events.py               # Events page + CRUD
│  ├─ recommendations.py      # Add recommendations
│  ├─ skills.py               # Add skills by category
│  └─ certifications.py       # Add/Edit/Delete certifications
├─ templates/                 # Jinja templates + JSON content store
│  ├─ index.html              # Landing page
│  ├─ events.html             # Events listing page
│  ├─ add_*.html, edit_*.html # Simple admin pages
│  └─ json/
│     ├─ cards_data.json          # Projects
│     ├─ events.json              # Events
│     ├─ recommendations.json     # Testimonials
│     ├─ skills.json              # Skills by category
│     └─ certifications.json      # Certifications grouped by category
├─ static/
│  ├─ css/*.css
│  ├─ js/*.js
│  └─ timeline.png
├─ .github/workflows/cicd.yml # CI: tests + Docker build/push
├─ DockerFile                 # Container image definition
├─ requirements.txt
├─ test_app.py                # Minimal pytest
└─ LICENSE
```

## Getting Started (Local)

Prerequisites: Python 3.9+ (Dockerfile uses 3.12), `pip`.

1) Create a virtual environment and install dependencies

```
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

2) Run the app

```
python app.py
# or
set FLASK_APP=app.py && flask run  # Windows
# FLASK_APP=app.py flask run        # macOS/Linux
```

App runs on http://127.0.0.1:5000.

## Run with Docker

Build and run the container:

```
docker build -t portfolio-flask . -f DockerFile
docker run --rm -p 5000:5000 portfolio-flask
```

The container runs `flask run` bound to `0.0.0.0:5000`.

## Content Model

This project intentionally avoids a database. Content is stored in JSON files under `templates/json`. Admin routes write to these files directly. Commit changes to persist them in version control.

- Projects: `templates/json/cards_data.json`
- Events: `templates/json/events.json`
- Skills: `templates/json/skills.json`
- Recommendations: `templates/json/recommendations.json`
- Certifications: `templates/json/certifications.json` (grouped categories)

## Routes Overview

- `GET /` — Home page, renders projects, recommendations, skills, certifications
- `POST /filter_projects` — JSON body `{ "category": "..." }` → returns filtered projects by label

Admin-style pages (basic forms writing to JSON):

- Projects
  - `GET,POST /add_project`
  - `GET,POST /edit_project/<int:project_index>`

- Events
  - `GET /events` — Public events listing
  - `GET,POST /add_event`
  - `GET,POST /edit_event/<int:index>`
  - `GET /delete_event/<int:index>`

- Skills
  - `GET,POST /add_skill`

- Recommendations
  - `GET,POST /add_recommendation`

- Certifications
  - `GET,POST /add_certification`
  - `GET,POST /edit_certification/<category>/<int:index>`
  - `GET /delete_certification/<category>/<int:index>`

Notes:
- Labels for projects are arrays, e.g., `["ML", "Docker", ...]`. The filter endpoint matches a provided label.
- Certification JSON is keyed by category (e.g., `professional`, `courses`).

## Development Tips

- Templates live in `templates/` and use Bootstrap 5.
- Static assets live in `static/`. The public resume is a Google Drive link stored in the database.

### Resume setup

The resume is managed from **Admin Dashboard → Resume** and must be a public Google Drive file link (for example, `https://drive.google.com/file/d/FILE_ID/view`). The Docker container runs `migrate_resume.py` automatically after PostgreSQL is ready. The script only creates the resume settings table; add the first public link from the dashboard after deployment. It is safe on every deployment and never overwrites an admin-updated link.

For a manual run, execute the script only inside the deployed web container (or another environment whose `DATABASE_URL` points to the production PostgreSQL server). Running it on your Windows machine without a local PostgreSQL server will try `localhost:5432` and fail.
- When editing JSON directly, ensure valid JSON formatting. The admin forms will write pretty-printed JSON with `indent=4`.

## Testing

Run the test suite with pytest:

```
pytest -q
```

The repository includes a placeholder test. Add more tests as you extend functionality.

## CI/CD

The GitHub Actions workflow at `.github/workflows/cicd.yml`:

- Checks out code and runs `pytest`
- Builds a Docker image using `DockerFile`
- Pushes the image to DockerHub tag `latest`

Required GitHub secrets:

- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`

There is also a commented section showing an example EC2 deployment step via SSH that pulls and runs the latest image.

## Deployment Notes

- Docker: Map a public port to container `5000` and front it with a reverse proxy (optional). Example:
  - `docker run -d --name portfolio -p 80:5000 youruser/portfolio-flaskapp:latest`
- Gunicorn (optional): You can run via Gunicorn inside the container by adjusting the CMD, e.g., `gunicorn -b 0.0.0.0:5000 app:app`.
- Render/Cloud: Use the Docker image produced by the workflow or build from the `DockerFile` directly.

## License

This project is licensed under the terms specified in `LICENSE`.

## Acknowledgements

- Built with Flask and Bootstrap
- Icons via Font Awesome CDN

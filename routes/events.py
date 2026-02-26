from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from models import db, Event

events = Blueprint('events', __name__)

@events.route('/events')
def events_view():
    events_list = Event.query.all()
    in_person = [e for e in events_list if e.mode == "in_person"][::-1]
    online = [e for e in events_list if e.mode == "online"][::-1]
    return render_template('events.html', in_person=in_person, online=online)

@events.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    if request.method == 'POST':
        new_event = Event(
            title=request.form["title"],
            description=request.form["description"],
            tags=[t.strip() for t in request.form["tags"].split(",")],
            image_url=request.form["image_url"],
            post_url=request.form["post_url"],
            mode=request.form["mode"],
        )
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for("events.add_event"))
    
    events_list = Event.query.order_by(Event.id.desc()).all()
    return render_template("add_event.html", events=events_list)

@events.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        event.title = request.form["title"]
        event.description = request.form["description"]
        event.tags = [t.strip() for t in request.form["tags"].split(",")]
        event.image_url = request.form["image_url"]
        event.post_url = request.form["post_url"]
        event.mode = request.form["mode"]
        db.session.commit()
        return redirect(url_for("events.add_event"))
    return render_template("edit_event.html", event=event)

@events.route('/delete_event/<int:event_id>')
@login_required
def delete_event(event_id):
    event = Event.query.get(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
    return redirect(url_for("events.add_event"))

from flask import Blueprint, render_template, request, redirect, url_for
import json

events = Blueprint('events', __name__)
events_file = "templates/json/events.json"

def load_json(file):
    with open(file, "r") as f: return json.load(f)

def save_to_json(data, file):
    with open(file, "w") as f: json.dump(data, f, indent=4)

@events.route('/events')
def events_view():
    events_data = load_json(events_file)
    in_person = [e for e in events_data if e.get("mode") == "in_person"][::-1]
    online = [e for e in events_data if e.get("mode") == "online"][::-1]
    return render_template('events.html', in_person=in_person, online=online)

@events.route('/add_event', methods=['GET', 'POST'])
def add_event():
    events_data = load_json(events_file)
    if request.method == 'POST':
        new_event = {
            "title": request.form["title"],
            "description": request.form["description"],
            "tags": [t.strip() for t in request.form["tags"].split(",")],
            "image_url": request.form["image_url"],
            "post_url": request.form["post_url"],
            "mode": request.form["mode"],
        }
        events_data.append(new_event)
        save_to_json(events_data, events_file)
        return redirect(url_for("events.add_event"))
    # Pass reversed list but preserve original indices for edit/delete operations
    events_with_idx = []
    for idx, item in enumerate(events_data):
        copy = dict(item)
        copy["_idx"] = idx
        events_with_idx.append(copy)
    events_with_idx.reverse()
    return render_template("add_event.html", events=events_with_idx)

@events.route('/edit_event/<int:index>', methods=['GET', 'POST'])
def edit_event(index):
    events_data = load_json(events_file)
    if index < 0 or index >= len(events_data):
        return redirect(url_for("events.add_event"))
    if request.method == 'POST':
        updated = {
            "title": request.form["title"],
            "description": request.form["description"],
            "tags": [t.strip() for t in request.form["tags"].split(",")],
            "image_url": request.form["image_url"],
            "post_url": request.form["post_url"],
            "mode": request.form["mode"],
        }
        events_data[index] = updated
        save_to_json(events_data, events_file)
        return redirect(url_for("events.add_event"))
    return render_template("edit_event.html", event=events_data[index])

@events.route('/delete_event/<int:index>')
def delete_event(index):
    events_data = load_json(events_file)
    if 0 <= index < len(events_data):
        del events_data[index]
        save_to_json(events_data, events_file)
    return redirect(url_for("events.add_event"))

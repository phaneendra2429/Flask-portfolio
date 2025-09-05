from flask import Blueprint, render_template, request, redirect, url_for
import json

certifications = Blueprint('certifications', __name__)
certifications_file = "templates/json/certifications.json"

def load_json(file): 
    with open(file, "r") as f: return json.load(f)

def save_to_json(data, file): 
    with open(file, "w") as f: json.dump(data, f, indent=4)

@certifications.route('/add_certification', methods=['GET', 'POST'])
def add_certification():
    data = load_json(certifications_file)
    if request.method == 'POST':
        cat = request.form['category']
        new_cert = {
            "title": request.form['title'],
            "platform": request.form['platform'],
            "date": request.form['date'],
            "image": request.form['image'],
            "url": request.form['url']
        }
        data.setdefault(cat, []).append(new_cert)
        save_to_json(data, certifications_file)
        return redirect(url_for('certifications.add_certification'))
    # Build flattened list with original indices for edit/delete
    all_certs = []
    for category, items in data.items():
        for idx, item in enumerate(items):
            entry = dict(item)
            entry['_category'] = category
            entry['_idx'] = idx
            all_certs.append(entry)
    # Show newest first within each category while preserving indices
    all_certs.sort(key=lambda x: (x['_category'], x['_idx']), reverse=True)
    return render_template('add_certification.html', certifications=all_certs)

@certifications.route('/edit_certification/<category>/<int:index>', methods=['GET', 'POST'])
def edit_certification(category, index):
    data = load_json(certifications_file)
    if category not in data or not (0 <= index < len(data[category])):
        return redirect(url_for('certifications.add_certification'))
    if request.method == 'POST':
        new_cat = request.form['category']
        existing = data[category][index]
        updated = dict(existing)
        updated.update({
            "title": request.form['title'],
            "platform": request.form['platform'],
            "date": request.form['date'],
            "image": request.form['image'],
            "url": request.form['url']
        })
        if new_cat == category:
            data[category][index] = updated
        else:
            # Move to a different category
            del data[category][index]
            data.setdefault(new_cat, []).append(updated)
        save_to_json(data, certifications_file)
        return redirect(url_for('certifications.add_certification'))
    cert = data[category][index]
    return render_template('edit_certification.html', certification=cert, category=category, index=index)

@certifications.route('/delete_certification/<category>/<int:index>')
def delete_certification(category, index):
    data = load_json(certifications_file)
    if category in data and 0 <= index < len(data[category]):
        del data[category][index]
        save_to_json(data, certifications_file)
    return redirect(url_for('certifications.add_certification'))

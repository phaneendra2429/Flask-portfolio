from flask import Blueprint, render_template, request, redirect, url_for
import json
import uuid

recommend = Blueprint('recommend', __name__)
recommendations_file = "templates/json/recommendations.json"

def load_json(file): 
    try:
        with open(file, "r") as f: 
            data = json.load(f)
            # Ensure all items have an ID (migration step)
            modified = False
            for item in data:
                if 'id' not in item:
                    item['id'] = str(uuid.uuid4())
                    modified = True
            if modified:
                save_to_json(data, file)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_to_json(data, file): 
    with open(file, "w") as f: json.dump(data, f, indent=4)

@recommend.route('/add_recommendation', methods=['GET', 'POST'])
def add_recommendation():
    data = load_json(recommendations_file)
    
    if request.method == 'POST':
        rec_id = request.form.get('id')
        
        if rec_id:
            # Edit existing
            for rec in data:
                if rec.get('id') == rec_id:
                    rec['name'] = request.form['name']
                    rec['title'] = request.form['title']
                    rec['recommendation'] = request.form['recommendation']
                    rec['date'] = request.form['date']
                    rec['image'] = request.form['image']
                    break
        else:
            # Add new
            new_rec = {
                "id": str(uuid.uuid4()),
                "name": request.form['name'],
                "title": request.form['title'],
                "recommendation": request.form['recommendation'],
                "date": request.form['date'],
                "image": request.form['image']
            }
            data.append(new_rec)
            
        save_to_json(data, recommendations_file)
        return redirect('/add_recommendation')
        
    return render_template('add_rec.html', recommendations=data)

@recommend.route('/delete_recommendation/<string:rec_id>')
def delete_recommendation(rec_id):
    data = load_json(recommendations_file)
    data = [rec for rec in data if rec.get('id') != rec_id]
    save_to_json(data, recommendations_file)
    return redirect('/add_recommendation')

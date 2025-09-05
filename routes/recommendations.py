from flask import Blueprint, render_template, request, redirect
import json

recommend = Blueprint('recommend', __name__)
recommendations_file = "templates/json/recommendations.json"

def load_json(file): 
    with open(file, "r") as f: return json.load(f)

def save_to_json(data, file): 
    with open(file, "w") as f: json.dump(data, f, indent=4)

@recommend.route('/add_recommendation', methods=['GET', 'POST'])
def add_recommendation():
    if request.method == 'POST':
        new_rec = {
            "name": request.form['name'],
            "title": request.form['title'],
            "recommendation": request.form['recommendation'],
            "date": request.form['date'],
            "image": request.form['image']
        }
        data = load_json(recommendations_file)
        data.append(new_rec)
        save_to_json(data, recommendations_file)
        return redirect('/')
    return render_template('add_rec.html')

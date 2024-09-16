from flask import Flask, render_template, jsonify, request, redirect, url_for
import json

app = Flask(__name__)

projects = "cards_data.json"
recommendation = "recommendations.json"

# Load projects from cards_data.json
# with open('cards_data.json', 'r') as f:
#     projects_data = json.load(f)

# Load JSON content
def load_json(recommendation):
    with open(recommendation, "r") as f:
        return json.load(f)

# Save data to JSON file
def save_to_json(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)
    

projects_data = load_json(projects)
recommendations = load_json(recommendation)

@app.route('/')
def index():
    # Load all projects by default
    return render_template('index.html', projects=projects_data, recommendations = recommendations)

@app.route('/filter_projects', methods=['POST'])
def filter_projects():
    category = request.json['category']
    filtered_projects = [project for project in projects_data if category in project['labels']]
    
    return jsonify(filtered_projects)


# Adding Project
@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        labels = request.form['labels'].split(',')
        image_placeholder = request.form['image']

        new_project = {
            "title": title,
            "description": description,
            "labels": labels,
            "image_placeholder": image_placeholder
        }

        projects_data.append(new_project)

        # Update the cards_data.json file
        with open('cards_data.json', 'w') as f:
            json.dump(projects_data, f, indent=4)

        return redirect(url_for('index'))
    return render_template('add_project.html')



# Adding Recommendation
@app.route('/add-recommendation', methods=['GET', 'POST'])
def add_recommendation():
    if request.method == 'POST':
        # Get form data
        new_rec = {
            "name": request.form['name'],
            "title": request.form['title'],
            "recommendation": request.form['recommendation'],
            "date": request.form['date'],
            "image": request.form['image']
        }

        # Load existing recommendations and add the new one
        data = load_json()
        data.append(new_rec)
        save_to_json(data, projects)

        return redirect('/')
    
    return render_template('add_rec.html')

if __name__ == '__main__':
    app.run(debug=True)

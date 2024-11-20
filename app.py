from flask import Flask, render_template, jsonify, request, redirect, url_for
import json

app = Flask(__name__)

# Load data from JSON files
def load_json(file):
    with open(file, "r") as f:
        return json.load(f)

# Save data to JSON files
def save_to_json(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# Define file paths for each JSON file
projects_file = "templates/json/cards_data.json"
recommendations_file = "templates/json/recommendations.json"
events_file = "templates/json/events.json"  
skills = "templates/json/skills.json"

# Load existing JSON data
# projects_data = load_json(projects_file)
# recommendations = load_json(recommendations_file)
# events_data = load_json(events_file)  # Corrected to use events_file


@app.route('/')
def index():
    # Load all projects, recommendations, and events by default
    projects_data = load_json(projects_file)
    recommendations = load_json(recommendations_file)
    skills_data = load_json(skills) 
    return render_template('index.html', projects=projects_data, recommendations=recommendations, skills_data=skills_data)

@app.route('/filter_projects', methods=['POST'])
def filter_projects():
    projects_data = load_json(projects_file)
    category = request.json['category']
    filtered_projects = [project for project in projects_data if category in project['labels']]
    return jsonify(filtered_projects)

# New route for events page
@app.route('/events')
def events():
    events_data = load_json(events_file)
    return render_template('events.html', events=events_data)

# New route for adding an event
@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    events_data = load_json(events_file)
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        tags = request.form["tags"].split(",")
        image_url = request.form["image_url"]
        post_url = request.form["post_url"]

        # Add the new event to events_data and save
        new_event = {
            "title": title,
            "description": description,
            "tags": tags,
            "image_url": image_url,
            "post_url": post_url
        }
        events_data.append(new_event)
        save_to_json(events_data, events_file)  # Corrected to save to events_file
        
        return redirect(url_for("events"))

    return render_template("add_event.html")


# Adding Project
@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    projects_data = load_json(projects_file)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        labels = request.form['labels'].split(',')
        image_placeholder = request.form['image']
        github = request.form['github']  

        new_project = {
            "title": title,
            "description": description,
            "labels": labels,
            "image_placeholder": image_placeholder,
            "github": github
        }

        projects_data.append(new_project)

        # Update the cards_data.json file
        save_to_json(projects_data, projects_file)  # Corrected to save to projects_file

        return redirect(url_for('index'))
    return render_template('add_project.html', projects=projects_data)

@app.route('/edit_project/<int:project_index>', methods=['GET', 'POST'])
def edit_project(project_index):
    projects_data = load_json(projects_file)
    project = projects_data[project_index]

    if request.method == 'POST':
        project['title'] = request.form['title']
        project['description'] = request.form['description']
        project['labels'] = request.form['labels'].split(',')
        project['image_placeholder'] = request.form['image']
        project['github'] = request.form['github']

        save_to_json(projects_data, projects_file)
        return redirect(url_for('add_project'))

    return render_template('edit_project.html', project=project, project_index=project_index)

# Adding Recommendation
@app.route('/add_recommendation', methods=['GET', 'POST'])
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
        data = load_json(recommendations_file)
        data.append(new_rec)
        save_to_json(data, recommendations_file)

        return redirect('/')
    
    return render_template('add_rec.html')

@app.route('/add_skill', methods=['GET', 'POST'])
def add_skill():
    if request.method == 'POST':
        category = request.form['category']
        topics = request.form['topics'].split(',')

        skills_data = load_json(skills)
        if category in skills_data:
            skills_data[category].extend(topics)
        else:
            skills_data[category] = topics

        save_to_json(skills_data, skills )
        return redirect(url_for('index'))
    return render_template('add_skills.html')

if __name__ == '__main__':
    app.run(debug=True)

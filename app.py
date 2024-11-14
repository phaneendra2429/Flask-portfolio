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
events_file = "templates/json/events.json"  # Define the path for events.json

# Load existing JSON data
projects_data = load_json(projects_file)
recommendations = load_json(recommendations_file)
events_data = load_json(events_file)  # Corrected to use events_file

@app.route('/')
def index():
    # Load all projects, recommendations, and events by default
    return render_template('index.html', projects=projects_data, recommendations=recommendations)

@app.route('/filter_projects', methods=['POST'])
def filter_projects():
    category = request.json['category']
    filtered_projects = [project for project in projects_data if category in project['labels']]
    return jsonify(filtered_projects)

# New route for events page
@app.route('/events')
def events():
    print("Accessing the events page")  # Debug statement
    print(events_data)  # Print the events data to verify it's loaded
    return render_template('events.html', events=events_data)

# New route for adding an event
@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        tags = request.form["tags"].split(",")
        image_url = request.form["image_url"]

        # Add the new event to events_data and save
        new_event = {
            "title": title,
            "description": description,
            "tags": tags,
            "image_url": image_url
        }
        events_data.append(new_event)
        save_to_json(events_data, events_file)  # Corrected to save to events_file
        
        return redirect(url_for("events"))

    return render_template("add_event.html")


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
        data = load_json()
        data.append(new_rec)
        save_to_json(data, projects)

        return redirect('/')
    
    return render_template('add_rec.html')

if __name__ == '__main__':
    app.run(debug=True)

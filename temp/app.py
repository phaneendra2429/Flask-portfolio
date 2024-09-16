from flask import Flask, render_template, request, redirect, jsonify
import json

app = Flask(__name__)
# Path to the JSON file
recommendation = "recommendations.json"

# Load JSON content
def load_json(recommendation):
    with open(recommendation, "r") as f:
        return json.load(f)

# Save data to JSON file
def save_to_json(data):
    with open(recommendation, "w") as f:
        json.dump(data, f, indent=4)

recommendations = load_json(recommendation)

class Recommendation:
    
    @app.route('/')
    def index():
        # recommendations = load_json()
        return render_template('index.html', recommendations=recommendations)

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
            save_to_json(data)

            return redirect('/')
        
        return render_template('add_rec.html')

if __name__ == '__main__':
    app.run(debug=True)

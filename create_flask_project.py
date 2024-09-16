import os

# Define the directory structure
project_structure = {
    'static': {
        'css': ['style.css', 'styles2.css'],
        'js': ['prjpages.js', 'prjpagesinsert.js', 'projects.js']
    },
    'templates': ['index.html', 'project.html'],
    'app.py': None
}

# Function to create directories and files
def create_file_structure(root_dir, structure):
    for item, value in structure.items():
        path = os.path.join(root_dir, item)
        if isinstance(value, dict):
            os.makedirs(path)
            create_file_structure(path, value)
        elif isinstance(value, list):
            os.makedirs(path)
            for file in value:
                open(os.path.join(path, file), 'a').close()  # Create empty files
        elif value is None:
            open(path, 'a').close()  # Create empty file

# Main function to create the project structure
def create_project_structure(root_dir):
    os.makedirs(root_dir)
    create_file_structure(root_dir, project_structure)

# Usage
if __name__ == "__main__":
    project_root = 'your_project'
    create_project_structure(project_root)
    print(f"Generated project structure in '{project_root}' successfully.")

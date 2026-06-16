from flask import Flask, send_from_directory
from pathlib import Path

PROJECTS_DIR = Path("projects")
PROJECTS_DIR.mkdir(exist_ok=True)

print(PROJECTS_DIR.resolve())

app = Flask(__name__)

# Helpers

def get_projects() :
    projects = []
    for item in PROJECTS_DIR.iterdir() :
        if item.is_dir() :
            projects.append(item.name)
    return projects

def clickable_projects() :
    projects = get_projects()
    string = ""
    for project in projects :
        string += f'<li><a href="/projects/{project}">{project}</a></li>\n'
    return string

def get_categories(project_name) :
    project_path = PROJECTS_DIR / project_name
    categories = []
    for item in project_path.iterdir() :
        if item.is_dir() :
            categories.append(item.name)
    return categories

def clickable_categories(project_name) :
    categories = get_categories(project_name)
    string = ""
    for category in categories :
        string += f'<li><a href="/projects/{project_name}/{category}">{category}</a></li>\n'
    return string

def get_subcategories(project_name, category) :
    category_path = PROJECTS_DIR / project_name / category
    subcategories = []
    for item in category_path.iterdir() :
        if item.is_dir() :
            subcategories.append(item.name)
    return subcategories

def clickable_subcategories(project_name, category) :
    subcategories = get_subcategories(project_name, category)
    string = ""
    for subcategory in subcategories :
        string += f'<li><a href="/projects/{project_name}/{category}/{subcategory}">{subcategory}</a></li>\n'
    return string

def get_images(project_name, category, subcategory) :
    image_path = PROJECTS_DIR / project_name / category / subcategory
    images = []
    for item in image_path.iterdir() :
        if item.is_file() :
            images.append(item.name)
    return images

def clickable_images(project_name, category, subcategory) :
    images = get_images(project_name, category, subcategory)
    string = ""
    for image in images :
        string += f"""
            <li>
                <img src="/files/{project_name}/{category}/{subcategory}/{image}" width="200">
                <p>{image}</p>
            </li>
            """
    return string

# Routes

@app.route("/files/<path:filename>")
def files(filename) :
    return send_from_directory(PROJECTS_DIR, filename)

@app.route("/")
def home() :
    projects = get_projects()
    return f"""
        <h1>The Cap Safe</h1>
        <ul>
            {clickable_projects()}
        </ul>
        """

@app.route("/projects/<project_name>")
def view_project(project_name) :
    return f"""
        <h1>{project_name}</h1>
        <h2>Categories</h2>
        <ul>
            {clickable_categories(project_name)}
        </ul>
        <p><a href="/">Home</a></p>
        """

@app.route("/projects/<project_name>/<category>")
def view_category(project_name, category) :
    return f"""
        <h1>{project_name} / {category}</h1>
        <h2>Subcategories</h2>
        <ul>
            {clickable_subcategories(project_name, category)}
        </ul>
        <p><a href="/projects/{project_name}">Back to project</a></p>
        <p><a href="/">Home</a></p>
        """

@app.route("/projects/<project_name>/<category>/<subcategory>")
def view_subcategory(project_name, category, subcategory) :
    return f"""
        <h1>{project_name} / {category} / {subcategory}</h1>
        <ul>
            {clickable_images(project_name, category, subcategory)}
        </ul>
        <p><a href="/projects/{project_name}/{category}">Back to category</a></p>
        <p><a href="/">Home</a></p>
        """

# Run

if __name__ == "__main__" :
    app.run(debug=True)
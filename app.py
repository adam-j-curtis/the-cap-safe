from flask import Flask, send_from_directory, request, redirect
from pathlib import Path

PROJECTS_DIR = Path("projects")
PROJECTS_DIR.mkdir(exist_ok=True)
IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
    ".bmp"
}

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

def get_census(project_name) :
    project_path = PROJECTS_DIR / project_name
    file_count = 0
    image_count = 0
    caption_file_count = 0
    pass
#Split into several fxs?

def display_census(project_name) :
    pass

def get_folders(project_name, folder_path="") :
    current_path = PROJECTS_DIR / project_name / folder_path
    folders = []
    for item in current_path.iterdir() :
        if item.is_dir() :
            folders.append(item.name)
    return folders

def clickable_folders(project_name, folder_path="") :
    folders = get_folders(project_name, folder_path)
    string = ""
    for folder in folders :
        if folder_path :
            link_path = f"{folder_path}/{folder}"
        else :
            link_path = folder
        string += f'<li><a href="/projects/{project_name}/{link_path}">{folder}</a></li>\n'
    return string

# def get_categories(project_name) :
#     project_path = PROJECTS_DIR / project_name
#     categories = []
#     for item in project_path.iterdir() :
#         if item.is_dir() :
#             categories.append(item.name)
#     return categories

# def clickable_categories(project_name) :
#     categories = get_categories(project_name)
#     string = ""
#     for category in categories :
#         string += f'<li><a href="/projects/{project_name}/{category}">{category}</a></li>\n'
#     return string

# def get_subcategories(project_name, category) :
#     category_path = PROJECTS_DIR / project_name / category
#     subcategories = []
#     for item in category_path.iterdir() :
#         if item.is_dir() :
#             subcategories.append(item.name)
#     return subcategories

# def clickable_subcategories(project_name, category) :
#     subcategories = get_subcategories(project_name, category)
#     string = ""
#     for subcategory in subcategories :
#         string += f'<li><a href="/projects/{project_name}/{category}/{subcategory}">{subcategory}</a></li>\n'
#     return string

def get_images(project_name, folder_path="") :
    image_path = PROJECTS_DIR / project_name / folder_path
    images = []
    for item in image_path.iterdir() :
        if item.is_file() :
            images.append(item.name)
    return images

def clickable_images(project_name, folder_path="") :
    images = get_images(project_name, folder_path)
    string = ""
    for image in images :
        string += f"""
            <li>
                <a href="/projects/{project_name}/{folder_path}/{image}">
                    <img src="/files/{project_name}/{folder_path}/{image}" width="200">
                </a>
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
        <h2>Projects</h2>
        <ul>
            {clickable_projects()}
        </ul>
        <form action="/create_project" method="post">
            <input name="project_name" placeholder="New project name">
            <button type="submit">Create Project</button>
        </form>
        """

@app.route("/create_project", methods=["POST"])
def create_project() :
    project_name = request.form["project_name"]
    project_path = PROJECTS_DIR / project_name
    project_path.mkdir(exist_ok=True)
    return redirect("/")

@app.route("/projects/<project_name>")
def view_project(project_name) :
    return f"""
        <h1>{project_name}</h1>
        <h2>Primary Category Folders</h2>
        <ul>
            {clickable_folders(project_name)}
        </ul>
        <form action="/create_folder/{project_name}" method="post">
            <input name="folder_name" placeholder="New folder name">
            <button type="submit">Create Folder</button>
        </form>
        <h2>Folder Census</h2>
        <p>Total images: </p>
        <p>Total caption files: </p>
        <p>[Folder names]: </p>
        <h2>Caption Census</h2>
        <p>[Caption name]: </p>
        <p>[Percentage of total images]: </p>
        <h3>Navigate</h3>
        <p><a href="/">Home</a></p>
        """
        # Folder names compiled into a list, displayed, and tabulated per name.
        # Compile list of captions using all caption files, increment the census count of each caption per occurrence.

@app.route("/create_folder/<project_name>", methods=["POST"])
def create_top_folder(project_name) :
    folder_name = request.form["folder_name"]
    new_folder_path = PROJECTS_DIR / project_name / folder_name
    new_folder_path.mkdir(exist_ok=True)
    return redirect(f"/projects/{project_name}")

@app.route("/create_folder/<project_name>/<path:folder_path>", methods=["POST"])
def create_folder(project_name, folder_path="") :
    folder_name = request.form["folder_name"]
    new_folder_path = PROJECTS_DIR / project_name / folder_path / folder_name
    new_folder_path.mkdir(exist_ok=True)
    return redirect(f"/projects/{project_name}/{folder_path}")

@app.route("/projects/<project_name>/<path:folder_path>")
def view_folder(project_name, folder_path) :
    
    images = get_images(project_name, folder_path)
    if images :
        image_section = f"""
            <h2>Images</h2>
            <ul>
                {clickable_images(project_name, folder_path)}
            </ul>
        """
    else :
        image_section = ""
    
    return f"""
        <h1>{project_name} / {folder_path}</h1>
        <h2>Subfolders</h2>
        <ul>
            {clickable_folders(project_name, folder_path)}
        </ul>
        {image_section}
        <form action="/create_folder/{project_name}/{folder_path}" method="post">
            <input name="folder_name" placeholder="New folder name">
            <button type="submit">Create Folder</button>
        </form>
        <p><a href="/projects/{project_name}">Back to project</a></p>
        <p><a href="/">Home</a></p>
        """
        # Add back-one-level link

# @app.route("/create_subcategory/<project_name>/<category>", methods=["POST"])
# def create_subcategory(project_name, category) :
#     subcategory_name = request.form["subcategory_name"]
#     subcategory_path = PROJECTS_DIR / project_name / category / subcategory_name
#     subcategory_path.mkdir(exist_ok=True)
#     return redirect(f"/projects/{project_name}/{category}")

# @app.route("/projects/<project_name>/<category>/<subcategory>")
# def view_subcategory(project_name, category, subcategory) :
#     return f"""
#         <h1>{project_name} / {category} / {subcategory}</h1>
#         <ul>
#             {clickable_images(project_name, category, subcategory)}
#         </ul>
#         <p><a href="/projects/{project_name}/{category}">Back to category</a></p>
#         <p><a href="/">Home</a></p>
#         """

# @app.route("/projects/<project_name>/<folder_path>/<image>")
# def view_image(project_name, folder_path, image) :
#     return f"""
#         <h1>{image}</h1>
#         <a href="/projects/{project_name}/{folder_path}">
#             <img src="/files/{project_name}/{folder_path}/{image}" style="max-width: 95%; height: auto;">
#         </a>
#         <p><a href="/projects/{project_name}/{folder_path}">Back to thumbnails</a></p>
#         <p><a href="/">Home</a></p>
#         """

# Run

if __name__ == "__main__" :
    app.run(debug=True)
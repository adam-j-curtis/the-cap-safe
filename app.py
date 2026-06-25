from flask import Flask, send_from_directory, request, redirect
from pathlib import Path
from project_utils import (
    PROJECTS_DIR,
    get_projects,
    clickable_projects,
    get_folders,
    clickable_folders,
    get_images,
    clickable_images,
    get_folder_state,
    get_census,
    display_census
)

print(PROJECTS_DIR.resolve())

app = Flask(__name__)

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
    state = get_folder_state(project_name)
    census = get_census(project_name)
    if state == "mixed" :
        warning = """
            <h3>Warning: This folder contains both subfolders and non-folders, which can cause unexpected app behavior.</h3>
            <p>Please move all non-folder files to a leaf folder or empty folder in the project; or move all folders to an empty or branch folder in the project.</p>
            """
    else :
        warning = ""
    return f"""
        <h1>{project_name}</h1>
        <p><a href="/">Home</a></p>
        <h2>Primary Category Folders</h2>
            {warning}
        <ul>
            {clickable_folders(project_name)}
        </ul>
        <form action="/create_folder/{project_name}" method="post">
            <input name="folder_name" placeholder="New folder name">
            <button type="submit">Create Folder</button>
        </form>
        <h2>Folder Census</h2>
        <p>Total images: {census["image_count"]}</p>
        <p>Total caption files: {census["caption_file_count"]}</p>
        <details>
            <summary>Show Folder Counts</summary>
            <ul>
                {display_census(census["folder_counts"], census["level_image_count"])}
            </ul>
        </details>
        <h2>Caption Census</h2>
        <p>[Caption name]: </p>
        <p>[Percentage of total images]: </p>        
        """
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
        
    path = f"<h1>{project_name} / {folder_path}</h1>"
    folder_section = f"""
        <h2>Subfolders</h2>
        <ul>
            {clickable_folders(project_name, folder_path)}
        </ul>
        """
    image_section = f"""
        <h2>Images</h2>
        <ul>
            {clickable_images(project_name, folder_path)}
        </ul>
        """
    folder_creation = f"""
        <form action="/create_folder/{project_name}/{folder_path}" method="post"> 
        <input name="folder_name" placeholder="New folder name">
        <button type="submit">Create Folder</button>
        </form>
        """
    path_object = Path(folder_path)
    if path_object.parent == Path(".") :
        back_one_link = f"""
            <p><a href="/projects/{project_name}">Back one step</a></p>
            """
    else :
        back_one_link = f"""
            <p><a href="/projects/{project_name}/{path_object.parent}">Back one step</a></p>
            """
    links = f"""
        {back_one_link}
        <p><a href=\"/projects/{project_name}\">Back to project</a></p>
        <p><a href=\"/\">Home</a></p>
        """

    state = get_folder_state(project_name, folder_path)    
    if state == "empty" :
        return f"""
            {path}
            {links}
            <h2>This folder is empty.</h2>
            {folder_creation}
        """
        # Allow image adding later, which will turn off folder creation
    elif state == "branch" :
        return f"""
            {path}
            {links}
            {folder_section}
            {folder_creation}
            """
    elif state == "leaf" :
        return f"""
            {path}
            {links}
            {image_section}
            """
    elif state == "mixed" :
        return f"""
            {path}
            {links}
            <h3>Warning: This folder contains both subfolders and non-folders, which can cause unexpected app behavior.</h3>
            <p>Please move all non-folder files to a leaf folder or empty folder in the project; or move all folders to an empty or branch folder in the project.</p>
            {folder_section}
            {image_section}
            {folder_creation}
            """

@app.route("/image/<project_name>/<path:image_path>")
def view_image(project_name, image_path) :
    path = Path(image_path)
    folder_path = path.parent
    image = path.name
    return f"""
        <h1>{image}</h1>
        <a href="/projects/{project_name}/{folder_path}">
            <img src="/files/{project_name}/{image_path}" style="max-width: 95%; height: auto;">
        </a>
        <p><a href="/projects/{project_name}/{folder_path}">Back to thumbnails</a></p>
        <p><a href="/">Home</a></p>
        """

# Run

if __name__ == "__main__" :
    app.run(debug=True)
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

def get_images(project_name, folder_path="") :
    image_path = PROJECTS_DIR / project_name / folder_path
    images = []
    for item in image_path.iterdir() :
        if item.is_file() and item.suffix.lower() in IMAGE_EXTENSIONS :
            images.append(item.name)
    return images

def clickable_images(project_name, folder_path="") :
    images = get_images(project_name, folder_path)
    string = ""
    for image in images :
        image_path = f"{folder_path}/{image}"
        string += f"""
            <li>
                <a href="/image/{project_name}/{image_path}">
                    <img src="/files/{project_name}/{image_path}" width="200">
                </a>
                <p>{image}</p>
            </li>
            """
    return string

def get_folder_state(project_name, folder_path="") :
    folders = get_folders(project_name, folder_path)
    images = get_images(project_name, folder_path)
    if folders and images :
        return "mixed"
    elif folders :
        return "branch"
    elif images :
        return "leaf"
    else :
        return "empty"
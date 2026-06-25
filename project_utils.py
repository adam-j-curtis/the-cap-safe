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
    
def get_census(project_name) :
    project_path = PROJECTS_DIR / project_name
    image_count = 0
    caption_file_count = 0
    folder_counts = {}
    level_image_count = {}

    for item in project_path.rglob("*") :

        if item.is_file() and item.suffix.lower() in IMAGE_EXTENSIONS :
            image_count += 1
            relative_folder = item.parent.relative_to(project_path)
            for level, folder_name in enumerate(relative_folder.parts) :
                if level not in level_image_count :
                    level_image_count[level] = 0
                level_image_count[level] += 1
                if level not in folder_counts :
                    folder_counts[level] = {}
                if folder_name not in folder_counts[level] :
                    folder_counts[level][folder_name] = 0
                folder_counts[level][folder_name] += 1

        
        elif item.is_file() and item.suffix.lower() == ".txt" :
            caption_file_count += 1
    
    return {
        "image_count" : image_count,
        "caption_file_count" : caption_file_count,
        "folder_counts" : folder_counts,
        "level_image_count" : level_image_count
    }

def display_census(folder_counts, level_image_count) :
    string = ""
    for level in folder_counts :
        if level == 0 :
            string += "<h3>Top level:</h3>"
        else :
            string += f"<h3>Level {level + 1}:</h3>"
        for folder_name, count in folder_counts[level].items() :
            percent = count / level_image_count[level] * 100
            string += f"<li>{folder_name} : {count} ({percent:.1f}%)</li>"
    return string
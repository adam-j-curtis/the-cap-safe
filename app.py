from flask import Flask
from pathlib import Path

PROJECTS_DIR = Path("projects")
PROJECTS_DIR.mkdir(exist_ok=True)

print(PROJECTS_DIR.resolve())

app = Flask(__name__)

def get_projects() :
    projects = []
    for item in PROJECTS_DIR.iterdir() :
        if item.is_dir() :
            projects.append(item.name)
    return projects

@app.route("/")
def home() :
    projects = get_projects()
    return f"""
    <h1>The Cap Safe</h1>
    <p>{projects}</p>
    """

if __name__ == "__main__" :
    app.run(debug=True)


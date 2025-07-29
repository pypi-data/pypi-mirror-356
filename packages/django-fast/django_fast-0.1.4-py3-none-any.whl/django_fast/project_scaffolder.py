import shutil
from pathlib import Path

def create_project():
    current_dir = Path.cwd()
    project_name = input("Project name: ")
    destination = current_dir / project_name
    template_path = Path(__file__).parent / "templates" / "project_template"
    shutil.copytree(template_path, destination)
    print(f"Project '{project_name}' created.")

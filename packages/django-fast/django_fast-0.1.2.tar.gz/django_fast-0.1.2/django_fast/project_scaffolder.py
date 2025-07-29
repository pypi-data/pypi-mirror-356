# project_scaffolder.py
import shutil
from pathlib import Path

def create_project():
    current_dir = Path.cwd()
    project_name = input("Project name: ")
    destination = current_dir / project_name
    shutil.copytree("myframework/templates/project_template", destination)
    print(f"Project '{project_name}' created.")

import shutil
from pathlib import Path
import importlib.resources as resources  # Python 3.9+

def create_project():
    from django_fast import templates  # 👈 import your package's submodule
    
    project_name = input("Project name: ")
    destination = Path.cwd() / project_name

    # Use resources to safely locate package data
    with resources.path("django_fast.templates", "project_template") as template_dir:
        shutil.copytree(template_dir, destination)

    print(f"✅ Project '{project_name}' created at {destination}")

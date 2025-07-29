# cli.py
import argparse
from .core import app

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command")

subparsers.add_parser("startproject")
subparsers.add_parser("runserver")

args = parser.parse_args()

if args.command == "startproject":
    from .project_scaffolder import create_project
    create_project()
elif args.command == "runserver":
    import uvicorn
    uvicorn.run("main:app", reload=True)
elif args.command in ["makemigrations", "migrate", "shell"]:
    import subprocess
    subprocess.run(["python", "manage.py", args.command])
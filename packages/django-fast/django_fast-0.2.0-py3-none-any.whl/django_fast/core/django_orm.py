# core/django_orm.py
import django
import os

def setup_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_fast.templates.project_template.settings")
    django.setup()

# core/django_orm.py
import django
import os

def setup_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    django.setup()

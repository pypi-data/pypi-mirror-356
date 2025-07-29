SECRET_KEY = "change-me"
DEBUG = True
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "app",  # Your models go here
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

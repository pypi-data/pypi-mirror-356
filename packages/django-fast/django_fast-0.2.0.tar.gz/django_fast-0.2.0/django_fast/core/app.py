# core/app.py
from .router import Router
from .django_orm import setup_django

setup_django()

class App:
    def __call__(self, scope, receive, send):
        return Router.handle(scope, receive, send)

app = App()

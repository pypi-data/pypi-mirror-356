# core/app.py
from core.router import Router
from core.django_orm import setup_django

setup_django()

class App:
    def __call__(self, scope, receive, send):
        return Router.handle(scope, receive, send)

app = App()

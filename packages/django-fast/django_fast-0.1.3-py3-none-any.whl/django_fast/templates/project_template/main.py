from core.router import Router

@Router.route("/", method="GET")
def index(request):
    return {"message": "Hello from your django-fast!"}

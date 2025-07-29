# core/router.py

routes = []

class Router:
    @staticmethod
    def route(path: str, method: str = "GET"):
        def decorator(func):
            routes.append({
                "path": path,
                "method": method.upper(),
                "handler": func
            })
            return func
        return decorator

    @staticmethod
    async def handle(scope, receive, send):
        if scope["type"] != "http":
            return

        path = scope["path"]
        method = scope["method"].upper()

        for route in routes:
            if route["path"] == path and route["method"] == method:
                response_data = route["handler"](scope)
                from core.response import JSONResponse
                await JSONResponse(response_data)(scope, receive, send)
                return

        from core.response import JSONResponse
        await JSONResponse({"error": "Not found"}, status=404)(scope, receive, send)

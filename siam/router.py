ROUTES = dict()


def process(event):
    path, method, params = _event_info(event)
    return ROUTES[path][method](
        **params
    )


def route(path, methods):
    def _route(f):
        path_route = ROUTES.pop(path, dict())

        for method in methods:
            path_route[method] = f

        ROUTES[path] = path_route

    return _route


def get(path):
    return route(path, methods=("GET",))


def post(path):
    return route(path, methods=("POST",))


def put(path):
    return route(path, methods=("PUT",))


def delete(path):
    return route(path, methods=("DELETE",))


def _event_info(event):
    return (
        event["path"],
        event["httpMethod"],
        event["pathParameters"]
    )
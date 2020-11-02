import re

ROUTES = dict()


def process(event):
    path, op, params, query_string = _event_info(event)

    for path_regex, routes in ROUTES.items():
        if path_regex.match(path):
            f = routes[op]
            params = _get_typed_params(f, params, query_string)
            return f(**params)

    raise Exception(f"No routes found for {op} {path}")


def route(path, methods):
    def _route(f):
        path_regex = _path_regex(path)
        routes = ROUTES.pop(path_regex, dict())

        for op in methods:
            routes[op] = f

        ROUTES[path_regex] = routes

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
        event["pathParameters"],
        event["queryStringParameters"]
    )


URL_REGEX = re.compile("{([^{}]*)?}")


def _path_regex(path):
    regex, idx = "", 0
    for match in URL_REGEX.finditer(path):
        regex += f"{path[idx: match.start()]}([^{{}}]*)"
        idx = match.end()
    regex += path[idx:-1]
    return re.compile(regex)


def _get_typed_params(f, params, query_string):
    return {
        k: f.__annotations__.get(k, str)(v)
        for k, v in dict(**params.copy(), **query_string)
    }

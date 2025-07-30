import os
import base64
import json
import requests

from flask import jsonify, request, Flask
from typing import List, Dict

from vitessestack_common.router import RouteDefinition


def retrieve_authorized_from_header(headers: dict):
    result = {}

    authorized_data: str = headers.get("Authorizedata")

    if authorized_data:
        del headers["Authorizedata"]

        authorized_data_encoded = [
            attribute.encode() for attribute in authorized_data.split(",")
        ]

        tmps = []

        for attr in authorized_data_encoded:
            key_path = base64.b64decode(attr).decode().split(".")

            tmp = key_path[-1]

            for item in reversed(key_path[:-1]):
                tmp = {item: tmp}

            tmps.append(tmp)

        for d in tmps:
            first_key = list(d.keys())[0]
            nested_data = d[first_key]
            result.update(nested_data)

    return result


def mock_lambda_event(
    path: str, method: str, path_params: dict = {}, include_body: bool = False
):
    headers = dict(request.headers)
    authorized_data = retrieve_authorized_from_header(headers)

    event = {
        "resource": path,
        "path": path,
        "httpMethod": method,
        "pathParameters": path_params,
        "headers": headers,
        "body": json.dumps(request.json) if include_body else "{}",
        **authorized_data,
    }

    return event


def response_body(raw_response: dict):
    """
    Returns json formatted body response.
    """
    raw_response["body"] = json.loads(raw_response["body"])

    return raw_response


def lambda_response(response):
    """
    Returns response body with status code as correct API response.
    """
    response = response_body(response)

    return jsonify(response.get("body", "{}")), response.get("statusCode", 500)


def get_authorizer_data_temporal_headers(authorizer_data: dict = {}):
    headers = {}
    keys = []

    def recurse(data: dict, path: str):
        for key, value in data.items():
            key_path = f"{path}.{key}"

            if isinstance(value, dict):
                recurse(value, key_path)
            else:
                keys.append(
                    base64.b64encode(f"{key_path}.{str(value)}".encode()).decode()
                )

    recurse(authorizer_data, "authorizer_data")

    if len(keys):
        headers["authorizedata"] = ",".join(keys)

    return headers


def make_request(
    host: str,
    method: str,
    path: str,
    body: dict = {},
    headers: dict = {},
    authorizer_data: dict = {},
):
    response = requests.request(
        method=method,
        url=f"{host}{path}",
        data=json.dumps(body),
        headers={**headers, **get_authorizer_data_temporal_headers(authorizer_data)},
    )

    return response.content.decode(), response.status_code


def gateway_signature():
    path = f"/{'/'.join(request.path.split('/')[2:])}"

    request_signature = {
        "method": request.method,
        "path": path,
        "body": {},
        "headers": {},
    }

    request_signature["headers"] = dict(request.headers)

    try:
        request_signature["body"] = request.json
    except Exception as e:
        print("No body on requests")

    return request_signature


def gateway_routes(app: Flask, routes: Dict[str, str], methods: List[str]):
    def wrapper(func):
        for id, route in routes.items():
            app.add_url_rule(route, id, view_func=func, methods=methods)

    return wrapper


class Test:
    routes: Dict[str, List[str]]

    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 5001,
        handler: callable = None,
        debug: bool = True,
    ):
        self.app = Flask(__file__)
        self.host = host
        self.port = port
        self.handler = handler
        self.debug = debug

        self.routes = dict()

    def add_route(self, path: str, method: str):
        if path not in self.routes:
            self.routes[path] = list()

        self.routes[path].append(method)

    def create_endpoints(self):
        for path, methods in self.routes.items():

            def temporal_method():
                url = request.path
                method = request.method
                with_body = method in ["POST", "PUT"]

                response = (
                    self.handler(mock_lambda_event(url, method, include_body=with_body))
                    if self.handler
                    else {}
                )

                return lambda_response(response)

            self.app.add_url_rule(
                path, methods=methods, view_func=temporal_method, endpoint=path
            )

    def add_from_routes(self, routes_path: str = "routes.json"):
        def add_single_route(route: RouteDefinition, path: str = str()):
            url = path + route.resource
            self.add_route(path=url, method=route.method)

            for child in route.children:
                add_single_route(child, path=url)

        if os.path.exists(routes_path):
            with open(routes_path, "r") as f:
                routes = json.loads(f.read())
                for route in routes:
                    route = RouteDefinition.parse_obj(route)
                    add_single_route(route)

    def run(self):
        self.create_endpoints()
        self.app.run(host=self.host, port=self.port, debug=self.debug)

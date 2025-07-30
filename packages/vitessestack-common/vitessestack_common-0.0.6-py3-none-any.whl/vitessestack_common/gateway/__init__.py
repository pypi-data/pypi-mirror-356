from dotenv import load_dotenv
from typing import List

load_dotenv()

from flask import Flask, make_response
from flask_cors import CORS
from uuid import uuid4

from vitessestack_common.test import (
    make_request,
    gateway_signature,
    gateway_routes,
    Test,
)
from utils import check_authorization


class Gateway:
    def __init__(self, api_tests: List[Test], authorizer_url: str):
        self.app = Flask(__file__)
        CORS(self.app)

        self.authorizer_url = authorizer_url

        for api in api_tests:
            self.set_api(api)

    def set_api(self, test: Test):
        routes, methods = dict(), set()

        def get_id():
            id = str(uuid4())

            while id in routes:
                id = str(uuid4())

            return id

        for path, path_methods in test.routes:
            routes[get_id()] = path
            methods = methods.union(path_methods)

        @gateway_routes(app=self.app, routes=routes, methods=list(methods))
        @check_authorization(self.authorizer_url)
        def temporal_method(authorizer_data: dict = {}, *args, **kwargs):
            response_body, response_status = make_request(
                host=f"{test.host}:{test.port}",
                **gateway_signature(),
                authorizer_data=authorizer_data,
            )

            response = make_response(response_body)
            response.status_code = response_status

            response.headers["Content-Type"] = "application/json"

            return response

    def run(self, host: str, port: int, debug: bool):
        self.app.run(host=host, port=port, debug=debug)

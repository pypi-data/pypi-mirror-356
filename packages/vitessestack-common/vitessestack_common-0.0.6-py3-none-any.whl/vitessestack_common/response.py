import json

from pydantic import BaseModel, BaseSettings
from enum import Enum

from vitessestack_common.utils import empty_method


class Settings(BaseSettings):
    cors_headers_origin: str = ""
    cors_headers_methods: str = ""
    cors_headers_headers: str = ""
    cors_headers_credentials: str = ""


class APIResponse(BaseModel):
    headers: dict
    body: str
    statusCode: int


class APIResponseType(Enum):
    JSON = "application/json"


class APIResponseHandler:
    def __init__(self, body: dict, status: int = None, headers: dict = {}):
        self.body = body
        self.status = status
        self.headers = headers
        self.settings = Settings()

    def __add_cors_headers(self):
        cors_headers = [
            (self.settings.cors_headers_origin, "Access-Control-Allow-Origin"),
            (self.settings.cors_headers_methods, "Access-Control-Allow-Methods"),
            (self.settings.cors_headers_headers, "Access-Control-Allow-Headers"),
            (
                self.settings.cors_headers_credentials,
                "Access-Control-Allow-Credentials",
            ),
        ]

        for value, title in cors_headers:
            if value:
                self.headers[title] = value

    def get_headers(self):
        self.__add_cors_headers()
        return self.headers

    def get_general(self, body: str) -> dict:
        status = self.status if self.status is not None else (200 if body else 500)

        return APIResponse(
            statusCode=status, body=body, headers=self.get_headers()
        ).dict()

    def _get_json(self):
        body = json.dumps(self.body if self.body is not None else {})
        self.headers["Content-Type"] = APIResponseType.JSON.value

        return self.get_general(body)

    def get(self, response_type: APIResponseType):
        options = {APIResponseType.JSON: self._get_json}

        return options.get(response_type, empty_method)()


__all__ = ["APIResponseHandler", "APIResponseType"]

import json
from pydantic import BaseModel
from typing import Any, List, Optional
from enum import Enum

from vitessestack_common.router import Router
from vitessestack_common.utils import get_token_payload


TOKEN_USER_ID_KEY = "user_id"


class EventItem(Enum):
    PATH = "path"
    RESOURCE = "resource"
    BODY = "pbody"
    HEADERS = "headers"
    METHOD = "httpMethod"
    PATH_PARAMS = "pathParameters"


class Event(BaseModel):
    path: str = ""
    resource: str = ""
    body: Optional[str] = "{}"
    headers: dict = {}
    httpMethod: str
    pathParameters: Optional[dict] = {}
    requestContext: Optional[dict]

    @property
    def pbody(self):
        result = {}
        try:
            result = json.loads(self.body or "{}")
        except Exception as e:
            pass

        return result


class AuthedEvent(Event):
    @property
    def token(self):
        header_value = ""

        token_header_name_alternatives = [
            "authorization",
            "Authorization",
            "AUTHORIZATION",
        ]
        for alternative in token_header_name_alternatives:
            if not header_value:
                authorization_value = self.headers.get(alternative, " ")
                _, token = authorization_value.split(" ")

                if token:
                    header_value = token

        return header_value

    @property
    def token_payload(self):
        return get_token_payload(self.token)

    @property
    def client_id(self):
        result = self.token_payload.get(TOKEN_USER_ID_KEY, "")

        to_client = (
            (self.requestContext.get("authorizer", {}).get("replace_client"))
            if self.requestContext
            else None
        )

        if to_client:
            result = to_client

        return result

    @classmethod
    def client_from_adhoc(cls, token: str):
        payload = get_token_payload(token)
        return payload.get(TOKEN_USER_ID_KEY, "")

    @staticmethod
    def token_from_adhoc(headers: dict):
        header_value = ""

        token_header_name_alternatives = [
            "authorization",
            "Authorization",
            "AUTHORIZATION",
        ]
        for alternative in token_header_name_alternatives:
            if not header_value:
                authorization_value = headers.get(alternative, " ")
                _, token = authorization_value.split(" ")

                if token:
                    header_value = token

        return header_value


class EventHandler:
    def __init__(self, event: dict, *args, logging: bool = False, **kwargs):
        self.raw = event
        self.router = None

        if logging:
            self.log_event()

        self.set()

    def log_event(self):
        print("EVENT", self.raw)

    def set(self):
        self.data = AuthedEvent(**self.raw)

    def create_router(
        self, definition_json: str = None, definition_methods: Any = None
    ):
        self.router = Router()

        if definition_json and definition_methods:
            self.router.add_from_json(
                definition_string=definition_json, methods_module=definition_methods
            )

    def run_router(self, included_from_event: List[EventItem] = []):
        result = None
        if self.router:
            data_dict = self.data.dict()
            fields = {
                item.value: data_dict.get(item.value) for item in included_from_event
            }
            result = self.router.run(
                **self.data.pbody,
                resource=self.data.resource,
                httpMethod=self.data.httpMethod,
                pathParameters=self.data.pathParameters,
                **fields,
                client_id=self.data.client_id,
            )

        return result

    @classmethod
    def handle(csl, logging: bool = False):
        def handler_wrapper(func):
            def wrapper(*args, **kwargs):
                return func(event=csl(*args, logging=logging, **kwargs))

            return wrapper

        return handler_wrapper


__all__ = ["EventHandler", "EventItem", "AuthedEvent"]

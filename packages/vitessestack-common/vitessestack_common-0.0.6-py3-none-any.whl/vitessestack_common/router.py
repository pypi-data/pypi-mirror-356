from __future__ import annotations
from typing import Any, List, Optional, Dict, Callable, ForwardRef
from pydantic import BaseModel

import json
from vitessestack_common.utils import empty_method


RouteDefinition = ForwardRef("RouteDefinition")


class RouteDefinition(BaseModel):
    resource: str
    method: str
    action: str
    children: Optional[List[RouteDefinition]]


RouteDefinition.update_forward_refs()


class Router:
    def __init__(self):
        self.routes: Dict[str, Dict[str, Callable]] = {}

    def add_route(self, path: str, method: str, action: callable, args: List[str] = []):
        if path not in self.routes:
            self.routes[path] = {}

        self.routes[path][method] = action

    def add_definition_route(
        self, definition: RouteDefinition, methods_module: Any, path: str = str()
    ):
        url = path + definition.resource

        self.add_route(
            url,
            definition.method,
            getattr(methods_module, definition.action, empty_method),
        )
        if definition.children:
            for child in definition.children:
                self.add_definition_route(child, methods_module, path=url)

    def add_from_json(self, definition_string: str, methods_module: Any):
        definition_dict: List[dict] = json.loads(definition_string)

        for ind in definition_dict:
            self.add_definition_route(RouteDefinition.parse_obj(ind), methods_module)

    def run(
        self, resource: str, httpMethod: str, pathParameters: dict = {}, *args, **kwargs
    ):
        route_action = self.routes.get(resource, {}).get(httpMethod, empty_method)
        return route_action(*args, **{**(pathParameters or {}), **kwargs})


__all__ = ["Router"]

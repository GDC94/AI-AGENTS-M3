"""Routing: decide which Area resolves a Query."""

from orchestration.routing.route import Route, RouteTarget
from orchestration.routing.router import ROUTER_PROMPT, build_router

__all__ = ["ROUTER_PROMPT", "Route", "RouteTarget", "build_router"]

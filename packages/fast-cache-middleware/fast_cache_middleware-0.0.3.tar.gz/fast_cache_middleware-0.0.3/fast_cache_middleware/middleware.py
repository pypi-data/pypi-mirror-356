import copy
import inspect
import logging
import typing as tp
import cachetools

from fastapi import FastAPI, routing
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Mount, get_route_path
from starlette.types import ASGIApp, Receive, Scope, Send

from .controller import Controller
from .depends import BaseCacheConfigDepends, CacheConfig, CacheDropConfig
from .schemas import RouteInfo
from .storages import BaseStorage, InMemoryStorage

logger = logging.getLogger(__name__)


def get_app_routes(app: FastAPI) -> tp.List[routing.APIRoute]:
    """Gets all routes from FastAPI application.

    Recursively traverses all application routers and collects their routes.

    Args:
        app: FastAPI application

    Returns:
        List of all application routes
    """
    routes = []

    # Get routes from main application router
    routes.extend(get_routes(app.router))

    # Traverse all nested routers
    for route in app.router.routes:
        if isinstance(route, Mount):
            if isinstance(route.app, routing.APIRouter):
                routes.extend(get_routes(route.app))

    return routes


def get_routes(router: routing.APIRouter) -> list[routing.APIRoute]:
    """Recursively gets all routes from router.

    Traverses all routes in router and its sub-routers, collecting them into a single list.

    Args:
        router: APIRouter to traverse

    Returns:
        List of all routes from router and its sub-routers
    """
    routes = []

    # Get all routes from current router
    for route in router.routes:
        if isinstance(route, routing.APIRoute):
            routes.append(route)
        elif isinstance(route, Mount):
            # Recursively traverse sub-routers
            if isinstance(route.app, routing.APIRouter):
                routes.extend(get_routes(route.app))

    return routes


async def send_with_callbacks(
    app: ASGIApp,
    scope: Scope,
    receive: Receive,
    send: Send,
    on_response_ready: tp.Callable[[Response], tp.Awaitable[None]] | None = None,
) -> None:
    response_holder: tp.Dict[str, tp.Any] = {}

    async def response_builder(message: tp.Dict[str, tp.Any]) -> None:
        """Wrapper for intercepting and saving response."""
        if message["type"] == "http.response.start":
            response_holder["status"] = message["status"]

            message.get("headers", []).append(
                ("X-Cache-Status".encode(), "MISS".encode())
            )
            response_holder["headers"] = [
                (k.decode(), v.decode()) for k, v in message.get("headers", [])
            ]

            response_holder["body"] = b""
        elif message["type"] == "http.response.body":
            body = message.get("body", b"")
            response_holder["body"] += body

            # If this is the last chunk, cache the response
            if not message.get("more_body", False):
                response = Response(
                    content=response_holder["body"],
                    status_code=response_holder["status"],
                    headers=dict(response_holder["headers"]),
                )

                # Call callback with ready response
                if on_response_ready:
                    await on_response_ready(response)

        # Pass event further
        await send(message)

    await app(scope, receive, response_builder)


def _build_scope_hash_key(scope: Scope) -> str:
    path = get_route_path(scope)
    method = scope["method"].upper()
    return f"{path}/{method}"


class FastCacheMiddleware:
    """Middleware for caching responses in ASGI applications.

    Route resolution approach:
    1. Analyzes all routes and their dependencies at startup
    2. Finds corresponding route by path and method on request
    3. Extracts cache configuration from route dependencies
    4. Performs standard caching/invalidation logic

    Advantages:
    - Pre-route analysis - fast configuration lookup
    - Support for all FastAPI dependencies
    - Flexible cache management at route level
    - Efficient cache invalidation

    Args:
        app: ASGI application to wrap
        storage: Cache storage (default InMemoryStorage)
        controller: Controller for managing caching logic
    """

    def __init__(
        self,
        app: ASGIApp,
        storage: tp.Optional[BaseStorage] = None,
        controller: tp.Optional[Controller] = None,
    ) -> None:
        self.app = app
        self.storage = storage or InMemoryStorage()
        self.controller = controller or Controller()

        self._routes_info: list[RouteInfo] = []

    def _extract_routes_info(self, routes: list[routing.APIRoute]) -> list[RouteInfo]:
        """Recursively extracts route information and their dependencies.

        Args:
            routes: List of routes to analyze
        """
        routes_info = []
        for route in routes:
            (
                cache_config,
                cache_drop_config,
            ) = self._extract_cache_configs_from_route(route)

            if cache_config or cache_drop_config:
                route_info = RouteInfo(
                    route=route,
                    cache_config=cache_config,
                    cache_drop_config=cache_drop_config,
                )
                routes_info.append(route_info)

        return routes_info

    def _extract_cache_configs_from_route(
        self, route: routing.APIRoute
    ) -> tp.Tuple[CacheConfig | None, CacheDropConfig | None]:
        """Extracts cache configurations from route dependencies.

        Args:
            route: Route to analyze

        Returns:
            Tuple with CacheConfig and CacheDropConfig (if found)
        """
        cache_config = None
        cache_drop_config = None

        endpoint = getattr(route, "endpoint", None)
        if not endpoint:
            return None, None

        # Analyze dependencies if they exist
        for dependency in getattr(route, "dependencies", []):
            if isinstance(dependency, BaseCacheConfigDepends):
                # need to make a copy, as dependency can be destroyed
                dependency = copy.deepcopy(dependency)
                if isinstance(dependency, CacheConfig):
                    cache_config = dependency
                elif isinstance(dependency, CacheDropConfig):
                    cache_drop_config = dependency
                continue

        return cache_config, cache_drop_config

    @cachetools.cached(
        cache=cachetools.LRUCache(maxsize=10**3),
        key=lambda _, request, __: _build_scope_hash_key(request.scope),
    )
    def _find_matching_route(
        self, request: Request, routes_info: list[RouteInfo]
    ) -> tp.Optional[RouteInfo]:
        """Finds route matching the request.

        Args:
            request: HTTP request

        Returns:
            RouteInfo if matching route found, otherwise None
        """
        for route_info in routes_info:
            if request.method not in route_info.methods:
                continue
            match_mode, _ = route_info.route.matches(request.scope)
            if match_mode == routing.Match.FULL:
                return route_info

        return

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        if not self._routes_info:
            app_routes = get_app_routes(scope["app"])
            self._routes_info = self._extract_routes_info(app_routes)

        request = Request(scope, receive)

        # Find matching route
        route_info = self._find_matching_route(request, self._routes_info)
        if not route_info:
            await self.app(scope, receive, send)
            return

        # Handle invalidation if specified
        if cc := route_info.cache_drop_config:
            await self.controller.invalidate_cache(cc, storage=self.storage)

        # Handle caching if config exists
        if route_info.cache_config:
            await self._handle_cache_request(route_info, request, scope, receive, send)
            return

        # Execute original request
        await self.app(scope, receive, send)

    async def _handle_cache_request(
        self,
        route_info: RouteInfo,
        request: Request,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        """Handles request with caching.

        Args:
            route_info: Route information
            request: HTTP request
            scope: ASGI scope
            receive: ASGI receive callable
            send: ASGI send callable
        """
        cache_config = route_info.cache_config
        if not cache_config:
            await self.app(scope, receive, send)
            return

        if not await self.controller.is_cachable_request(request):
            await self.app(scope, receive, send)
            return

        cache_key = await self.controller.generate_cache_key(request, cache_config)

        cached_response = await self.controller.get_cached_response(
            cache_key, self.storage
        )
        if cached_response is not None:
            logger.debug("Returning cached response for key: %s", cache_key)
            await cached_response(scope, receive, send)
            return

        # Cache not found - execute request and cache result
        await send_with_callbacks(
            self.app,
            scope,
            receive,
            send,
            lambda response: self.controller.cache_response(
                cache_key, request, response, self.storage, cache_config.max_age
            ),
        )

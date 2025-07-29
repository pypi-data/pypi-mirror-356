import re
import typing as tp

from fastapi import params
from starlette.requests import Request


class BaseCacheConfigDepends(params.Depends):
    """Base class for cache configuration via ASGI scope extensions.

    Uses standardized ASGI extensions mechanism for passing
    configuration from route dependencies to middleware.
    """

    use_cache: bool = True

    def __call__(self, request: Request) -> None:
        """Saves configuration in ASGI scope extensions.

        Args:
            request: HTTP request
        """
        # Use standard ASGI extensions mechanism
        if "extensions" not in request.scope:
            request.scope["extensions"] = {}

        if "fast_cache" not in request.scope["extensions"]:
            request.scope["extensions"]["fast_cache"] = {}

        request.scope["extensions"]["fast_cache"]["config"] = self

    @property
    def dependency(self) -> params.Depends:
        return self


class CacheConfig(BaseCacheConfigDepends):
    """Cache configuration for route.

    Args:
        max_age: Cache lifetime in seconds
        key_func: Cache key generation function
    """

    def __init__(
        self,
        max_age: int = 5 * 60,
        key_func: tp.Optional[tp.Callable[[Request], str]] = None,
    ) -> None:
        self.max_age = max_age
        self.key_func = key_func


class CacheDropConfig(BaseCacheConfigDepends):
    """Cache invalidation configuration for route.

    Args:
        paths: Path for cache invalidation. Can be string or regular expression.
            If string, it will be converted to regular expression
            that matches the beginning of request path.
    """

    def __init__(self, paths: list[str | re.Pattern]) -> None:
        self.paths: list[re.Pattern] = [
            p if isinstance(p, re.Pattern) else re.compile(f"^{p}") for p in paths
        ]

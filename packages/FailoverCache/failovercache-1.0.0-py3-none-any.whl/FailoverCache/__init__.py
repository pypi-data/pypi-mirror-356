import inspect
from typing import Awaitable, Callable, Optional, TypeVar, Union

from diskcache import Cache as DiskCache
from redis import Redis

T = TypeVar("T")


class FailoverCache:
    def __init__(
        self,
        redis_host: str = "127.0.0.1",
        redis_port: int = 6379,
        diskcache_directory: str = ".cache",
    ):
        try:
            r = Redis(host=redis_host, port=redis_port)
            r.ping()
            self.redis = r
        except Exception:
            print("Redis not available. Redis Cache is disabled.")
            self.redis = None
        self.diskcache = DiskCache(diskcache_directory)

    def get(self, key: str) -> Optional[str]:
        if isinstance(self.redis, Redis):
            try:
                value = self.redis.get(key)
                if value is not None:
                    return value.decode() if isinstance(value, bytes) else str(value)
                return None
            except Exception:
                pass

        value = self.diskcache.get(key)
        if value is not None:
            return value.decode() if isinstance(value, bytes) else str(value)
        return None

    def put(self, key: str, value: str, ttl: int = 60) -> None:
        if isinstance(self.redis, Redis):
            try:
                self.redis.setex(key, ttl, value)
            except Exception:
                pass

        self.diskcache.set(key, value, ttl)

    def has(self, key: str) -> bool:
        if isinstance(self.redis, Redis):
            try:
                if self.redis.exists(key):
                    return True
            except Exception:
                pass

        return key in self.diskcache

    def forget(self, key: str) -> None:
        if isinstance(self.redis, Redis):
            try:
                self.redis.delete(key)
            except Exception:
                pass
        self.diskcache.pop(key)

    def pull(self, key: str) -> Optional[str]:
        value = self.get(key)
        self.forget(key)
        return value

    async def remember(
        self, key: str, callback: Callable[[], Union[T, Awaitable[T]]], ttl: int = 60
    ) -> T:
        value = self.get(key)
        if value is not None:
            return value

        result = callback()
        if inspect.isawaitable(result):
            result = await result

        self.put(key, result, ttl)
        return result

    def flush(self) -> None:
        if isinstance(self.redis, Redis):
            try:
                self.redis.flushdb()
            except Exception:
                pass
        self.diskcache.clear()

    def extend_ttl(self, key: str, seconds: int) -> None:
        if isinstance(self.redis, Redis):
            try:
                current_ttl = self.redis.ttl(key)
                if current_ttl > 0:
                    self.redis.expire(key, current_ttl + seconds)
            except Exception:
                pass

        try:
            current_ttl = self.diskcache.ttl(key)
            if current_ttl is not None:
                self.diskcache.touch(key, expire=current_ttl + seconds, retry=True)
        except Exception:
            pass

    def set_ttl(self, key: str, ttl: int) -> None:
        if isinstance(self.redis, Redis):
            try:
                self.redis.expire(key, ttl)
            except Exception:
                pass

        try:
            self.diskcache.touch(key, expire=ttl, retry=True)
        except Exception:
            pass

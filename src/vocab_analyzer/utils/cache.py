"""
Caching utilities for vocab-analyzer.
"""
from functools import lru_cache, wraps
from typing import Any, Callable, Optional


def cached_property(func: Callable) -> property:
    """
    Decorator to cache property values.

    Similar to functools.cached_property (Python 3.8+) but with explicit implementation.

    Args:
        func: Property getter function

    Returns:
        Property with cached value

    Example:
        >>> class MyClass:
        ...     @cached_property
        ...     def expensive_operation(self):
        ...         return compute_something()
    """
    attr_name = f"_cached_{func.__name__}"

    @wraps(func)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)

    return property(wrapper)


def memoize(maxsize: int = 128):
    """
    Memoization decorator using lru_cache.

    This is essentially an alias for functools.lru_cache with a friendly name.

    Args:
        maxsize: Maximum cache size (default: 128)

    Returns:
        Decorated function with caching

    Example:
        >>> @memoize(maxsize=256)
        ... def expensive_function(arg):
        ...     return compute_result(arg)
    """

    def decorator(func: Callable) -> Callable:
        return lru_cache(maxsize=maxsize)(func)

    return decorator


class SimpleCache:
    """
    Simple in-memory cache for storing key-value pairs.

    Useful for caching vocabulary lookups, phrase matches, etc.
    """

    def __init__(self, maxsize: Optional[int] = None):
        """
        Initialize cache.

        Args:
            maxsize: Maximum number of items to cache (None = unlimited)
        """
        self._cache: dict = {}
        self._maxsize = maxsize
        self._hits = 0
        self._misses = 0

    def get(self, key: Any, default: Any = None) -> Any:
        """
        Get value from cache.

        Args:
            key: Cache key
            default: Default value if key not found

        Returns:
            Cached value or default
        """
        if key in self._cache:
            self._hits += 1
            return self._cache[key]
        else:
            self._misses += 1
            return default

    def set(self, key: Any, value: Any) -> None:
        """
        Set value in cache.

        If cache is full (maxsize reached), removes oldest item.

        Args:
            key: Cache key
            value: Value to cache
        """
        # If cache is full, remove oldest item (FIFO)
        if self._maxsize and len(self._cache) >= self._maxsize:
            if key not in self._cache:  # Only remove if adding new key
                first_key = next(iter(self._cache))
                del self._cache[first_key]

        self._cache[key] = value

    def clear(self) -> None:
        """Clear all cached items."""
        self._cache.clear()
        self._hits = 0
        self._misses = 0

    def contains(self, key: Any) -> bool:
        """
        Check if key exists in cache.

        Args:
            key: Cache key

        Returns:
            True if key exists
        """
        return key in self._cache

    @property
    def size(self) -> int:
        """Get current cache size."""
        return len(self._cache)

    @property
    def hit_rate(self) -> float:
        """
        Calculate cache hit rate.

        Returns:
            Hit rate as percentage (0-100)
        """
        total = self._hits + self._misses
        if total == 0:
            return 0.0
        return (self._hits / total) * 100

    @property
    def stats(self) -> dict:
        """
        Get cache statistics.

        Returns:
            Dictionary with hits, misses, size, and hit_rate
        """
        return {
            "hits": self._hits,
            "misses": self._misses,
            "size": self.size,
            "maxsize": self._maxsize,
            "hit_rate": self.hit_rate,
        }

    def __contains__(self, key: Any) -> bool:
        """Support 'in' operator."""
        return key in self._cache

    def __len__(self) -> int:
        """Support len() function."""
        return len(self._cache)

    def __repr__(self) -> str:
        """String representation."""
        return f"SimpleCache(size={self.size}, maxsize={self._maxsize}, hit_rate={self.hit_rate:.1f}%)"


# Global cache instances for vocabulary and phrases
_vocabulary_cache = SimpleCache(maxsize=10000)
_phrase_cache = SimpleCache(maxsize=1000)


def get_vocabulary_cache() -> SimpleCache:
    """
    Get global vocabulary cache instance.

    Returns:
        Vocabulary cache
    """
    return _vocabulary_cache


def get_phrase_cache() -> SimpleCache:
    """
    Get global phrase cache instance.

    Returns:
        Phrase cache
    """
    return _phrase_cache


def clear_all_caches() -> None:
    """Clear all global caches."""
    _vocabulary_cache.clear()
    _phrase_cache.clear()

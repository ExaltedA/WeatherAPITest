import logging
from django.core.cache import cache
from typing import Any, Optional

# Set up a logger for this module
logger = logging.getLogger(__name__)

class CacheService:
    def get_cached_data(self, cache_key: str) -> Optional[Any]:
        """
        Retrieves cached data for a given key.
        If the key does not exist, it returns None.
        """
        try:
            data = cache.get(cache_key)
            return data
        except Exception as e:
            # Log the error with ERROR level
            logger.error(f"Error retrieving cache for key {cache_key}: {e}")
            return None

    def set_cached_data(self, cache_key: str, data: Any, timeout: int = 1800) -> bool:
        """
        Caches the given data for a specified timeout.
        Returns True if the data was cached successfully, False otherwise.
        """
        try:
            cache.set(cache_key, data, timeout)
            return True
        except Exception as e:
            # Log the error with ERROR level
            logger.error(f"Error setting cache for key {cache_key}: {e}")
            return False

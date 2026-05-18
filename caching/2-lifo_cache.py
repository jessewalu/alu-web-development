#!/usr/bin/env python3
"""Module for LIFO caching system."""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """LIFO caching system."""

    def __init__(self):
        """Initialize LIFO cache."""
        super().__init__()
        self.last_key = None

    def put(self, key, item):
        """
        Add an item to the cache using LIFO policy.

        Args:
            key: The key for the item.
            item: The item to store.
        """
        if key is None or item is None:
            return

        if (
            len(self.cache_data) >= BaseCaching.MAX_ITEMS
            and key not in self.cache_data
        ):
            discard = self.last_key
            del self.cache_data[discard]
            print("DISCARD: {}".format(discard))

        self.cache_data[key] = item
        self.last_key = key

    def get(self, key):
        """
        Retrieve an item from the cache.

        Args:
            key: The key to retrieve.

        Returns:
            The cached item or None.
        """
        if key is None:
            return None

        return self.cache_data.get(key)

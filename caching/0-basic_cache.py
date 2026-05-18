#!/usr/bin/env python3
"""Module for BasicCache caching system."""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """Basic caching system without limit."""

    def put(self, key, item):
        """
        Add an item to the cache.

        Args:
            key: The key for the item.
            item: The item to store.
        """
        if key is None or item is None:
            return

        self.cache_data[key] = item

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

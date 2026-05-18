#!/usr/bin/env python3
"""Module for LRU caching system."""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """LRU caching system."""

    def __init__(self):
        """Initialize LRU cache."""
        super().__init__()
        self.usage_order = []

    def put(self, key, item):
        """
        Add an item to the cache using LRU policy.

        Args:
            key: The key for the item.
            item: The item to store.
        """
        if key is None or item is None:
            return

        if key in self.usage_order:
            self.usage_order.remove(key)

        self.cache_data[key] = item
        self.usage_order.append(key)

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            discard = self.usage_order.pop(0)
            del self.cache_data[discard]
            print("DISCARD: {}".format(discard))

    def get(self, key):
        """
        Retrieve an item from the cache.

        Args:
            key: The key to retrieve.

        Returns:
            The cached item or None.
        """
        if key is None or key not in self.cache_data:
            return None

        self.usage_order.remove(key)
        self.usage_order.append(key)

        return self.cache_data[key]

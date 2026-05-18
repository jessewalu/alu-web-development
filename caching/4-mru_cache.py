#!/usr/bin/env python3
"""Module for MRU caching system."""

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """MRU caching system."""

    def __init__(self):
        """Initialize MRU cache."""
        super().__init__()
        self.usage_order = []

    def put(self, key, item):
        """
        Add an item to the cache using MRU policy.

        Args:
            key: The key for the item.
            item: The item to store.
        """
        if key is None or item is None:
            return

        if key in self.usage_order:
            self.usage_order.remove(key)

        if (
            len(self.cache_data) >= BaseCaching.MAX_ITEMS
            and key not in self.cache_data
        ):
            discard = self.usage_order.pop()
            del self.cache_data[discard]
            print("DISCARD: {}".format(discard))

        self.cache_data[key] = item
        self.usage_order.append(key)

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

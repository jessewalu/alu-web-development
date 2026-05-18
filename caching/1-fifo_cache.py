#!/usr/bin/env python3
"""Module for FIFO caching system."""

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """FIFO caching system."""

    def __init__(self):
        """Initialize FIFO cache."""
        super().__init__()
        self.order = []

    def put(self, key, item):
        """
        Add an item to the cache using FIFO policy.

        Args:
            key: The key for the item.
            item: The item to store.
        """
        if key is None or item is None:
            return

        if key not in self.cache_data:
            self.order.append(key)

        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            discard = self.order.pop(0)
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
        if key is None:
            return None

        return self.cache_data.get(key)

"""
Core STAC Search results class - common for both PC and EarthSearch
"""
from typing import Dict, Optional
from .collections import STACItemCollection

class STACSearch:
    """Universal search results class compatible with both PC and EarthSearch."""

    def __init__(self, search_results: Dict, provider: str = "unknown"):
        self._results = search_results
        self._items = search_results.get('items', search_results.get('features', []))
        self.provider = provider

    def get_all_items(self) -> STACItemCollection:
        """Return all items as a STACItemCollection."""
        return STACItemCollection(self._items, provider=self.provider)

    def item_collection(self) -> STACItemCollection:
        """Alias for get_all_items()."""
        return self.get_all_items()

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"STACSearch({len(self._items)} items found, provider='{self.provider}')"

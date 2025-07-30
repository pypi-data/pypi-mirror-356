"""
Planetary Computer client implementation
"""
import requests
from datetime import datetime
from typing import Dict, List, Optional, Union, Any
from ..core.search import STACSearch
from .signing import sign_item

class PlanetaryComputerCollections:
    """Planetary Computer STAC API client with signing support."""

    def __init__(self, auto_sign: bool = False):
        self.base_url = "https://planetarycomputer.microsoft.com/api/stac/v1"
        self.search_url = f"{self.base_url}/search"
        self.auto_sign = auto_sign
        self.collections = self._fetch_collections()
        self._collection_details = {}

    def _fetch_collections(self):
        """Fetch all collections from the Planetary Computer STAC API."""
        url = f"{self.base_url}/collections"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            collections = data.get('collections', [])
            return {col['id']: f"{self.base_url}/collections/{col['id']}" for col in collections}
        except requests.RequestException as e:
            print(f"Error fetching collections: {e}")
            return {}

    def list_collections(self):
        """Return a list of all available collection names."""
        return sorted(list(self.collections.keys()))

    def search_collections(self, keyword):
        """Search for collections containing a specific keyword."""
        keyword = keyword.lower()
        return [col for col in self.collections.keys() if keyword in col.lower()]

    def get_collection_info(self, collection_name):
        """Get detailed information about a specific collection."""
        if collection_name not in self.collections:
            return None

        if collection_name not in self._collection_details:
            try:
                response = requests.get(self.collections[collection_name])
                response.raise_for_status()
                self._collection_details[collection_name] = response.json()
            except requests.RequestException as e:
                print(f"Error fetching collection details: {e}")
                return None

        return self._collection_details[collection_name]

    def search(self,
               collections: Optional[List[str]] = None,
               intersects: Optional[Dict] = None,
               bbox: Optional[List[float]] = None,
               datetime: Optional[Union[str, List[str]]] = None,
               query: Optional[Dict] = None,
               limit: int = 100,
               max_items: Optional[int] = None) -> STACSearch:
        """Search for products with Planetary Computer integration."""

        search_payload = {}

        if collections:
            invalid_collections = [col for col in collections if col not in self.collections]
            if invalid_collections:
                raise ValueError(f"Invalid collections: {invalid_collections}")
            search_payload["collections"] = collections

        if intersects:
            search_payload["intersects"] = intersects

        if bbox:
            if len(bbox) != 4:
                raise ValueError("bbox must be [west, south, east, north]")
            search_payload["bbox"] = bbox

        if datetime:
            if isinstance(datetime, list):
                search_payload["datetime"] = "/".join(datetime)
            else:
                search_payload["datetime"] = datetime

        if query:
            search_payload["query"] = query

        search_payload["limit"] = min(limit, 10000)

        try:
            response = requests.post(self.search_url, json=search_payload)
            response.raise_for_status()
            data = response.json()

            items = data.get("features", [])

            if max_items and len(items) > max_items:
                items = items[:max_items]

            # Auto-sign items if enabled
            if self.auto_sign:
                signed_items = []
                for item in items:
                    try:
                        signed_items.append(sign_item(item))
                    except Exception as e:
                        print(f"Warning: Failed to sign item {item.get('id', 'unknown')}: {e}")
                        signed_items.append(item)
                items = signed_items

            return STACSearch({
                "items": items,
                "total_returned": len(items),
                "search_params": search_payload,
                "collections_searched": collections or "all"
            }, provider="planetary_computer")

        except requests.RequestException as e:
            print(f"Search error: {e}")
            return STACSearch({"items": [], "total_returned": 0, "error": str(e)}, provider="planetary_computer")

    def create_bbox_from_center(self, lat: float, lon: float, buffer_km: float = 10) -> List[float]:
        """Create a bounding box around a center point."""
        buffer_deg = buffer_km / 111.0
        return [lon - buffer_deg, lat - buffer_deg, lon + buffer_deg, lat + buffer_deg]

    def create_geojson_polygon(self, coordinates: List[List[float]]) -> Dict:
        """Create a GeoJSON polygon for area of interest."""
        if coordinates[0] != coordinates[-1]:
            coordinates.append(coordinates[0])
        return {"type": "Polygon", "coordinates": [coordinates]}

    def __repr__(self):
        return f"PlanetaryComputerCollections({len(self.collections)} collections available)"

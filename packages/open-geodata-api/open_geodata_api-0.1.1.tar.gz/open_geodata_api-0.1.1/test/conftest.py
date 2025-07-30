"""
Pytest configuration and fixtures for open-geodata-api tests
"""
import pytest
import json
from unittest.mock import Mock, patch
from pathlib import Path

# Test data directory
FIXTURES_DIR = Path(__file__).parent / "fixtures"

@pytest.fixture
def sample_stac_item():
    """Sample STAC item for testing."""
    return {
        "type": "Feature",
        "stac_version": "1.0.0",
        "id": "S2A_MSIL2A_20240330T190951_N0510_R056_T10UEU_20240331T072923",
        "collection": "sentinel-2-l2a",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[-122.5, 47.5], [-122.0, 47.5], [-122.0, 48.0], [-122.5, 48.0], [-122.5, 47.5]]]
        },
        "bbox": [-122.5, 47.5, -122.0, 48.0],
        "properties": {
            "datetime": "2024-03-30T19:09:51Z",
            "eo:cloud_cover": 15.5,
            "platform": "sentinel-2a"
        },
        "assets": {
            "B02": {
                "href": "https://example.com/B02.tif",
                "type": "image/tiff",
                "title": "Blue Band"
            },
            "B03": {
                "href": "https://example.com/B03.tif", 
                "type": "image/tiff",
                "title": "Green Band"
            },
            "B04": {
                "href": "https://example.com/B04.tif",
                "type": "image/tiff", 
                "title": "Red Band"
            },
            "blue": {
                "href": "https://earthsearch.example.com/blue.tif",
                "type": "image/tiff",
                "title": "Blue Band"
            },
            "thumbnail": {
                "href": "https://example.com/thumb.jpg",
                "type": "image/jpeg",
                "title": "Thumbnail"
            }
        },
        "links": []
    }

@pytest.fixture
def sample_pc_search_response():
    """Sample Planetary Computer search response."""
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": "item1",
                "collection": "sentinel-2-l2a",
                "properties": {"datetime": "2024-01-01T00:00:00Z", "eo:cloud_cover": 10},
                "assets": {"B02": {"href": "https://pc.example.com/item1/B02.tif", "type": "image/tiff"}},
                "geometry": {"type": "Point", "coordinates": [-122, 47]},
                "bbox": [-122.1, 46.9, -121.9, 47.1]
            },
            {
                "type": "Feature", 
                "id": "item2",
                "collection": "sentinel-2-l2a",
                "properties": {"datetime": "2024-01-02T00:00:00Z", "eo:cloud_cover": 20},
                "assets": {"B02": {"href": "https://pc.example.com/item2/B02.tif", "type": "image/tiff"}},
                "geometry": {"type": "Point", "coordinates": [-122, 47]},
                "bbox": [-122.1, 46.9, -121.9, 47.1]
            }
        ]
    }

@pytest.fixture
def sample_es_search_response():
    """Sample EarthSearch search response."""
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": "es_item1", 
                "collection": "sentinel-2-l2a",
                "properties": {"datetime": "2024-01-01T00:00:00Z", "eo:cloud_cover": 15},
                "assets": {"blue": {"href": "https://es.example.com/item1/blue.tif", "type": "image/tiff"}},
                "geometry": {"type": "Point", "coordinates": [-122, 47]},
                "bbox": [-122.1, 46.9, -121.9, 47.1]
            }
        ]
    }

@pytest.fixture
def mock_requests_post():
    """Mock requests.post for API calls."""
    with patch('requests.post') as mock_post:
        yield mock_post

@pytest.fixture
def mock_requests_get():
    """Mock requests.get for API calls."""
    with patch('requests.get') as mock_get:
        yield mock_get

@pytest.fixture
def mock_pc_sign():
    """Mock planetary computer signing."""
    with patch('open_geodata_api.planetary.signing.sign_url') as mock_sign:
        mock_sign.side_effect = lambda url: f"{url}?signed=true"
        yield mock_sign

@pytest.fixture
def collections_response():
    """Sample collections response."""
    return {
        "collections": [
            {"id": "sentinel-2-l2a", "title": "Sentinel-2 Level-2A"},
            {"id": "landsat-c2-l2", "title": "Landsat Collection 2 Level-2"}
        ]
    }

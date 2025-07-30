"""
Tests for API client classes
"""
import pytest
import requests
from unittest.mock import Mock, patch

from open_geodata_api.planetary.client import PlanetaryComputerCollections
from open_geodata_api.earthsearch.client import EarthSearchCollections


class TestPlanetaryComputerCollections:
    """Test Planetary Computer client."""
    
    def test_init_default(self):
        """Test default initialization."""
        with patch.object(PlanetaryComputerCollections, '_fetch_collections', return_value={}):
            client = PlanetaryComputerCollections()
            assert client.auto_sign is False
            assert client.base_url == "https://planetarycomputer.microsoft.com/api/stac/v1"
    
    def test_init_with_auto_sign(self):
        """Test initialization with auto_sign."""
        with patch.object(PlanetaryComputerCollections, '_fetch_collections', return_value={}):
            client = PlanetaryComputerCollections(auto_sign=True)
            assert client.auto_sign is True
    
    @patch('requests.get')
    def test_fetch_collections_success(self, mock_get, collections_response):
        """Test successful collections fetching."""
        mock_get.return_value.json.return_value = collections_response
        mock_get.return_value.raise_for_status.return_value = None
        
        # Patch init to avoid first call
        with patch.object(PlanetaryComputerCollections, '__init__', lambda x: None):
            client = PlanetaryComputerCollections()
            client.base_url = "https://planetarycomputer.microsoft.com/api/stac/v1"
            
            collections = client._fetch_collections()
            
            assert "sentinel-2-l2a" in collections
            assert "landsat-c2-l2" in collections
            mock_get.assert_called_once_with(f"{client.base_url}/collections")
    
    @patch('requests.get')
    def test_fetch_collections_failure(self, mock_get):
        """Test collections fetching failure."""
        mock_get.side_effect = requests.RequestException("API Error")
        
        with patch.object(PlanetaryComputerCollections, '__init__', lambda x: None):
            client = PlanetaryComputerCollections()
            client.base_url = "https://planetarycomputer.microsoft.com/api/stac/v1"
            
            collections = client._fetch_collections()
            assert collections == {}
    
    @patch('requests.get')
    def test_list_collections(self, mock_get, collections_response):
        """Test list_collections method."""
        mock_get.return_value.json.return_value = collections_response
        mock_get.return_value.raise_for_status.return_value = None
        
        client = PlanetaryComputerCollections()
        collections = client.list_collections()
        
        assert isinstance(collections, list)
        assert "sentinel-2-l2a" in collections
        assert "landsat-c2-l2" in collections
    
    @patch('requests.get')  
    def test_search_collections(self, mock_get, collections_response):
        """Test search_collections method."""
        mock_get.return_value.json.return_value = collections_response
        mock_get.return_value.raise_for_status.return_value = None
        
        client = PlanetaryComputerCollections()
        results = client.search_collections("sentinel")
        
        assert "sentinel-2-l2a" in results
        assert "landsat-c2-l2" not in results
    
    @patch('requests.get')
    @patch('requests.post')
    def test_search_success(self, mock_post, mock_get, collections_response, sample_pc_search_response):
        """Test successful search."""
        # Mock collections call during init
        mock_get.return_value.json.return_value = collections_response
        mock_get.return_value.raise_for_status.return_value = None
        
        # Mock search call
        mock_post.return_value.json.return_value = sample_pc_search_response
        mock_post.return_value.raise_for_status.return_value = None
        
        client = PlanetaryComputerCollections()
        result = client.search(
            collections=["sentinel-2-l2a"],
            bbox=[-122.5, 47.5, -122.0, 48.0],
            datetime="2024-01-01/2024-01-31"
        )
        
        assert result is not None
        items = result.get_all_items()
        assert len(items) == 2
        assert items[0].id == "item1"
    
    @patch('requests.get')
    @patch('requests.post')
    def test_search_with_query(self, mock_post, mock_get, collections_response, sample_pc_search_response):
        """Test search with query parameter."""
        # Mock collections call during init
        mock_get.return_value.json.return_value = collections_response
        mock_get.return_value.raise_for_status.return_value = None
        
        # Mock search call
        mock_post.return_value.json.return_value = sample_pc_search_response
        mock_post.return_value.raise_for_status.return_value = None
        
        client = PlanetaryComputerCollections()
        result = client.search(
            collections=["sentinel-2-l2a"],
            query={"eo:cloud_cover": {"lt": 30}}
        )
        
        # Check that query was included in the request
        call_args = mock_post.call_args
        request_data = call_args[1]['json']
        assert 'query' in request_data
        assert request_data['query'] == {"eo:cloud_cover": {"lt": 30}}
    
    @patch('requests.get')
    def test_search_invalid_collection(self, mock_get, collections_response):
        """Test search with invalid collection."""
        mock_get.return_value.json.return_value = collections_response
        mock_get.return_value.raise_for_status.return_value = None
        
        client = PlanetaryComputerCollections()
        
        with pytest.raises(ValueError, match="Invalid collections"):
            client.search(collections=["invalid-collection"])
    
    @patch('requests.get')
    @patch('requests.post')
    def test_search_failure(self, mock_post, mock_get, collections_response):
        """Test search failure handling."""
        # Mock collections call during init
        mock_get.return_value.json.return_value = collections_response
        mock_get.return_value.raise_for_status.return_value = None
        
        # Mock search failure
        mock_post.side_effect = requests.RequestException("Search failed")
        
        client = PlanetaryComputerCollections()
        result = client.search(collections=["sentinel-2-l2a"])
        
        items = result.get_all_items()
        assert len(items) == 0
    
    def test_create_bbox_from_center(self):
        """Test bbox creation from center point."""
        with patch.object(PlanetaryComputerCollections, '_fetch_collections', return_value={}):
            client = PlanetaryComputerCollections()
            bbox = client.create_bbox_from_center(lat=47.6, lon=-122.3, buffer_km=10)
            
            assert len(bbox) == 4
            assert bbox[0] < -122.3 < bbox[2]  # lon bounds
            assert bbox[1] < 47.6 < bbox[3]   # lat bounds
    
    def test_create_geojson_polygon(self):
        """Test GeoJSON polygon creation."""
        with patch.object(PlanetaryComputerCollections, '_fetch_collections', return_value={}):
            client = PlanetaryComputerCollections()
            coords = [[-122.5, 47.5], [-122.0, 47.5], [-122.0, 48.0], [-122.5, 48.0]]
            
            polygon = client.create_geojson_polygon(coords)
            
            assert polygon['type'] == 'Polygon'
            assert polygon['coordinates'][0][0] == polygon['coordinates'][0][-1]  # Closed ring


class TestEarthSearchCollections:
    """Test EarthSearch client."""
    
    def test_init_default(self):
        """Test default initialization."""
        with patch.object(EarthSearchCollections, '_fetch_collections', return_value={}):
            client = EarthSearchCollections()
            assert client.auto_validate is False
            assert client.base_url == "https://earth-search.aws.element84.com/v1"
    
    def test_format_datetime_rfc3339(self):
        """Test datetime formatting."""
        with patch.object(EarthSearchCollections, '_fetch_collections', return_value={}):
            client = EarthSearchCollections()
            
            # Test date range
            result = client._format_datetime_rfc3339("2024-01-01/2024-01-31")
            assert result == "2024-01-01T00:00:00Z/2024-01-31T23:59:59Z"
            
            # Test single date
            result = client._format_datetime_rfc3339("2024-01-01")
            assert result == "2024-01-01T00:00:00Z"
            
            # Test already formatted
            result = client._format_datetime_rfc3339("2024-01-01T12:00:00Z")
            assert result == "2024-01-01T12:00:00Z"
    
    @patch('requests.get')
    @patch('requests.post')
    def test_search_success(self, mock_post, mock_get, collections_response, sample_es_search_response):
        """Test successful EarthSearch search."""
        # Mock collections call during init
        mock_get.return_value.json.return_value = collections_response
        mock_get.return_value.raise_for_status.return_value = None
        
        # Mock search call
        mock_post.return_value.json.return_value = sample_es_search_response
        mock_post.return_value.raise_for_status.return_value = None
        
        client = EarthSearchCollections()
        result = client.search(
            collections=["sentinel-2-l2a"],
            bbox=[-122.5, 47.5, -122.0, 48.0]
        )
        
        items = result.get_all_items()
        assert len(items) == 1
        assert items[0].id == "es_item1"
        assert items[0].provider == "earthsearch"
    
    @patch('requests.get')
    @patch('requests.post')
    def test_search_with_headers(self, mock_post, mock_get, collections_response, sample_es_search_response):
        """Test that proper headers are sent."""
        # Mock collections call during init
        mock_get.return_value.json.return_value = collections_response
        mock_get.return_value.raise_for_status.return_value = None
        
        # Mock search call
        mock_post.return_value.json.return_value = sample_es_search_response
        mock_post.return_value.raise_for_status.return_value = None
        
        client = EarthSearchCollections()
        client.search(collections=["sentinel-2-l2a"])
        
        # Check headers
        call_args = mock_post.call_args
        headers = call_args[1]['headers']
        assert headers['Content-Type'] == 'application/json'
        assert headers['Accept'] == 'application/geo+json'


## Alternative: Simplified Test Approach
# @patch('requests.get')
# def test_fetch_collections_success_alternative(self, mock_get, collections_response):
#     """Test successful collections fetching - alternative approach."""
#     mock_get.return_value.json.return_value = collections_response
#     mock_get.return_value.raise_for_status.return_value = None
    
#     client = PlanetaryComputerCollections()  # This calls _fetch_collections once
#     collections = client._fetch_collections()  # This calls it again
    
#     assert "sentinel-2-l2a" in collections
#     assert "landsat-c2-l2" in collections
#     # Expect 2 calls: one during init, one explicit
#     assert mock_get.call_count == 2

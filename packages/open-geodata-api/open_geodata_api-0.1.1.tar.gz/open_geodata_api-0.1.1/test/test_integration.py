"""
Integration tests for open-geodata-api
"""
import pytest
from unittest.mock import patch

import open_geodata_api as ogapi


class TestIntegration:
    """Integration tests."""
    
    @patch('requests.post')
    @patch('requests.get')
    def test_end_to_end_workflow(self, mock_get, mock_post, 
                                collections_response, sample_pc_search_response):
        """Test complete end-to-end workflow."""
        # Mock collections endpoint
        mock_get.return_value.json.return_value = collections_response
        mock_get.return_value.raise_for_status.return_value = None
        
        # Mock search endpoint
        mock_post.return_value.json.return_value = sample_pc_search_response
        mock_post.return_value.raise_for_status.return_value = None
        
        # Create client
        pc = ogapi.planetary_computer(auto_sign=True)
        
        # List collections
        collections = pc.list_collections()
        assert "sentinel-2-l2a" in collections
        
        # Search for data
        results = pc.search(
            collections=["sentinel-2-l2a"],
            bbox=[-122.5, 47.5, -122.0, 48.0]
        )
        
        # Get items
        items = results.get_all_items()
        assert len(items) == 2
        
        # Get URLs
        item = items[0]
        urls = item.get_all_asset_urls()
        assert isinstance(urls, dict)
        assert len(urls) > 0
        
        # Convert to DataFrame
        df = items.to_dataframe(include_geometry=False)
        assert len(df) == 2
    
    @patch('requests.post')
    def test_multi_provider_comparison(self, mock_post, 
                                     sample_pc_search_response, 
                                     sample_es_search_response):
        """Test comparing results from multiple providers."""
        
        def side_effect(*args, **kwargs):
            """Return different responses based on URL."""
            url = args[0]
            mock_response = type('MockResponse', (), {})()
            mock_response.raise_for_status = lambda: None
            
            if "planetarycomputer" in url:
                mock_response.json = lambda: sample_pc_search_response
            else:  # EarthSearch
                mock_response.json = lambda: sample_es_search_response
            
            return mock_response
        
        mock_post.side_effect = side_effect
        
        # Get clients
        clients = ogapi.get_clients(pc_auto_sign=True)
        pc = clients["planetary_computer"]
        es = clients["earth_search"]
        
        # Search both
        search_params = {
            "collections": ["sentinel-2-l2a"],
            "bbox": [-122.5, 47.5, -122.0, 48.0]
        }
        
        pc_results = pc.search(**search_params)
        es_results = es.search(**search_params)
        
        pc_items = pc_results.get_all_items()
        es_items = es_results.get_all_items()
        
        assert len(pc_items) == 2
        assert len(es_items) == 1
        assert pc_items[0].provider == "planetary_computer"
        assert es_items[0].provider == "earthsearch"
    
    def test_error_handling_workflow(self):
        """Test error handling in complete workflow."""
        # This tests error handling without mocking failures
        
        # Test with invalid client configuration
        pc = ogapi.planetary_computer()
        
        # Test search with invalid parameters
        try:
            result = pc.search(collections=["nonexistent-collection"])
            # Should handle gracefully
            items = result.get_all_items()
            assert len(items) == 0
        except Exception as e:
            # Should raise meaningful error
            assert "collection" in str(e).lower()

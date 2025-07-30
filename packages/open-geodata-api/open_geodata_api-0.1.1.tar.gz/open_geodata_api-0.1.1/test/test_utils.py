"""
Tests for utility functions
"""
import pytest
from unittest.mock import patch, Mock

from open_geodata_api.planetary.signing import sign_url, sign_item, sign_asset_urls
from open_geodata_api.earthsearch.validation import validate_url, validate_item, validate_asset_urls
from open_geodata_api.utils.filters import filter_by_cloud_cover


class TestPlanetaryComputerSigning:
    """Test Planetary Computer signing functions."""
    
    @patch('planetary_computer.sign')
    def test_sign_url_success(self, mock_pc_sign):
        """Test successful URL signing."""
        mock_pc_sign.return_value = "https://example.com/test.tif?signed=true"
        
        result = sign_url("https://example.com/test.tif")
        assert result == "https://example.com/test.tif?signed=true"
        mock_pc_sign.assert_called_once_with("https://example.com/test.tif")
    
    @patch('planetary_computer.sign')
    def test_sign_url_failure(self, mock_pc_sign):
        """Test URL signing failure."""
        mock_pc_sign.side_effect = Exception("Signing failed")
        
        with pytest.raises(RuntimeError, match="Failed to sign URL"):
            sign_url("https://example.com/test.tif")
    
    @patch('open_geodata_api.planetary.signing.SIGNING_AVAILABLE', False)
    def test_sign_url_not_available(self):
        """Test signing when planetary-computer not available."""
        with pytest.raises(ImportError, match="planetary-computer is required"):
            sign_url("https://example.com/test.tif")
    
    @patch('planetary_computer.sign')
    def test_sign_item_success(self, mock_pc_sign, sample_stac_item):
        """Test successful item signing."""
        mock_pc_sign.return_value = sample_stac_item
        
        result = sign_item(sample_stac_item)
        assert result == sample_stac_item
        mock_pc_sign.assert_called_once_with(sample_stac_item)
    
    @patch('planetary_computer.sign')
    def test_sign_asset_urls_success(self, mock_pc_sign):
        """Test successful asset URLs signing."""
        urls = {
            "B02": "https://example.com/B02.tif",
            "B03": "https://example.com/B03.tif"
        }
        mock_pc_sign.side_effect = lambda url: f"{url}?signed=true"
        
        result = sign_asset_urls(urls)
        assert result["B02"] == "https://example.com/B02.tif?signed=true"
        assert result["B03"] == "https://example.com/B03.tif?signed=true"
    
    @patch('planetary_computer.sign')
    def test_sign_asset_urls_partial_failure(self, mock_pc_sign, capsys):
        """Test asset URLs signing with partial failure."""
        urls = {
            "B02": "https://example.com/B02.tif",
            "B03": "https://example.com/B03.tif"
        }
        
        def side_effect(url):
            if "B02" in url:
                return f"{url}?signed=true"
            else:
                raise Exception("Signing failed")
        
        mock_pc_sign.side_effect = side_effect
        
        result = sign_asset_urls(urls)
        captured = capsys.readouterr()
        
        assert result["B02"] == "https://example.com/B02.tif?signed=true"
        assert result["B03"] == "https://example.com/B03.tif"  # Unsigned fallback
        assert "Warning: Failed to sign URL for band B03" in captured.out


class TestEarthSearchValidation:
    """Test EarthSearch validation functions."""
    
    def test_validate_url_success(self):
        """Test successful URL validation."""
        url = "https://example.com/test.tif"
        result = validate_url(url)
        assert result == url
    
    def test_validate_url_empty(self):
        """Test empty URL validation."""
        with pytest.raises(ValueError, match="URL cannot be empty"):
            validate_url("")
    
    def test_validate_url_invalid_scheme(self):
        """Test invalid URL scheme."""
        with pytest.raises(ValueError, match="URL must start with"):
            validate_url("ftp://example.com/test.tif")
    
    def test_validate_item_success(self, sample_stac_item):
        """Test successful item validation."""
        result = validate_item(sample_stac_item)
        assert result == sample_stac_item
    
    def test_validate_item_not_dict(self):
        """Test item validation with non-dict."""
        with pytest.raises(ValueError, match="Item must be a dictionary"):
            validate_item("not a dict")
    
    def test_validate_item_no_assets(self):
        """Test item validation without assets."""
        item = {"id": "test", "type": "Feature"}
        
        with pytest.raises(ValueError, match="Item must contain 'assets' field"):
            validate_item(item)
    
    def test_validate_asset_urls_success(self):
        """Test successful asset URLs validation."""
        urls = {
            "B02": "https://example.com/B02.tif",
            "B03": "https://example.com/B03.tif"
        }
        
        result = validate_asset_urls(urls)
        assert result == urls
    
    def test_validate_asset_urls_with_invalid(self, capsys):
        """Test asset URLs validation with invalid URL."""
        urls = {
            "B02": "https://example.com/B02.tif",
            "B03": "invalid-url"
        }
        
        result = validate_asset_urls(urls)
        captured = capsys.readouterr()
        
        assert result["B02"] == "https://example.com/B02.tif"
        assert result["B03"] == "invalid-url"  # Keeps original despite warning
        assert "Warning: Invalid URL for asset B03" in captured.out


class TestFilters:
    """Test filtering functions."""
    
    def test_filter_by_cloud_cover(self, sample_pc_search_response):
        """Test cloud cover filtering."""
        from open_geodata_api.core.collections import STACItemCollection
        
        collection = STACItemCollection(
            sample_pc_search_response["features"],
            provider="test"
        )
        
        # Filter to items with <15% cloud cover
        filtered = filter_by_cloud_cover(collection, max_cloud_cover=15)
        
        assert len(filtered) == 1  # Only item1 has 10% cloud cover
        assert filtered[0].properties["eo:cloud_cover"] == 10
    
    def test_filter_by_cloud_cover_no_cloud_data(self):
        """Test cloud cover filtering with missing cloud cover data."""
        from open_geodata_api.core.collections import STACItemCollection
        
        items_data = [
            {
                "id": "test1",
                "type": "Feature",
                "properties": {},  # No cloud cover data
                "assets": {},
                "geometry": {"type": "Point", "coordinates": [0, 0]}
            }
        ]
        
        collection = STACItemCollection(items_data, provider="test")
        filtered = filter_by_cloud_cover(collection, max_cloud_cover=30)
        
        # Items without cloud cover data should be included
        assert len(filtered) == 1

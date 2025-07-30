"""
Tests for core STAC classes
"""
import pytest
from unittest.mock import patch

from open_geodata_api.core.items import STACItem
from open_geodata_api.core.collections import STACItemCollection
from open_geodata_api.core.assets import STACAsset, STACAssets


class TestSTACAsset:
    """Test STACAsset class."""
    
    def test_init(self):
        """Test STACAsset initialization."""
        asset_data = {
            "href": "https://example.com/test.tif",
            "type": "image/tiff",
            "title": "Test Asset",
            "roles": ["data"]
        }
        
        asset = STACAsset(asset_data)
        assert asset.href == "https://example.com/test.tif"
        assert asset.type == "image/tiff"
        assert asset.title == "Test Asset"
        assert asset.roles == ["data"]
    
    def test_getitem(self):
        """Test dict-like access."""
        asset_data = {"href": "https://example.com/test.tif", "custom_field": "value"}
        asset = STACAsset(asset_data)
        
        assert asset["href"] == "https://example.com/test.tif"
        assert asset["custom_field"] == "value"
    
    def test_to_dict(self):
        """Test conversion to dict."""
        asset_data = {"href": "https://example.com/test.tif"}
        asset = STACAsset(asset_data)
        
        result = asset.to_dict()
        assert result == asset_data
        assert result is not asset._data  # Should be a copy


class TestSTACAssets:
    """Test STACAssets class."""
    
    def test_init(self):
        """Test STACAssets initialization."""
        assets_data = {
            "B02": {"href": "https://example.com/B02.tif", "type": "image/tiff"},
            "B03": {"href": "https://example.com/B03.tif", "type": "image/tiff"}
        }
        
        assets = STACAssets(assets_data)
        assert len(assets) == 2
        assert "B02" in assets
        assert isinstance(assets["B02"], STACAsset)
    
    def test_iteration(self):
        """Test asset iteration."""
        assets_data = {
            "B02": {"href": "https://example.com/B02.tif"},
            "B03": {"href": "https://example.com/B03.tif"}
        }
        
        assets = STACAssets(assets_data)
        asset_keys = list(assets)
        assert "B02" in asset_keys
        assert "B03" in asset_keys


class TestSTACItem:
    """Test STACItem class."""
    
    def test_init(self, sample_stac_item):
        """Test STACItem initialization."""
        item = STACItem(sample_stac_item, provider="test")
        
        assert item.id == sample_stac_item["id"]
        assert item.collection == "sentinel-2-l2a"
        assert item.provider == "test"
        assert isinstance(item.assets, STACAssets)
        assert len(item.assets) == 5
    
    def test_get_asset_url_basic(self, sample_stac_item):
        """Test basic asset URL retrieval."""
        item = STACItem(sample_stac_item, provider="test")
        
        url = item.get_asset_url("B02")
        assert url == "https://example.com/B02.tif"
    
    def test_get_asset_url_not_found(self, sample_stac_item):
        """Test asset URL retrieval for non-existent asset."""
        item = STACItem(sample_stac_item, provider="test")
        
        with pytest.raises(KeyError, match="Asset 'B99' not found"):
            item.get_asset_url("B99")
    
    @patch('open_geodata_api.planetary.signing.sign_url')
    def test_get_asset_url_pc_signing(self, mock_sign, sample_stac_item):
        """Test Planetary Computer URL signing."""
        mock_sign.return_value = "https://example.com/B02.tif?signed=true"
        
        item = STACItem(sample_stac_item, provider="planetary_computer")
        url = item.get_asset_url("B02", signed=True)
        
        assert url == "https://example.com/B02.tif?signed=true"
        mock_sign.assert_called_once_with("https://example.com/B02.tif")
    
    def test_get_all_asset_urls(self, sample_stac_item):
        """Test getting all asset URLs."""
        item = STACItem(sample_stac_item, provider="test")
        
        urls = item.get_all_asset_urls()
        assert isinstance(urls, dict)
        assert len(urls) == 5
        assert "B02" in urls
        assert "B03" in urls
        assert "B04" in urls
    
    def test_get_band_urls(self, sample_stac_item):
        """Test getting specific band URLs."""
        item = STACItem(sample_stac_item, provider="test")
        
        urls = item.get_band_urls(["B02", "B03", "B04"])
        assert len(urls) == 3
        assert urls["B02"] == "https://example.com/B02.tif"
        assert urls["B03"] == "https://example.com/B03.tif"
        assert urls["B04"] == "https://example.com/B04.tif"
    
    def test_get_band_urls_missing(self, sample_stac_item, capsys):
        """Test getting URLs for missing bands."""
        item = STACItem(sample_stac_item, provider="test")
        
        urls = item.get_band_urls(["B02", "B99"])
        captured = capsys.readouterr()
        
        assert len(urls) == 1  # Only B02 found
        assert "B02" in urls
        assert "B99" not in urls
        assert "Bands not available: ['B99']" in captured.out
    
    def test_list_assets(self, sample_stac_item):
        """Test listing available assets."""
        item = STACItem(sample_stac_item, provider="test")
        
        assets = item.list_assets()
        assert isinstance(assets, list)
        assert len(assets) == 5
        assert "B02" in assets
        assert "thumbnail" in assets
    
    def test_has_asset(self, sample_stac_item):
        """Test checking asset existence."""
        item = STACItem(sample_stac_item, provider="test")
        
        assert item.has_asset("B02") is True
        assert item.has_asset("B99") is False
    
    def test_get_rgb_urls(self, sample_stac_item):
        """Test getting RGB URLs."""
        item = STACItem(sample_stac_item, provider="test")
        
        # This should try red, green, blue and fall back to available assets
        urls = item.get_rgb_urls()
        # Since our sample doesn't have "red", "green", "blue" assets, should return empty
        assert isinstance(urls, dict)
    
    def test_print_assets_info(self, sample_stac_item, capsys):
        """Test printing asset info."""
        item = STACItem(sample_stac_item, provider="test")
        
        item.print_assets_info()
        captured = capsys.readouterr()
        
        assert item.id in captured.out
        assert "Available Assets" in captured.out
        assert "B02" in captured.out


class TestSTACItemCollection:
    """Test STACItemCollection class."""
    
    def test_init(self, sample_pc_search_response):
        """Test STACItemCollection initialization."""
        collection = STACItemCollection(
            sample_pc_search_response["features"], 
            provider="test"
        )
        
        assert len(collection) == 2
        assert collection.provider == "test"
        assert isinstance(collection[0], STACItem)
    
    def test_iteration(self, sample_pc_search_response):
        """Test collection iteration."""
        collection = STACItemCollection(
            sample_pc_search_response["features"],
            provider="test"
        )
        
        items = list(collection)
        assert len(items) == 2
        assert all(isinstance(item, STACItem) for item in items)
    
    def test_to_dict(self, sample_pc_search_response):
        """Test conversion to GeoJSON."""
        collection = STACItemCollection(
            sample_pc_search_response["features"],
            provider="test"
        )
        
        result = collection.to_dict()
        assert result["type"] == "FeatureCollection"
        assert len(result["features"]) == 2
    
    @patch('pandas.DataFrame')
    def test_to_dataframe_no_geometry(self, mock_df, sample_pc_search_response):
        """Test DataFrame conversion without geometry."""
        collection = STACItemCollection(
            sample_pc_search_response["features"],
            provider="test"
        )
        
        collection.to_dataframe(include_geometry=False)
        mock_df.assert_called_once()
    
    def test_get_all_assets(self, sample_pc_search_response):
        """Test getting all unique assets."""
        collection = STACItemCollection(
            sample_pc_search_response["features"],
            provider="test"
        )
        
        assets = collection.get_all_assets()
        assert isinstance(assets, list)
        assert "B02" in assets
    
    def test_get_all_urls(self, sample_pc_search_response):
        """Test getting all URLs from collection."""
        collection = STACItemCollection(
            sample_pc_search_response["features"],
            provider="test"
        )
        
        urls = collection.get_all_urls()
        assert isinstance(urls, dict)
        assert len(urls) == 2
        assert "item1" in urls
        assert "item2" in urls
    
    def test_get_all_urls_specific_assets(self, sample_pc_search_response):
        """Test getting URLs for specific assets."""
        collection = STACItemCollection(
            sample_pc_search_response["features"],
            provider="test"
        )
        
        urls = collection.get_all_urls(asset_keys=["B02"])
        assert isinstance(urls, dict)
        for item_urls in urls.values():
            assert "B02" in item_urls
    
    @patch('builtins.open')
    @patch('json.dump')
    def test_export_urls_json(self, mock_json_dump, mock_open, sample_pc_search_response):
        """Test exporting URLs to JSON."""
        collection = STACItemCollection(
            sample_pc_search_response["features"],
            provider="test"
        )
        
        collection.export_urls_json("test.json")
        mock_open.assert_called_once_with("test.json", "w")
        mock_json_dump.assert_called_once()

"""
Tests for factory functions
"""
import pytest
from unittest.mock import patch

import open_geodata_api as ogapi
from open_geodata_api.planetary.client import PlanetaryComputerCollections
from open_geodata_api.earthsearch.client import EarthSearchCollections


class TestFactoryFunctions:
    """Test factory functions."""
    
    def test_planetary_computer_default(self):
        """Test planetary_computer factory with defaults."""
        client = ogapi.planetary_computer()
        
        assert isinstance(client, PlanetaryComputerCollections)
        assert client.auto_sign is False
    
    def test_planetary_computer_with_auto_sign(self):
        """Test planetary_computer factory with auto_sign."""
        client = ogapi.planetary_computer(auto_sign=True)
        
        assert isinstance(client, PlanetaryComputerCollections)
        assert client.auto_sign is True
    
    def test_earth_search_default(self):
        """Test earth_search factory with defaults."""
        client = ogapi.earth_search()
        
        assert isinstance(client, EarthSearchCollections)
        assert client.auto_validate is False
    
    def test_earth_search_with_auto_validate(self):
        """Test earth_search factory with auto_validate."""
        client = ogapi.earth_search(auto_validate=True)
        
        assert isinstance(client, EarthSearchCollections)
        assert client.auto_validate is True
    
    def test_get_clients_default(self):
        """Test get_clients factory with defaults."""
        clients = ogapi.get_clients()
        
        assert isinstance(clients, dict)
        assert "planetary_computer" in clients
        assert "earth_search" in clients
        assert isinstance(clients["planetary_computer"], PlanetaryComputerCollections)
        assert isinstance(clients["earth_search"], EarthSearchCollections)
        assert clients["planetary_computer"].auto_sign is False
        assert clients["earth_search"].auto_validate is False
    
    def test_get_clients_with_options(self):
        """Test get_clients factory with options."""
        clients = ogapi.get_clients(pc_auto_sign=True, es_auto_validate=True)
        
        assert clients["planetary_computer"].auto_sign is True
        assert clients["earth_search"].auto_validate is True
    
    def test_info_function(self, capsys):
        """Test info function output."""
        ogapi.info()
        captured = capsys.readouterr()
        
        assert "Open Geodata API" in captured.out
        assert "Microsoft Planetary Computer" in captured.out
        assert "EarthSearch" in captured.out
        assert "Maximum flexibility" in captured.out

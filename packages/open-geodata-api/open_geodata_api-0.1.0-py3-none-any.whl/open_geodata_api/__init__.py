"""
Open Geodata API: Unified Python client for open geospatial data APIs
Supports Microsoft Planetary Computer, AWS EarthSearch, and more
"""

__version__ = "0.1.0"
__author__ = "Mirjan Ali Sha"
__email__ = "your.email@example.com"

# Import main client classes for easy access
from .planetary.client import PlanetaryComputerCollections
from .earthsearch.client import EarthSearchCollections

# Import core STAC classes
from .core.items import STACItem
from .core.assets import STACAsset, STACAssets
from .core.collections import STACItemCollection
from .core.search import STACSearch

# Import signing functions for PC
from .planetary.signing import sign_url, sign_item, sign_asset_urls

# Import validation functions for ES
from .earthsearch.validation import validate_url, validate_item, validate_asset_urls

# Import common utilities
from .utils.filters import filter_by_cloud_cover

# Factory functions for easy client creation
def planetary_computer(auto_sign: bool = False):
    """Create a Planetary Computer client for accessing Microsoft's geospatial data."""
    return PlanetaryComputerCollections(auto_sign=auto_sign)

def earth_search(auto_validate: bool = False):
    """Create an EarthSearch client for accessing AWS open datasets.""" 
    return EarthSearchCollections(auto_validate=auto_validate)

# Quick access to both major open geodata APIs
def get_clients(pc_auto_sign: bool = False, es_auto_validate: bool = False):
    """Get both Planetary Computer and EarthSearch clients for unified access."""
    return {
        'planetary_computer': planetary_computer(auto_sign=pc_auto_sign),
        'earth_search': earth_search(auto_validate=es_auto_validate)
    }

__all__ = [
    # Client classes
    'PlanetaryComputerCollections',
    'EarthSearchCollections',
    
    # Core STAC classes
    'STACItem',
    'STACAsset', 
    'STACAssets',
    'STACItemCollection',
    'STACSearch',
    
    # PC-specific functions
    'sign_url',
    'sign_item', 
    'sign_asset_urls',
    
    # ES-specific functions
    'validate_url',
    'validate_item',
    'validate_asset_urls',
    
    # Common utilities
    'filter_by_cloud_cover',
    
    # Factory functions
    'planetary_computer',
    'earth_search',
    'get_clients',
]

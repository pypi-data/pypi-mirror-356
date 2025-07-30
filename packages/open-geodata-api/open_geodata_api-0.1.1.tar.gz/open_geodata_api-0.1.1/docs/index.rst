Welcome to Open Geodata API Documentation
==========================================

.. image:: https://img.shields.io/pypi/v/open-geodata-api.svg
   :target: https://pypi.org/project/open-geodata-api/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/open-geodata-api.svg
   :target: https://pypi.org/project/open-geodata-api/
   :alt: Python versions

**Open Geodata API** is a unified Python client library that provides seamless access to multiple open geospatial data APIs. It focuses on API access, search, and URL management while maintaining maximum flexibility for data reading and processing.

Key Features
------------

✅ **Unified Access**: Single interface for multiple geospatial APIs  
✅ **Automatic URL Management**: Handles signing (PC) and validation (ES) automatically  
✅ **Maximum Flexibility**: Use any raster reading package you prefer  
✅ **Zero Lock-in**: No forced dependencies or reading methods  
✅ **Clean API**: Intuitive, Pythonic interface  
✅ **Production Ready**: Robust error handling and comprehensive testing  

Supported APIs
--------------

* **Microsoft Planetary Computer** - With automatic URL signing
* **Element84 EarthSearch** - With URL validation

Quick Example
-------------

.. code-block:: python

   import open_geodata_api as ogapi

   # Get clients for both APIs
   clients = ogapi.get_clients(pc_auto_sign=True)
   pc = clients['planetary_computer']
   
   # Search for Sentinel-2 data
   results = pc.search(
       collections=["sentinel-2-l2a"],
       bbox=[-122.5, 47.5, -122.0, 48.0],
       datetime="2024-01-01/2024-03-31"
   )
   
   # Get ready-to-use URLs
   items = results.get_all_items()
   blue_url = items[0].get_asset_url('B02')  # Automatically signed!
   
   # Use with ANY raster package
   import rioxarray
   data = rioxarray.open_rasterio(blue_url)

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   user-guide/index
   user-guide/basic-usage
   user-guide/advanced-usage
   user-guide/planetary-computer
   user-guide/earthsearch

.. toctree::
   :maxdepth: 2
   :caption: Examples

   examples/index
   examples/basic-examples
   examples/advanced-examples

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/index
   api/clients
   api/core
   api/utilities

.. toctree::
   :maxdepth: 1
   :caption: Development

   contributing
   changelog
   license

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

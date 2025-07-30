Quick Start Guide
=================

This guide will get you up and running with Open Geodata API in 5 minutes.

30-Second Example
-----------------

.. code-block:: python

   import open_geodata_api as ogapi

   # Create clients
   pc = ogapi.planetary_computer(auto_sign=True)
   
   # Search for data
   results = pc.search(
       collections=["sentinel-2-l2a"],
       bbox=[-122.5, 47.5, -122.0, 48.0],
       datetime="2024-01-01/2024-03-31"
   )
   
   # Get URLs and use with any package
   item = results.get_all_items()[0]
   blue_url = item.get_asset_url('B02')
   
   # Use with your preferred raster package
   import rioxarray
   data = rioxarray.open_rasterio(blue_url)

Basic Workflow
--------------

1. **Import and Setup**

.. code-block:: python

   import open_geodata_api as ogapi
   
   # Get both clients
   clients = ogapi.get_clients(pc_auto_sign=True)
   pc = clients['planetary_computer']
   es = clients['earth_search']

2. **Search for Data**

.. code-block:: python

   # Define search parameters
   bbox = [-122.5, 47.5, -122.0, 48.0]  # San Francisco area
   
   results = pc.search(
       collections=['sentinel-2-l2a'],
       bbox=bbox,
       datetime='2024-01-01/2024-03-31',
       query={'eo:cloud_cover': {'lt': 30}}  # Less than 30% clouds
   )

3. **Work with Results**

.. code-block:: python

   items = results.get_all_items()
   print(f"Found {len(items)} items")
   
   # Get first item
   item = items[0]
   item.print_assets_info()

4. **Get URLs for Data Reading**

.. code-block:: python

   # Single asset
   red_url = item.get_asset_url('B04')
   
   # Multiple assets
   rgb_urls = item.get_band_urls(['B04', 'B03', 'B02'])
   
   # All assets
   all_urls = item.get_all_asset_urls()

5. **Use URLs with Any Raster Package**

.. code-block:: python

   # Option 1: rioxarray
   import rioxarray
   data = rioxarray.open_rasterio(red_url)
   
   # Option 2: rasterio
   import rasterio
   with rasterio.open(red_url) as src:
       data = src.read(1)
   
   # Option 3: GDAL
   from osgeo import gdal
   dataset = gdal.Open(red_url)

Key Concepts
------------

**Providers**
  - Planetary Computer (Microsoft) - requires signing
  - EarthSearch (Element84/AWS) - no authentication needed

**Collections**
  - Groups of related datasets (e.g., "sentinel-2-l2a")

**Items**
  - Individual products/scenes with metadata

**Assets**
  - Individual files (bands, thumbnails, metadata)

**URL Management**
  - Package automatically handles signing/validation
  - URLs work with any raster reading package

Next Steps
----------

* Read the :doc:`user-guide/index` for detailed usage
* Check out :doc:`examples/index` for real-world examples
* Browse the :doc:`api/index` for complete reference

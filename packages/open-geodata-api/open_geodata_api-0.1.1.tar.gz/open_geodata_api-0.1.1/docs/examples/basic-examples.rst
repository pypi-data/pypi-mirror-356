Basic Examples
==============

Simple examples to get you started with common tasks.

Finding Available Data
----------------------

.. code-block:: python

   import open_geodata_api as ogapi
   
   # Setup client
   pc = ogapi.planetary_computer(auto_sign=True)
   
   # List all collections
   collections = pc.list_collections()
   print(f"Available collections: {len(collections)}")
   
   # Find Sentinel collections
   sentinel_collections = [c for c in collections if 'sentinel' in c.lower()]
   print(f"Sentinel collections: {sentinel_collections}")

Geographic Data Search
----------------------

.. code-block:: python

   # Define area of interest (San Francisco Bay Area)
   bbox = [-122.5, 37.5, -122.0, 38.0]
   
   # Search for recent, low-cloud data
   results = pc.search(
       collections=['sentinel-2-l2a'],
       bbox=bbox,
       datetime='2024-06-01/2024-08-31',
       query={'eo:cloud_cover': {'lt': 20}},
       limit=10
   )
   
   items = results.get_all_items()
   print(f"Found {len(items)} items with <20% clouds")

Working with Search Results
---------------------------

.. code-block:: python

   # Convert to DataFrame for analysis
   df = items.to_dataframe()
   
   # Basic statistics
   print(f"Date range: {df['datetime'].min()} to {df['datetime'].max()}")
   print(f"Cloud cover: {df['eo:cloud_cover'].min():.1f}% to {df['eo:cloud_cover'].max():.1f}%")
   print(f"Collections: {df['collection'].unique()}")

Getting Data URLs
-----------------

.. code-block:: python

   # Get first item
   item = items[0]
   
   # Show available assets
   item.print_assets_info()
   
   # Get specific band URLs
   rgb_urls = item.get_band_urls(['B04', 'B03', 'B02'])  # Red, Green, Blue
   print(f"RGB URLs: {list(rgb_urls.keys())}")
   
   # Get all asset URLs
   all_urls = item.get_all_asset_urls()
   print(f"Total assets: {len(all_urls)}")

Using URLs with Different Packages
-----------------------------------

.. code-block:: python

   # Get red band URL
   red_url = item.get_asset_url('B04')
   
   # Option 1: rioxarray
   import rioxarray
   data_xr = rioxarray.open_rasterio(red_url)
   print(f"rioxarray shape: {data_xr.shape}")
   
   # Option 2: rasterio
   import rasterio
   with rasterio.open(red_url) as src:
       data_rio = src.read(1)
       print(f"rasterio shape: {data_rio.shape}")
   
   # Option 3: GDAL
   from osgeo import gdal
   dataset = gdal.Open(red_url)
   band = dataset.GetRasterBand(1)
   data_gdal = band.ReadAsArray()
   print(f"GDAL shape: {data_gdal.shape}")

Installation
============

Basic Installation
------------------

Install the core package from PyPI:

.. code-block:: bash

   pip install open-geodata-api

This installs the minimal dependencies needed for API access and URL management.

Optional Dependencies
---------------------

For Spatial Analysis
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install open-geodata-api[spatial]

Includes: geopandas, shapely

For Raster Reading (Suggestions)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Option 1: rioxarray + xarray
   pip install open-geodata-api[raster-rioxarray]
   
   # Option 2: rasterio only
   pip install open-geodata-api[raster-rasterio]
   
   # Option 3: GDAL
   pip install open-geodata-api[raster-gdal]

Complete Installation
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install open-geodata-api[complete]

Includes all optional dependencies.

Development Installation
------------------------

For contributors:

.. code-block:: bash

   git clone https://github.com/yourusername/open-geodata-api.git
   cd open-geodata-api
   pip install -e .[dev]

Verify Installation
-------------------

.. code-block:: python

   import open_geodata_api as ogapi
   ogapi.info()

Dependencies
------------

Core Dependencies
~~~~~~~~~~~~~~~~~

* requests >= 2.25.0
* pandas >= 1.3.0  
* planetary-computer >= 1.0.0

Optional Dependencies
~~~~~~~~~~~~~~~~~~~~~

* geopandas >= 0.10.0 (for spatial operations)
* rioxarray >= 0.11.0 (for raster reading)
* rasterio >= 1.3.0 (for raster reading)
* matplotlib >= 3.3.0 (for plotting examples)

System Requirements
-------------------

* Python 3.8+
* Operating System: Linux, macOS, Windows
* Memory: 1GB+ RAM recommended for large datasets

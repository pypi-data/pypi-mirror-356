Examples
========

This section provides practical examples of using Open Geodata API for real-world geospatial data tasks.

.. toctree::
   :maxdepth: 2

   basic-examples
   advanced-examples

Example Notebooks
-----------------

Interactive Jupyter notebooks with complete examples:

.. toctree::
   :maxdepth: 1
   :glob:

   notebooks/*

Quick Reference
---------------

**Data Discovery**

.. code-block:: python

   # List available collections
   collections = pc.list_collections()
   
   # Get collection details
   info = pc.get_collection_info('sentinel-2-l2a')

**Geographic Search**

.. code-block:: python

   # Search by bounding box
   results = pc.search(
       collections=['sentinel-2-l2a'],
       bbox=[-122.5, 47.5, -122.0, 48.0]
   )

**Data Export**

.. code-block:: python

   # Export URLs to JSON
   items.export_urls_json('urls.json')
   
   # Convert to DataFrame
   df = items.to_dataframe()

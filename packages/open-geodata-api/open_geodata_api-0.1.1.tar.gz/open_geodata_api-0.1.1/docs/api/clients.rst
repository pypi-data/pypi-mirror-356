API Clients
===========

This module contains the main client classes for accessing different geospatial APIs.

Planetary Computer Client
--------------------------

.. autoclass:: open_geodata_api.planetary.client.PlanetaryComputerCollections
   :members:
   :undoc-members:
   :show-inheritance:

   Example usage:

   .. code-block:: python

      pc = PlanetaryComputerCollections(auto_sign=True)
      results = pc.search(
          collections=["sentinel-2-l2a"],
          bbox=[-122.5, 47.5, -122.0, 48.0]
      )

EarthSearch Client  
------------------

.. autoclass:: open_geodata_api.earthsearch.client.EarthSearchCollections
   :members:
   :undoc-members:
   :show-inheritance:

   Example usage:

   .. code-block:: python

      es = EarthSearchCollections()
      results = es.search(
          collections=["sentinel-2-l2a"],
          bbox=[-122.5, 47.5, -122.0, 48.0]
      )

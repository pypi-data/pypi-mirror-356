Contributing
============

We welcome contributions to Open Geodata API! This guide will help you get started.

Types of Contributions
----------------------

* **Bug Reports**: Found a bug? Report it on GitHub Issues
* **Feature Requests**: Have an idea? Submit a feature request
* **Code Contributions**: Fix bugs or add features via Pull Requests
* **Documentation**: Improve docs, examples, or tutorials
* **Testing**: Add test cases or improve test coverage

Development Setup
-----------------

1. **Fork and Clone**

.. code-block:: bash

   git clone https://github.com/yourusername/open-geodata-api.git
   cd open-geodata-api

2. **Install Development Dependencies**

.. code-block:: bash

   pip install -e .[dev]

3. **Run Tests**

.. code-block:: bash

   pytest

4. **Check Code Style**

.. code-block:: bash

   black .
   flake8

Pull Request Process
--------------------

1. Create a feature branch: ``git checkout -b feature-name``
2. Make your changes
3. Add tests for new functionality
4. Update documentation if needed
5. Run tests and style checks
6. Submit a Pull Request

Code Style Guidelines
---------------------

* Follow PEP 8
* Use Black for code formatting
* Add type hints for public APIs
* Write comprehensive docstrings
* Keep functions focused and small

Documentation Guidelines
------------------------

* Update relevant documentation for any changes
* Add examples for new features
* Use Google-style docstrings
* Test code examples in documentation

Testing Guidelines
------------------

* Write tests for new functionality
* Maintain high test coverage
* Use descriptive test names
* Mock external API calls in tests

Release Process
---------------

1. Update version in ``__init__.py``
2. Update ``CHANGELOG.rst``
3. Create release PR
4. Tag release after merge
5. Automated PyPI deployment via GitHub Actions

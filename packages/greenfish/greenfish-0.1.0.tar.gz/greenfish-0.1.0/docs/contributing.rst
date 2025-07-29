Contributing
============

Thank you for considering contributing to Greenfish! This page provides a brief overview of the contribution process.

For detailed instructions, please see the `CONTRIBUTING.md <https://github.com/mexyusef/greenfish/blob/main/CONTRIBUTING.md>`_ file in the repository.

Getting Started
--------------

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Make your changes
4. Run the tests to ensure they pass
5. Submit a pull request

Development Environment
---------------------

To set up your development environment:

.. code-block:: bash

    # Clone the repository
    git clone https://github.com/mexyusef/greenfish.git
    cd greenfish

    # Create and activate virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    # Install development dependencies
    pip install -e ".[dev]"

Code Style
---------

We use the following tools to ensure code quality:

- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

Run the following commands before submitting a PR:

.. code-block:: bash

    # Format code
    black greenfish tests
    isort greenfish tests

    # Check code quality
    flake8 greenfish tests
    mypy greenfish

Testing
------

We use pytest for testing. Write tests for new features and ensure all tests pass before submitting a PR:

.. code-block:: bash

    pytest

For test coverage:

.. code-block:: bash

    pytest --cov=greenfish tests/

Documentation
-----------

We use Sphinx for documentation. To build the documentation:

.. code-block:: bash

    cd docs
    make html

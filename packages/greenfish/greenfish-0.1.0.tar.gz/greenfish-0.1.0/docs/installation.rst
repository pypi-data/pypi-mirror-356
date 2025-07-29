Installation
============

Prerequisites
------------

Before installing Greenfish, ensure you have the following prerequisites:

* Python 3.8 or higher
* pip (Python package installer)

For development, you'll also need:

* Git
* A virtual environment tool (optional but recommended)

Installing from PyPI
-------------------

The easiest way to install Greenfish is from PyPI:

.. code-block:: bash

    pip install greenfish

This will install Greenfish and all its dependencies.

Installing from Source
---------------------

To install Greenfish from source:

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/mexyusef/greenfish.git
       cd greenfish

2. Create and activate a virtual environment (optional but recommended):

   .. code-block:: bash

       python -m venv venv
       # On Windows:
       venv\Scripts\activate
       # On Unix or MacOS:
       source venv/bin/activate

3. Install the package in development mode:

   .. code-block:: bash

       pip install -e .

   This will install Greenfish in development mode, allowing you to make changes to the code and see them reflected immediately.

4. For development, you might want to install additional dependencies:

   .. code-block:: bash

       pip install -e ".[dev]"

Verifying Installation
---------------------

To verify that Greenfish has been installed correctly, run:

.. code-block:: bash

    greenfish --version

This should display the version number of Greenfish that you have installed.

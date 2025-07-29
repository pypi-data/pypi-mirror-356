Virtual Environments
==================

Using Virtual Environments
-------------------------

We recommend using Python virtual environments for all Python projects. This isolates your project dependencies from your system Python installation and other projects.

Creating a Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For all Generate Git Timesheet development and usage, we use the ``.venv`` directory for virtual environments:

.. code-block:: bash

   # Create a virtual environment in the .venv directory
   python -m venv .venv

Activating the Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before installing or using Generate Git Timesheet, activate the virtual environment:

On Linux/macOS:

.. code-block:: bash

   source .venv/bin/activate

On Windows:

.. code-block:: bash

   .venv\Scripts\activate

Your command prompt should change to indicate that the virtual environment is active.

Installing in the Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the virtual environment is active, you can install the package:

.. code-block:: bash

   # For users
   pip install git-timesheet

   # For developers
   pip install -e ".[dev]"

Deactivating the Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you're done working with Generate Git Timesheet, you can deactivate the virtual environment:

.. code-block:: bash

   deactivate
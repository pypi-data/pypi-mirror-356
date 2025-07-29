Git Timesheet Generator
=====================

A Python tool to generate timesheets from git commit history.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   user/index
   user/virtualenv
   api/index

Overview
--------

This tool analyzes git commit history across multiple repositories and:

- Filters commits by author name/email
- Estimates time spent on each commit (in 15-minute increments)
- Adjusts time based on commit message keywords
- Groups work by day and week
- Formats output as a readable timesheet

Quick Start
----------

.. code-block:: bash

   # Create and activate a virtual environment
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Install the package
   pip install git-timesheet

   # Initialize configuration
   ggts --init
   # or
   ggts init

   # Generate a timesheet for the last 2 weeks
   ggts --since="2 weeks ago"
   # or explicitly
   ggts generate --since="2 weeks ago"

   # Generate a CSV timesheet for a specific repository
   ggts --repos my-project --output csv --output-file timesheet.csv

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
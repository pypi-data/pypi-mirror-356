.. bc_configs documentation master file, created by
   sphinx-quickstart on Sat Sep 30 20:30:18 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to bc-configs's documentation!
======================================

*Let's make your configuration easy.*

Introduction
------------

`bc-configs` is a library that makes configuring your applications easier.

Installation
------------

To install, use pip:

.. code-block:: bash

   pip install bc-configs

Make your custom config class
-----------------------------

You can create your custom config class by inheriting from `BaseConfig`:

.. code-block:: python

   import os
   from bc_configs import BaseConfig

   class MyConfig(BaseConfig):
       some_int: int
       some_string: str
       some_bool: bool

   my_config = MyConfig()  # type: ignore[call-arg]

   assert int(os.getenv("MY_SOME_INT")) == my_config.some_int  # True
   assert os.getenv("MY_SOME_STRING") == my_config.some_string  # True
   assert bool(os.getenv("MY_SOME_BOOL")) == my_config.some_bool  # True

The name of the environment variable is formed based on the names of the class and field.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   bc_configs
   for_contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

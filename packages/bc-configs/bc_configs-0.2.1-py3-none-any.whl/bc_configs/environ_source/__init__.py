"""
Module with methods that configure the environment source.

If you wanna use it, please that in your main src `__init__.py` file.

.. code:: python

    from bc_configs import define

    define()

.. note::

    If python-dotenv installed, it will use the dotenv module and call the load_dotenv function.

.. note::

    If hvac installed, it will use the hvac module and put data form storage to os.environ.


"""

from .define import define
from .EnvironSourceException import EnvironSourceException
from .VaultConfig import VaultConfig

__all__ = ["EnvironSourceException", "VaultConfig", "define"]

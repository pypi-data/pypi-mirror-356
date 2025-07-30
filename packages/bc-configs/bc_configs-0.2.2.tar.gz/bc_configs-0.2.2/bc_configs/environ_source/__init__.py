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

.. note::

    If `pyyaml` is installed, `bc_configs` will attempt to load environment variables
    from a YAML file. By default, it looks for `.env.yml` in the current working directory.
    You can specify a different YAML file by setting the `YAML_CONFIG_FILE` environment variable.
    Variables from the YAML file will be loaded into `os.environ`, but existing environment
    variables will not be overwritten.

    Example `.env.yml` file:

    .. code-block:: yaml

        APP_NAME: MyAwesomeApp
        DEBUG_MODE: true
        DATABASE_URL: postgresql://user:password@host:port/dbname


"""

from .define import define
from .EnvironSourceException import EnvironSourceException
from .VaultConfig import VaultConfig

__all__ = ["EnvironSourceException", "VaultConfig", "define"]

import logging
import os

from .EnvironSourceException import EnvironSourceException
from .VaultConfig import VaultConfig


def define(*, vault_config: VaultConfig | None = None) -> None:
    """
    Define the configuration for the application.

    :param vault_config: The configuration for accessing secrets from a vault. Defaults to None.
    :type vault_config: VaultConfig | None
    """
    # Define environment variables from .env file
    _dotenv_define()

    # Define configuration for accessing secrets from a vault
    _vault_define(vault_config)


def _dotenv_define() -> None:
    """
    Load the dotenv module and call the load_dotenv function.

    This function checks if the dotenv module is available and then imports it.
    It then calls the load_dotenv function to load the environment variables
    from the .env file.

    Note: This function is particularly useful during local development,
    as it allows you to define environment variables
    in a .env file and have them automatically loaded into your application.
    """
    try:
        from dotenv import load_dotenv  # type: ignore[import]
    except ImportError:
        logging.debug("python-dotenv is not installed and will be skipped")
    else:
        load_dotenv()


def _vault_define(config: VaultConfig | None = None) -> None:
    """
    Define environment variables from secrets stored in Vault.

    :param config: The VaultConfig object containing the configuration for accessing Vault.
    :type config: VaultConfig | None

    :raises EnvironSourceException: If hvac module is not installed or if there is no data to connect to Vault.
    """
    config = config or VaultConfig()
    if config.need_to_use():
        try:
            import hvac  # type: ignore[import]
        except ImportError:
            raise EnvironSourceException(
                "hvac is not installed but you are trying to use Vault for config. "
                "Please install hvac module `pip install hvac`.",
            ) from None

        if config.has_filled_connect_fields():
            vault_client = hvac.Client(url=config.address)
            if config.token:
                vault_client.token = config.token
            elif config.username and config.password:
                vault_client.auth.ldap.login(username=config.username, password=config.password)

            vault_secrets = vault_client.secrets.kv.v2.read_secret(mount_point=config.mount, path=config.path)["data"][
                "data"
            ]

            for k, v in vault_secrets.items():
                if k not in os.environ:
                    os.environ.update(**{k: str(v)})
        else:
            raise EnvironSourceException("There is no data to connect to Vault")

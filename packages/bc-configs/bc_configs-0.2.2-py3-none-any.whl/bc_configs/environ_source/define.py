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

    # Define environment variables from .env.yml file
    _yaml_define()

    # Define configuration for accessing secrets from a vault
    _vault_define(vault_config)


def _dotenv_define() -> None:
    """
    Load the dotenv module (from python-dotenv package) and call the load_dotenv function.

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


def _yaml_define() -> None:
    """
    Load the yaml module (from pyyaml package) and define environment variables from secrets stored in yaml file.

    This function checks if the yaml module is available and then imports it.
    It then calls the load_yaml function to load the environment variables
    from the .env.yml file or $YAML_CONFIG_FILE.
    """

    try:
        import yaml  # type: ignore[import]
    except ImportError:
        logging.debug("pyyaml is not installed and will be skipped")
        return

    def load_yaml_from_file(file_path: str) -> None:
        """
        Loads environment variables from a YAML file.

        :param file_path: The path to the YAML file.
        :type file_path: str
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                yaml_secrets = yaml.safe_load(f)
            if not isinstance(yaml_secrets, dict):
                logging.warning(f"YAML file '{file_path}' does not contain a top-level dictionary. Skipping.")
                return

            for k, v in yaml_secrets.items():
                if not isinstance(k, str):
                    logging.warning(f"Key '{k}' in YAML file '{file_path}' is not a string. Skipping.")
                    continue
                if k not in os.environ:
                    os.environ.update(**{k: str(v)})
                else:
                    logging.debug(f"Environment variable '{k}' already exists. Skipping loading from YAML file.")

        except FileNotFoundError:
            logging.debug(f"YAML file '{file_path}' not found. Skipping loading.")

    load_yaml_from_file(os.getenv("YAML_CONFIG_FILE", ".env.yml"))


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

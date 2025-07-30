from pydantic import Field

from ..configurator import BaseConfig


class VaultConfig(BaseConfig):
    """
    Configuration for HashiCorp Vault.
    """

    address: str | None = Field(default=None, description="The address of the Vault server.")
    mount: str | None = Field(default=None, description="The mount point of the Vault server.")
    path: str | None = Field(default=None, description="The path to the secret in the Vault.")
    token: str | None = Field(default=None, description="The authentication token for accessing the Vault.")
    username: str | None = Field(
        default=None,
        description="The username for authentication (if token is not provided).",
    )
    password: str | None = Field(
        default=None,
        description="The password for authentication (if token is not provided).",
    )

    def need_to_use(self) -> bool:
        """
        Check if the token or username and password are provided.

        :return: True if the token or username and password are provided, False otherwise.
        :rtype: bool
        """
        return bool(self.token or (self.username and self.password))

    def has_filled_connect_fields(self) -> bool:
        """
        Check if all connect fields are filled.

        :return: True if all fields are filled, False otherwise.
        :rtype: bool
        """
        return all([self.address, self.mount, self.path, self.need_to_use()])

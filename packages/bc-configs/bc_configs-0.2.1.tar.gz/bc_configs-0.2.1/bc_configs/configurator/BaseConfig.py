import os
import re
from abc import ABC
from typing import Any, cast

from pydantic import BaseModel, model_validator


def _get_env_name_by_field_name(class_name: str, field_name: str) -> str:
    """
    Generate the environment variable name based on the class name and field name.

    This function is used when defining a custom configuration class that extends BaseConfig
    or any other BaseConfig extended class, in order to use different names for environment
    variables for them.

    :param class_name: The name of the class.
    :type class_name: str
    :param field_name: The name of the field.
    :type field_name: str
    :return: The environment variable name generated based on the class name and field name.
    :rtype: str
    """
    return "_".join(
        [
            i.replace("_", "").upper()
            for i in re.findall(r"[A-ZА-Я_][a-zа-я\d]*", f"{class_name.replace('Config', '')}_{field_name}")  # noqa: RUF001
        ],
    )


def _get_field_form_env(
    *,
    class_name: str | None = None,
    field_name: str | None = None,
    env_name: str | None = None,
) -> Any:
    """
    Get the value of a field from the environment variables.

    If the `env_name` parameter is provided, it returns the value of the corresponding
    environment variable.
    If the `class_name` and `field_name` parameters are provided, it generates the
    environment variable name using
    `_get_env_name_by_field_name` function and returns the value of the corresponding
    environment variable.

    :param class_name: The name of the class.
    :type class_name: str, optional
    :param field_name: The name of the field.
    :type field_name: str, optional
    :param env_name: The name of the environment variable.
    :type env_name: str, optional
    :return: The value of the field from the environment variables.
    :rtype: Any
    :raises TypeError: If the key type for the variable is invalid.
    """
    result = None
    if isinstance(env_name, str):
        result = os.getenv(env_name)
    elif isinstance(class_name, str) and isinstance(field_name, str):
        result = os.getenv(_get_env_name_by_field_name(class_name, field_name))
    else:
        raise TypeError("Invalid key type for variable")

    return result


class BaseConfig(BaseModel, ABC):
    """
    Provides to receive values from the environment variables on the validation step of
    pydantic model.
    """

    @model_validator(mode="before")
    @classmethod
    def _populate_from_env(cls, data: dict) -> Any:
        """
        This function checks if any value in the input `data` dictionary is None.
        If a value is None, it retrieves the value from the environment variables
        based on the class name and field name.

        :param cls: The class that the function is called on.
        :type cls: type
        :param values: The dictionary of values to check and update.
        :type values: dict
        :return: The updated dictionary of values that will be stored in config instance.
        :rtype: dict
        """
        for field_name, field_info in cls.model_fields.items():
            if data.get(field_name) is None:
                if not isinstance(field_info.json_schema_extra, dict) and field_info.json_schema_extra is not None:
                    raise ValueError(
                        f"Unexpected {cls.__name__}.{field_name} json_schema_extra type: {type(field_info.json_schema_extra).__name__}",  # noqa: E501
                    )
                env_name = cast(str, (field_info.json_schema_extra or {}).get("env_name"))

                value = _get_field_form_env(
                    class_name=cls.__name__,
                    field_name=field_name,
                    env_name=env_name,
                )
                if value is not None:
                    data[field_name] = value

        return data

import os
import unittest
from unittest.mock import patch

from pydantic import Field, ValidationError

from bc_configs.configurator.BaseConfig import BaseConfig


class TestBaseConfig(unittest.TestCase):
    def test_change_from_env_if_none(self) -> None:
        # Create an instance of the custom configuration class that extends BaseConfig
        class CustomConfig(BaseConfig):
            field1: str
            field2: int
            field3: float
            field4: bool

        # Mock the os.environ dictionary with the desired values
        with patch.dict(
            os.environ,
            {
                "CUSTOM_FIELD1": "value1",
                "CUSTOM_FIELD2": "42",
                "CUSTOM_FIELD3": "3.14",
                "CUSTOM_FIELD4": "True",
            },
        ):
            # Create an instance of the custom configuration class
            config = CustomConfig()  # type: ignore[call-arg]

            # Check if the values are retrieved from the environment variables correctly
            self.assertEqual(config.field1, "value1")
            self.assertEqual(config.field2, 42)
            self.assertAlmostEqual(config.field3, 3.14)
            self.assertTrue(config.field4)

    def test_missing_field_error(self) -> None:
        # Create an instance of the custom configuration class that extends BaseConfig
        class CustomConfig(BaseConfig):
            field1: str
            field2: int

        # Mock the os.environ dictionary with a subset of the required fields
        with patch.dict(os.environ, {"CUSTOM_FIELD1": "value1"}):
            # Create an instance of the custom configuration class
            with self.assertRaises(ValidationError) as context:
                _ = CustomConfig()  # type: ignore[call-arg]

            # Check if the correct error message is raised
            self.assertEqual(1, len(context.exception.errors()[0]["loc"]))
            self.assertEqual("field2", context.exception.errors()[0]["loc"][0])

    def test_custom_env_var_name(self) -> None:
        # Create an instance of the custom configuration class that extends BaseConfig
        class CustomConfig(BaseConfig):
            my_field: str = Field(json_schema_extra={"env_name": "CUSTOM_ENV_NAME"})

        # Mock the os.environ dictionary with the desired values
        with patch.dict(os.environ, {"CUSTOM_ENV_NAME": "value1"}):
            # Create an instance of the custom configuration class
            config = CustomConfig()  # type: ignore[call-arg]

        # Check if the values are retrieved from the environment variables correctly
        self.assertEqual(config.my_field, "value1")


if __name__ == "__main__":
    unittest.main()

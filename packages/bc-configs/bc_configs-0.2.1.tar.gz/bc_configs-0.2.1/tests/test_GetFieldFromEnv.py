import os
import unittest
from unittest.mock import patch

from bc_configs.configurator.BaseConfig import _get_field_form_env


class TestGetFieldFromEnv(unittest.TestCase):
    def test_get_field_from_env_with_env_name(self) -> None:
        """
        Test case: When `env_name` parameter is provided
        It should return the value of the corresponding environment variable
        """
        with patch.dict(os.environ, {"MY_VARIABLE": "my_value"}):
            result = _get_field_form_env(env_name="MY_VARIABLE")
            self.assertEqual(result, "my_value")

    def test_get_field_from_env_invalid_key_type(self) -> None:
        """
        Test case: When the key type for the variable is invalid
        It should raise a TypeError
        """
        with self.assertRaises(TypeError):
            _get_field_form_env(class_name=123, field_name="my_field")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()

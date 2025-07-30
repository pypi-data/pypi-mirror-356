import unittest

from bc_configs.configurator.BaseConfig import _get_env_name_by_field_name


class TestGetEnvNameByFieldName(unittest.TestCase):
    def test_case_1(self) -> None:
        result = _get_env_name_by_field_name("MyConfig", "my_field")
        self.assertEqual(result, "MY_MY_FIELD")

    def test_case_2(self) -> None:
        result = _get_env_name_by_field_name("MyOtherConfig", "another_field")
        self.assertEqual(result, "MY_OTHER_ANOTHER_FIELD")

    def test_case_3(self) -> None:
        result = _get_env_name_by_field_name("SomeClass", "some_field")
        self.assertEqual(result, "SOME_CLASS_SOME_FIELD")


if __name__ == "__main__":
    unittest.main()

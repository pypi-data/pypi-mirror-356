"""
Module with BaseConfig. That config is the main element of `bc_configs`.
It provides to receive values from the environment variables on the validation step of
pydantic model. For use, create child class of `BaseConfig` and declare needed fields with typehint.

.. code:: python

    class MyConfig(BaseConfig):
        my_field: str


    my_config = MyConfig()  # type: ignore[call-arg]

.. note::

    `my_config.my_field` will contain the value of the environment variable `MY_MY_FIELD`.


Building the environment variable name
------------------------------------------

- First part of the environment variable name is the class name in SCREAMING_SNAKE_CASE without the `Config` suffix.
- Second part of the environment variable name is the field name in SCREAMING_SNAKE_CASE.

.. note::

    If class name is `FooBarConfig` and field name is `del_bar` then the environment variable name will be
    `FOO_BAR_DEL_BAR`.

Customizing the environment variable name
--------------------------------------------

If you want to customize the environment variable name, you can define it in `field→json_schema_extra→env_name`.

.. code:: python

    from pydantic import Field


    class FooConfig(BaseConfig):
        bar: str = Field(json_schema_extra={"env_name": "CUSTOM_ENV_NAME"})

Casting the environment variable value
------------------------------------------

If you want to cast the environment variable value, you can define field typehint.

.. code:: python

    class FooConfig(BaseConfig):
        bar: str
        baz: int
        foo: bool


    foo_config = FooConfig()

    assert isinstance(foo_config.bar, str)  # True
    assert isinstance(foo_config.baz, int)  # True
    assert isinstance(foo_config.foo, bool)  # True

Optional fields
----------------

If you want to make the field optional, you can define field typehint with `| None`.

.. code:: python

    import os


    class FooConfig(BaseConfig):
        bar: str | None


    foo_config = FooConfig()

    assert os.getenv("FOO_BAR") is None  # True
    assert foo_config.bar is None  # True

.. warning::

    By default, all fields are required. If the environment variable is missing an exception will follow.

Default values
-----------------

If you want to define default values for the fields, you can define Field with default value argument.

.. code:: python

    import os
    from pydantic import Field


    class FooConfig(BaseConfig):
        bar: str = Field(default="default value")

    assert os.getenv("FOO_BAR") is None  # True
    assert foo_config.bar == "default value"  # True

"""

from .BaseConfig import BaseConfig

__all__ = ["BaseConfig"]

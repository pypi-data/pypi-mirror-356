# bc-config

![](./docs/source/_static/coverage-badge.svg) ![](./docs/source/_static/unittests-badge.svg) ![](./docs/source/_static/mypy-badge.svg) ![](./docs/source/_static/ruff-badge.svg)

*Make configuring your application easier.*

# Installing

```bash
pip install bc-configs
```

# Make your custom config class

```python
import os
from bc_configs import BaseConfig

class MyConfig(BaseConfig):
    some_int: int
    some_string: str
    some_bool: bool

my_config = MyConfig()  # type: ignore[call-arg]

assert int(os.getenv("MY_SOME_INT")) == my_config.some_int  # True
assert os.getenv("MY_SOME_STRING") == my_config.some_string  # True
assert bool(os.getenv("MY_SOME_BOOL")) == my_config.some_bool  # True
```

The name of the environment variable is formed based on the names of the class and field.

For contributing
=================

.. toctree::
   :maxdepth: 4

Installing environment
-----------------------

Clone the repository.

.. code:: bash

    git clone git@github.com:esoft-tech/py-bc-configs.git


Install poetry using the guide from their website – https://python-poetry.org/docs/#installation.

After installation, apply this in order for poetry to create venv in your project folder.

.. code:: bash

    poetry config virtualenvs.in-project true


Inside project directory install dependencies.

.. code:: bash

    poetry install


After that, install pre-commit hook.

.. code:: bash

    ./.venv/bin/python -m pre-commit install


Done 🪄 🐈‍⬛ Now you can develop.

If you want contributing
-------------------------

- Check that ruff passed.
- Check that mypy passed.
- Before adding or changing the functionality, write unittests.
- Check that unittests passed.

If you need to build and publish the package
---------------------------------------------

Up the package version in the `pyproject.toml`.

.. code:: diff

    - version = "0.1.0"
    + version = "0.1.1"

Commit changes and push them to the origin.

.. code:: bash

    git add pyproject.toml
    git commit -m "Up to 0.1.1"
    git push

Make a tag and push them to the origin.

.. code:: bash

    git tag 0.1.1
    git push origin 0.1.1


Build the package.

.. code:: bash

    poetry build


Configurate your pypi token for the poetry.

.. code:: bash

    poetry config pypi-token.pypi <your-api-token>

Publish the package.

.. code:: bash

    poetry publish

.. warning::

    Make a release with notes about changes.


How to generate badges?
-------------------------


Just exec that command.

.. code:: bash

    ./.venv/bin/python ./.bc/badges.py

Then all badges actualize ourselves.


How to build sphinx docs?
-----------------------------

.. code:: bash

    bash ./.bc/build_docs.sh

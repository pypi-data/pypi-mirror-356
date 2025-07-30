|coverage| |maintainability| |precommit_ci| |docs| |style| |version| |status| |pyversions|


.. |docs| image:: https://readthedocs.com/projects/mirageoscience-plate-simulation/badge/?version=latest
    :alt: Documentation Status
    :target: https://mirageoscience-plate-simulation.readthedocs-hosted.com/en/latest/?badge=latest

.. |coverage| image:: https://codecov.io/gh/MiraGeoscience/plate-simulation/branch/develop/graph/badge.svg
    :alt: Code coverage
    :target: https://codecov.io/gh/MiraGeoscience/plate-simulation

.. |style| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Coding style
    :target: https://github.com/pf/black

.. |version| image:: https://img.shields.io/pypi/v/plate-simulation.svg
    :alt: version on PyPI
    :target: https://pypi.python.org/pypi/plate-simulation/

.. |status| image:: https://img.shields.io/pypi/status/plate-simulation.svg
    :alt: version status on PyPI
    :target: https://pypi.python.org/pypi/plate-simulation/

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/plate-simulation.svg
    :alt: Python versions
    :target: https://pypi.python.org/pypi/plate-simulation/

.. |precommit_ci| image:: https://results.pre-commit.ci/badge/github/MiraGeoscience/plate-simulation/develop.svg
    :alt: pre-commit.ci status
    :target: https://results.pre-commit.ci/latest/github/MiraGeoscience/plate-simulation/develop

.. |maintainability| image:: https://api.codeclimate.com/v1/badges/_token_/maintainability
   :target: https://codeclimate.com/github/MiraGeoscience/plate-simulation/maintainability
   :alt: Maintainability


plate-simulation
================
**plate-simulation** is a package for creating a specialized mesh, model and simulation for
a particular parameterization of the halfspace + overburden and plate geological setting.

.. contents:: Table of Contents
   :local:
   :depth: 3

Documentation
^^^^^^^^^^^^^
`Online documentation <https://mirageoscience-plate-simulation.readthedocs-hosted.com/en/latest/>`_


Installation
^^^^^^^^^^^^
**plate-simulation** is currently written for Python 3.10 or higher.

Install Conda
-------------

To install **plate-simulation**, you need to install **Conda** first.

We recommend to install **Conda** using `miniforge`_.

.. _miniforge: https://github.com/conda-forge/miniforge

Within a conda environment
--------------------------

You can install (or update) a conda environment with all the requires packages to run **plate-simulation**.
To do so you can directly run the **Install_or_Update.bat** file by double left clicking on it.

Install with conda
------------------

You can install the package using ``conda`` and the ``.lock`` files from a conda prompt:

.. code-block:: bash

  conda env create -n my-env -f environments/[the_desired_env].lock.yml

Install with PyPI
-----------------

You should not install the package from PyPI, as the app requires conda packages to run.
Still, you can install it in a conda environment without its dependencies (``--no-deps``).

From PyPI
~~~~~~~~~

To install the **plate-simulation** package published on PyPI:

.. code-block:: bash

    pip install -U --no-deps plate-simulation

From a Git tag or branch
~~~~~~~~~~~~~~~~~~~~~~~~
If the package is not on PiPY yet, you can install it from a Git tag:

.. code-block:: bash

    pip install -U --no-deps --force-reinstall https://github.com/MiraGeoscience/plate-simulation/archive/refs/tags/TAG.zip

Or to install the latest changes available on a given Git branch:

.. code-block:: bash

    pip install -U --no-deps --force-reinstall https://github.com/MiraGeoscience/plate-simulation/archive/refs/heads/BRANCH.zip

.. note::
    The ``--force-reinstall`` option is used to make sure the updated version
    of the sources is installed, and not the cached version, even if the version number
    did not change. The ``-U`` or ``--upgrade`` option is used to make sure to get the latest version,
    on not merely reinstall the same version. As the package is aimed to be in a **Conda environment**, the option ``--no-deps`` is used to avoid installing the dependencies with pip, as they will be installed with conda.

From a local copy of the sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you have a git clone of the package sources locally,
you can install **plate-simulation** from the local copy of the sources with:

.. code-block:: bash

    pip install -U --force-reinstall path/to/project_folder_with_pyproject_toml

Or in **editable mode**, so that you can edit the sources and see the effect immediately at runtime:

.. code-block:: bash

    pip install -e -U --force-reinstall path/to/project_folder_with_pyproject_toml

Setup for development
^^^^^^^^^^^^^^^^^^^^^
To configure the development environment and tools, please see `README-dev.rst`_.

.. _README-dev.rst: README-dev.rst

License
^^^^^^^
MIT License

Copyright (c) 2024-2025 Mira Geoscience

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Third Party Software
^^^^^^^^^^^^^^^^^^^^
The plate-simulation Software may provide links to third party libraries or code (collectively "Third Party Software")
to implement various functions. Third Party Software does not comprise part of the Software.
The use of Third Party Software is governed by the terms of such software license(s).
Third Party Software notices and/or additional terms and conditions are located in the
`THIRD_PARTY_SOFTWARE.rst`_ file.

.. _THIRD_PARTY_SOFTWARE.rst: docs/source/THIRD_PARTY_SOFTWARE.rst\

Trademarks
^^^^^^^^^^
"Python" and the Python logos are trademarks or registered trademarks of the Python Software Foundation.

Copyright
^^^^^^^^^
Copyright (c) 2024-2025 Mira Geoscience Ltd.

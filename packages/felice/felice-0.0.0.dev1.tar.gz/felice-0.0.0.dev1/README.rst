======
felice
======

Overview
--------

Create/autocomplete/format a python project and upload it to PyPI.

Installation
------------

To install ``felice``, you can use ``pip``. Open your terminal and run:

.. code-block:: bash

    pip install felice

Usage
-----

The ``felice`` package provides the functions ``main`` and ``run``. ``main`` provides the CLI. To familiarize us with ``felice`` it may be a good starting point to use the help option of main:

.. code-block:: bash

    # bash
    python3 -m felice -h

or

.. code-block:: python

    # python
    import felice
    felice.main(["-h"])

The arguments of ``main`` can also be used analogously on the function ``run`` (except for the flags ``-h`` and ``-V``).

.. code-block:: python

    # The following lines are all identical:
    felice.main(["--author", "John Doe", "path/to/project"])
    felice.main(["--author=John Doe", "path/to/project"])
    felice.main(["--author", "John Doe", "--", "path/to/project"])
    felice.run("path/to/project", author="John Doe")
    felice.run(author="John Doe", path="path/to/project")
    felice.run("path/to/project", author="John Doe", email=None)

If an option is not used (i.e. given the value ``None``) it defaults to the value provided in the ``default`` table in the included file ``config.toml`` (if existent).

.. code-block:: toml

    [default]
    author = "Johannes"
    description = ""
    email = "johannes-programming@mailfence.com"
    github = "johannes-programming"
    requires_python = "{preset} \\| {current}"
    v = "bump(2, 1)"
    year = "{current}"

    [general]
    root = ""

If that fails the arguments default to the empty string. The empty string itself usually results in skipping whatever steps required the information.
The ``general.root`` setting allows to change directory even before ``path`` is applied.
It is recommended to create a ``config.toml`` file inside the ``felice`` package before usage.

License
-------

This project is licensed under the MIT License.

Links
-----

* `Download <https://pypi.org/project/felice/#files>`_
* `Index <https://pypi.org/project/felice>`_
* `Source <https://github.com/johannes-programming/felice>`_
* `Website <http://www.felice.johannes-programming.online>`_

Credits
-------

* Author: `Johannes <http://www.johannes-programming.online>`_
* Email: `johannes-programming@mailfence.com <mailto:johannes-programming@mailfence.com>`_

Thank you for using ``felice``!
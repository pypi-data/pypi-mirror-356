# This file is part of IMAS-Python.
# You should have received the IMAS-Python LICENSE file with this project.
"""Support module to run imas as a module:

.. code-block:: bash
    :caption: Options to run imas CLI interface

    # Run as a module (implemented in imas/__main__.py)
    python -m imas

    # Run as "program" (see project.scripts in pyproject.toml)
    imas
"""

from imas.command.cli import cli

cli()

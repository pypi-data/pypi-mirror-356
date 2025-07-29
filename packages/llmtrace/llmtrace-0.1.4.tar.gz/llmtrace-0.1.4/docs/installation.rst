Installation
============

You can install LLMTrace using pip:

.. code-block:: bash

   pip install llmtrace

For additional features like the web dashboard and advanced evaluation metrics, install with extras:

.. code-block:: bash

   pip install "llmtrace[web,eval]"

For development, including linting and testing tools:

.. code-block:: bash

   pip install "llmtrace[dev]"

To install all optional dependencies, use:

.. code-block:: bash

   pip install "llmtrace[all]"

## Compatibility

LLMTrace is designed to be compatible with the following environments:

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Python Version
     - Linux (x86_64)
     - macOS (x86_64 / arm64)
     - Windows (WSL2)
   * - 3.9
     - ✅ Supported
     - ✅ Supported
     - ✅ Supported
   * - 3.10
     - ✅ Supported
     - ✅ Supported
     - ✅ Supported
   * - 3.11
     - ✅ Supported
     - ✅ Supported
     - ✅ Supported

.. note::
   **Apple Silicon (macOS arm64) Specifics:**
   While LLMTrace generally supports Apple Silicon, some underlying dependencies (like `aiosqlite` or `psycopg2` for PostgreSQL) might not always have pre-built binary wheels available for `arm64` on PyPI. If you encounter installation issues related to binary dependencies, you might need to install them from source or use the `--no-binary` flag during installation. For example, for `aiosqlite`:

   .. code-block:: bash

      pip install --no-binary :all: aiosqlite

   This forces pip to build the package from source, which requires appropriate build tools (e.g., Xcode Command Line Tools on macOS).

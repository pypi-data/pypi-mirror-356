Contributing
============

We welcome contributions to LLMTrace! If you're interested in contributing, please read our guidelines below.

How to Contribute
-----------------

1.  **Fork the repository**: Start by forking the LLMTrace repository on GitHub.
2.  **Clone your fork**: Clone your forked repository to your local machine.
3.  **Create a new branch**: Create a new branch for your feature or bug fix.
4.  **Make your changes**: Implement your changes, ensuring they adhere to our coding standards (PEP8, docstrings, etc.).
5.  **Write tests**: Add unit tests for your new features or bug fixes.
6.  **Run tests**: Ensure all tests pass.
7.  **Update documentation**: If your changes affect the API or functionality, update the relevant documentation.
8.  **Commit your changes**: Write clear and concise commit messages.
9.  **Push to your fork**: Push your changes to your fork on GitHub.
10. **Open a Pull Request**: Submit a pull request to the `main` branch of the original LLMTrace repository.

Coding Standards
----------------

*   **PEP8**: Follow the `PEP8` style guide for Python code.
*   **Docstrings**: All functions, classes, and modules should have comprehensive docstrings following the Google style (parsed by `Napoleon`).
*   **Type Hinting**: Use type hints for function arguments and return values.
*   **Testing**: Write `pytest` unit tests for all new features and bug fixes, including asynchronous tests with `pytest-asyncio`.

Setting up Development Environment
---------------------------------

It's recommended to use a virtual environment:

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate # On Windows: .venv\Scripts\activate
   pip install -e ".[dev,web,eval,sqlite_async,postgresql]" # Incluye todos los extras para desarrollo completo

Pre-commit Hooks
----------------

We use `pre-commit` hooks to ensure code quality. Install them after setting up your environment:

.. code-block:: bash

   pre-commit install

This will run linters (Black, Flake8, Isort) automatically before each commit.

Reporting Bugs
--------------

If you find a bug, please open an issue on our GitHub repository. Provide a clear description of the bug, steps to reproduce it, and expected behavior.

Feature Requests
----------------

We welcome feature requests! Open an issue on GitHub to suggest new features or improvements.

Thank you for contributing to LLMTrace!

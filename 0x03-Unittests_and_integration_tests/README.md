# ALX Python - Unit and Integration Testing

This project covers writing unit tests and integration tests for Python code, following best practices like mocking, patching, parameterization, and memoization.

## 🧪 Topics Covered

- **Unit testing** with `unittest`
- **Parameterization** using `parameterized` and `parameterized_class`
- **Mocking external requests** with `unittest.mock.patch` and `PropertyMock`
- **Testing decorators** like `@memoize`
- **Integration testing** using real logic while mocking only HTTP calls
- **PEP8 Compliance** with `pycodestyle` 2.5
- **Executable files**, proper **docstrings**, and **type annotations**

## 🧰 Key Modules

- `utils.py` — generic utility functions like:
  - `access_nested_map()`
  - `get_json()`
  - `memoize()`

- `client.py` — contains `GithubOrgClient` class for interacting with GitHub’s API.

- `fixtures.py` — provides static payloads for integration tests.

- `test_client.py` and `test_utils.py` — test files with:
  - Unit tests for each function/class
  - Integration tests for GitHub API logic

## ✅ Requirements

- Python 3.7 (Ubuntu 18.04 LTS)
- All files must:
  - Start with `#!/usr/bin/env python3`
  - Be executable (`chmod +x file.py`)
  - End with a newline
  - Follow `pycodestyle` (version 2.5)
  - Include full docstrings and type hints

## 🧪 Running Tests

```bash
python3 -m unittest discover 0x03-Unittests_and_integration_tests

[[_TOC_]]

## 1. Python Starter Code

- Python Starter Code comes with the basic template that can be used a starting
  point for projects.
- Aligned to `Visual Studio Code` as the editor
- Dependencies are managed using `poetry` library
- Uses `black` as the default formatter
- Uses `pytest` library for unit testing
- Uses `tox` library for performing testing under multiple environments. Runs
  the unit tests on following python environments
  - python 3.9
  - python 3.10 and performs the following linters check
  - flake8
  - `mypy`
  - `pydocstyle`

## 2. Folder Structure

```
python_starter_code
 ┣ .github
 ┃ ┗ workflows
 ┃ ┃ ┣ build_and_publish_internal_pypi.yml # Pipeline to build and publish packages to Internal PyPI server
 ┃ ┃ ┣ build_and_publish_public.yml        # Pipeline to build and publish packages to PyPI server
 ┃ ┃ ┗ upload_artifact_sample.yml          # Pipeline to build packages
 ┣ .vscode
 ┃ ┣ extensions.json                       # Recommended VS Code Extensions
 ┃ ┗ settings.json                         # Recommended VS Code Settings
 ┣ docs
 ┃ ┣ Build and Publish to PyPI.md          # Steps to build and publish packages to PyPI Server
 ┃ ┗ Hosting Internal PyPI and Publish.md  # Steps to build and publish packages to Internal PyPI Server
 ┣ src
 ┃ ┗ python_sample_03_08_2023
 ┃ ┃ ┣ basic_math.py                       # Basic mathematical operations
 ┃ ┃ ┗ __init__.py
 ┣ tests
 ┃ ┣ conftest.py                           # Configuration file for pytest library
 ┃ ┗ test_math_operations.py               # Unit tests for mathematical operations
 ┣ .gitignore                              # Files to exclude from version control tracking
 ┣ LICENSE                                 # LICENSE file
 ┣ poetry.lock                             # Dependencies file
 ┣ pyproject.toml                          # Configuration file for poetry library
 ┣ README.md                               # Documentation about the repo
 ┣ tox.ini                                 # Configuration file for tox library
 ┗ version-history.md                      # Version history details of the repo
```

## 3. Install Poetry

1.  Poetry is a CLI tool that needs a Python interpreter to run
2.  It is recommended to install poetry in an isolated environment which can be
    done using **`pipx​`**
    > `python –m pip install pipx-in-pipx --user`
3.  To install poetry, run
    > `pipx install poetry`

## 4. Creating and activating Virtual Environment​

1.  Poetry can create virtual environments for a project and automatically
    activate it during first time.
    1. To create a virtual environment,
       > `poetry config virtualenvs.in-project true`
    2. To activate the virtual environment,
       > poetry shell
    3. To install the dependencies,
       > poetry install
    4. Run the below command to update to latest dependencies and rewrite the
       lock file​
       > poetry update

## 5. Recommended Extensions and VSCode Settings

The template comes with the recommended VS Code extensions that can be installed
as follows.

1. Click on the Extensions icon in the Activity Bar on the side of the window or
   use the keyboard shortcut Ctrl+Shift+X (Windows/Linux) or Cmd+Shift+X (Mac)
   to open the Extensions view.
2. In the Extensions view, type the name of the extension you want to install in
   the search bar.
3. Find the extension in the search results, and click the "Install" button next
   to it. Wait for the installation process to complete.

extensions.json

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.flake8",
    "ms-python.vscode-pylance",
    "ms-python.pylint",
    "ms-python.mypy-type-checker",
    "njpwerner.autodocstring",
    "littlefoxteam.vscode-python-test-adapter",
    "ms-vscode.test-adapter-converter",
    "hbenl.vscode-test-explorer",
    "yzhang.markdown-all-in-one",
    "tamasfe.even-better-toml",
    "mhutchie.git-graph",
    "eamodio.gitlens"
  ]
}
```

settings.json

```json
{
  "terminal.integrated.defaultProfile.windows": "Command Prompt",
  "editor.rulers": [100],
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "ms-python.black-formatter",
  "black-formatter.args": ["--line-length", "100"],
  "flake8.args": ["--max-line-length=100", "--extend-ignore=W503"]
}
```

## 6. tox.ini file

```ini
[tox]
description = Run CI actions with tox
env_list =
    py39, lint, vulnerabilities
minversion = 4.11.3

[testenv]
description = Run the tests with pytest
changedir = {tox_root}/tests
deps =
    pytest
    pytest-html
    pytest-cov
commands =
    pytest
parallel_show_output=True

[testenv:lint]
description = Run Linting
basepython = 3.9
changedir = {tox_root}
deps =
    flake8
    mypy
    pydocstyle
commands =
    flake8 src tests --max-line-length=100 --extend-ignore=W503
    mypy src tests
    pydocstyle src tests
parallel_show_output=True

[testenv:vulnerabilities]
description = Check for vulnerabilities
basepython = 3.9
changedir = {tox_root}
deps =
    poetry
    poetry-audit-plugin
commands =
    poetry audit
parallel_show_output=True
```

## 7. `pyproject.toml`

```toml
[tool.poetry]
name = "python_sample_03_08_2023"
version = "0.1.2"
description = "template python project to get started"
authors = ["Soliton"]
readme = "README.md"
packages = [{ include = "*", from = "src" }]

[tool.poetry.dependencies]
python = "^3.9"

[tool.poetry.group.dev.dependencies]
mypy = "^1.6.1"
flake8 = "^6.1.0"
pydocstyle = "^6.3.0"
tox = "^4.11.4"
poetry-audit-plugin = "^0.3.0"

[tool.poetry.group.test.dependencies]
pytest = "^7.4.3"
pytest-html = "^4.0.2"
pytest-cov = "^4.1.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.mypy]
ignore_missing_imports = true

[tool.flake8]
max-line-length = 100
extend-ignore = "W503"

[tool.pytest.ini_options]
addopts = [
        "--verbose",
        "--cov=python_sample_03_08_2023",
        "--cov-report=html:.pytest_results/coverage_report",
        "--cov-report=xml:.pytest_results/coverage_report/coverage.xml",
        "--html=.pytest_results/test_report.html",
        "--self-contained-html"
    ]
markers = [
        "multiply: tests to validate multiplication",
        "zerodivision: tests to validate division"
    ]
```

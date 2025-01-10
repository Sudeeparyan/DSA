# Version history for Python Project Template

[[_TOC_]]

## Version 0.3.0

### Contributors of 0.3.0

1. Abishlal Nelson

### Reviewers of 0.3.0

1. Karthick Shanmuga Rao
2. Karvendan Velusamy
3. Shangar Arivazhagan
   
### Fixes of 0.3.0

1. Update Poetry installation command in the Python CI pipeline template by adding the flags `--without test,dev`, `--sync --no-interaction`and `--no-interaction`.
2. Update `mypy` command in `tox.ini` by adding `--install-types` and `--non-interactive` flags.
3. Update `tox.ini` with `skip_install` and `allowlist_externals` configurations.
4. Add Python version as a variable in the CI pipeline file.

## Version 0.2.0

### Contributors of 0.2.0

1. Shangar Arivazhagan

### Reviewers of 0.2.0

1. Karthick Shanmuga Rao
2. Karvendan Velusamy
3. Nanthagopal Eswaran
4. Santhosh Manoharan
5. Namratha Balakrishna
6. Ramkumar Palaniappan Saravanan

### Features of 0.2.0

1. Remove code profile and use extensions and settings json (Applying code
   profile overrides other settings and extensions available already)
2. HTML and Coverage report generation for Test Automation

### Fixes of 0.2.0

1. Update maximum line length to 100 commonly across all places (extensions and
   linters)
2. Update `Pytoml`
   1. Included `Pytest` Report features (HTML and Coverage)
   2. Added settings for `pytest` execution (HTML and Coverage)
3. Minor fixes in tox settings (base python version)
4. Updated depreciated warnings settings with corresponding extensions

## Version 0.1.0

### Contributors of 0.1.0

1. Karthick Shanmuga Rao
2. Karvendan Velusamy
3. Nanthagopal Eswaran
4. Santhosh Manoharan

### Reviewers of 0.1.0

1. Karthick Shanmuga Rao
2. Karvendan Velusamy
3. Nanthagopal Eswaran
4. Santhosh Manoharan
5. Shangar Arivazhagan

### Features of 0.1.0

1. Recommended Code Editor: VS Code
2. Linters
   1. `mypy` (from vs code settings and python package)
   2. `pydocstyle` (from vs code settings and python package)
   3. `flake8` (from vs code settings and python package)
3. Code Formatters: Black (from vs code extension)
4. Dependency and Package Management: Poetry
5. CI Pipeline (with and without self hosted runner)
6. Test Automation
   1. `Pytest`
   2. `tox`
7. VS Code extensions and settings as code profile

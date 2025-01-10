# Build and Publish to PyPI

1. Register for a PyPI account
2. Create a API Token
3. Add PyPI token to poetry config

   > `poetry shell`

   and

   > `poetry config pypi-token.pypi your-api-token`

4. Build wheel file
   > poetry build -f wheel
5. Publish
   > poetry publish

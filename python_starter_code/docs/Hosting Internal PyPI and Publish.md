# Publishing Packages to Internal PyPI Server

## Setting up Internal PyPI Server

1. Install `pypiserver` in any station
   > `pip install pypiserver`
2. Start hosting the `internal_pypi` folder at <http://localhost:8090>
   > `pypi-server run -p 8090 -P . -a . --hash-algo sha256 \\192.168.0.12\Userarea\Karthick\internal_pypi`
3. After hosting the `internal_pypi` at localhost anyone can publish to the
   `internal_pypi` using the machine's ip address or host name. Example:
   <http://192.168.0.105:8090/> or <http://CBE-DLT-467.solitontech.local:8090/>

Note: It is recommended to use the host name since the IP address might change

## Publishing the Package

1. Add poetry config to add the repo(any of the below two options)

   > `poetry config --local repositories.internal_pypi http://192.168.0.105:8090`

   or

   > `poetry config --local repositories.internal_pypi http://CBE-DLT-467.solitontech.local:8090`

2. Publish
   > `poetry publish --repository internal_pypi`

## Installing from the Internal PyPI

1. Activate any `venv`
   > poetry shell
2. Add the PyPI reference to look for packages
   > `poetry source add --secondary internal_pypi http://192.168.0.105:8090/simple`
3. Install the package 'python_sample_03_08_2023'
   > poetry add python_sample_03_08_2023

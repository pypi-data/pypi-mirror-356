# flake8-all-not-strings
![PyPI data-understand](https://img.shields.io/pypi/v/flake8-all-not-strings)
![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)
![versions](https://img.shields.io/pypi/pyversions/flake8-all-not-strings)
![Downloads](https://static.pepy.tech/badge/flake8-all-not-strings)

[![Python Linting](https://github.com/ggupta2005/flake8-all-not-strings/actions/workflows/python-linting.yml/badge.svg)](https://github.com/ggupta2005/flake8-all-not-strings/actions/workflows/python-linting.yml)
[![Run Python Unit Tests](https://github.com/ggupta2005/flake8-all-not-strings/actions/workflows/python-unit-tests.yml/badge.svg)](https://github.com/ggupta2005/flake8-all-not-strings/actions/workflows/python-unit-tests.yml)

[![CodeFactor](https://www.codefactor.io/repository/github/ggupta2005/flake8-all-not-strings/badge)](https://www.codefactor.io/repository/github/ggupta2005/flake8-all-not-strings)

Flake8 plugin that checks that the all the elements defined in the `__all__` list are strings. Sometimes the flake8 doesn't throw error from the `__init__.py` if the modules under `__all__` are not strings.

Example below of an `__init__.py` file which should throw an error:-
```
from some_module import some_function 
__all__ = [
      some_function
]
```

Example below of an `__init__.py` file which should not throw an error:-
```
from some_module import some_function 
__all__ = [
      'some_function'
]
```

## Installation
```
pip install flake8-all-not-strings
```

## Flake8 codes
| Code | description |
|----------|----------|
| ANS100 | '<<some_module_name>>' import under __all__ is not a string. |

## Testing
In order to run unit tests under the `tests/` directory you can do the following steps:-

### Install editable version of `flake8-all-not-strings` from the top level directory
```
pip install -e .
```

### Install `pytest`
```
pip install pytest
```

### Run tests
Change to `tests/` directory and run tests using `pytest`
```
cd tests/
pytest
```
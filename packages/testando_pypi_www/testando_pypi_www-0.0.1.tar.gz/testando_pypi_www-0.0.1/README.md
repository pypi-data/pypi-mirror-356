# my_test_pypi_www

A test package for PyPI publishing demonstration.

## Installation

```bash
pip install my_test_pypi_www
```

## Usage

```python
from my_test_pypi_www import my_func

my_func()
```

## Development

To install in development mode:

```bash
pip install -e .
```

## Building and Publishing

1. Build the package:
```bash
python -m build
```

2. Upload to PyPI (you'll need to create an account first):
```bash
python -m twine upload dist/*
```

## License

MIT License 
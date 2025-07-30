# MoaM

A placeholder Python package ready for distribution on PyPI and conda-forge.

## Installation

### From PyPI

```bash
pip install MoaM
```

### From source

```bash
git clone https://github.com/ahe6/MoaM.git
cd MoaM
pip install -e .
```

## Usage

```python
import MoaM

print(MoaM.hello())  # Output: Hello from MoaM!
```

## Development

To install development dependencies:

```bash
pip install -e ".[dev]"
```

## Building and Publishing

### Building the package

```bash
python -m build
```

### Publishing to PyPI

First, install twine:

```bash
pip install twine
```

Then upload to PyPI:

```bash
twine upload dist/*
```

### Publishing to conda-forge

1. Fork https://github.com/conda-forge/staged-recipes
2. Create a new branch for your recipe
3. Add your recipe in `recipes/MoaM/meta.yaml`
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
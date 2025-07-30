# IDA Domain

[![PyPI version](https://badge.fury.io/py/ida-domain.svg)](https://badge.fury.io/py/ida-domain)
[![Python Support](https://img.shields.io/pypi/pyversions/ida-domain.svg)](https://pypi.org/project/ida-domain/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project provides a **Domain Model** for IDA Pro, allowing seamless interaction with IDA SDK components via Python.

## 🚀 Features

- **Domain Model Interface**: Clean, Pythonic API on top of IDA Python
- **Fully compatible with IDA Python SDK**: Can be used alongside the IDA Python SDK
- **Easy Installation**: Simple pip install from PyPI
- **Documentation**: API reference and usage examples
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 📦 Installation

### Prerequisites

Set the `IDADIR` environment variable to point to your IDA installation directory:

```bash
export IDADIR="[IDA Installation Directory]"
```

**Example:**
```bash
export IDADIR="/Applications/IDA Professional 9.1.app/Contents/MacOS/"
```

> **Note:** If you have already installed and configured the `idapro` Python package, setting `IDADIR` is not required.

### Install from PyPI

```bash
pip install ida-domain
```

## 🎯 Usage Example

Here is an example showing how to use IDA Domain to analyze a binary:

```python
<!-- EXPLORE_DATABASE_EXAMPLE_PLACEHOLDER -->
```

## 📖 Documentation

Complete documentation is available at: **https://hexrayssa.github.io/ida-domain/**

- **API Reference**: Documentation of available classes and methods
- **Installation Guide**: Detailed setup instructions
- **Examples**: Usage examples for common tasks - [View Examples](https://hexrayssa.github.io/ida-domain/examples.html)
- **Getting Started**: Basic guide for new users

For more examples, visit: https://hexrayssa.github.io/ida-domain/examples.html

<!-- GITHUB_ONLY_START -->

## 🛠️ Development

### Install from Source

```bash
git clone https://github.com/HexRaysSA/ida-domain.git
cd ida-domain
pip install .
```

### Development Installation

For development, a UV (see https://docs.astral.sh/uv/) based workflow is recommended:

```bash
git clone https://github.com/HexRaysSA/ida-domain.git
cd ida-domain
uv sync --extra dev
uv run pre-commit install
```

## 🧪 Testing

Run the test suite using pytest:

```bash
uv sync --extra dev
uv run pytest
```

## 📚 Documentation

The IDA Domain API documentation is built with Sphinx and includes:

- **API Reference**: Documentation of available classes and methods
- **Installation Guide**: Setup instructions
- **Examples**: Usage examples for common tasks
- **Getting Started**: Basic guide for new users

### Building Documentation Locally

To build the documentation locally:

```bash
cd docs
uv run --with sphinx --with sphinx-rtd-theme --with sphinx-autodoc-typehints make html
```

The generated documentation will be available at `docs/_build/html/index.html`.

### Online Documentation

The latest documentation is available at: https://hexrayssa.github.io/ida-domain/

## 📝 Examples

Check the `examples/` directory for usage examples:

```bash
python examples/analyze_database.py
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to:

- Report bugs and suggest features
- Submit pull requests with proper testing
- Set up your development environment with UV
- Generate and update documentation automatically

<!-- GITHUB_ONLY_END -->

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

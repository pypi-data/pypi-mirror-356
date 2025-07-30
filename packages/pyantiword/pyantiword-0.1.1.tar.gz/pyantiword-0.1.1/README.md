# pyantiword

A Python wrapper for [antiword](https://web.archive.org/web/20221207132720/http://www.winfield.demon.nl/) with the antiword binary and data files bundled for easy use in any environment.

## Features

- Bundles the `antiword` binary and required data files
- No external dependencies or system requirements
- Simple Python interface to extract text from `.doc` (Microsoft Word) files

## Installation

```sh
pip install pyantiword
```

## Usage

```python
from pyantiword.antiword_wrapper import extract_text

# Extract text from a .doc file
text = extract_text("path/to/document.doc")
print(text)
```

## Requirements

- Python 3.6+
- No external dependencies

## How it works

This package includes the `antiword` binary and its required data files. When you install `pyantiword`, everything you need is included—no need to install antiword separately.

## Building and Publishing

To be able to build, for now, the ``build_antiword.sh`` script only only **guaranteed** to work on Ubuntu, with Python 3.6 and above.
In the future, we might make this more stable with a mandatory virtual environment step, or a docker container.

To build and publish `pyantiword` to PyPI, follow these steps:

### 1. Build the antiword binary

Before packaging, ensure the `antiword` binary and data files are present by running:

```sh
./build_antiword.sh
```

### 2. Install build tools

If you haven't already, install the required Python packaging tools:

```sh
pip install --upgrade build twine
```

### 3. Build the package

This will create both a source distribution and a wheel in the `dist/` directory:

```sh
python -m build
```

### 4. Publish to PyPI

Upload the package to [PyPI](https://pypi.org/) using Twine:

```sh
twine upload dist/*
```

You will need a PyPI account and your credentials to complete this step. Your credentials being, most likely, your API token.

---

**Note:**  
Always ensure the `antiword` binary and data files are up-to-date in the `pyantiword/` directory before building the package.


## License

[MIT License](LICENSE)

## Author

Vitor Hugo Moreira Reis

## Links

- [PyPI Project](https://pypi.org/project/pyantiword/)
- [antiword homepage (on web archive)](https://web.archive.org/web/20221207132720/http://www.winfield.demon.nl/)
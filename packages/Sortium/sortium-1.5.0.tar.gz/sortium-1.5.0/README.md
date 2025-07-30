# Sortium

**Sortium** is a Python utility that automatically organizes files in a directory based on their type (e.g., Images, Documents, Videos, etc.) and optionally by their last modified date.

---

## Table of Contents

* [Features](#features)
* [Installation](#installation)
  * [PyPI](#pypi)
* [Running Tests](#running-tests)
* [Author](#author)
* [License](#license)
* [Contributing](#contributing)
* [Documentation and Issues](#documentation-and-issues)

---

## Features

* Automatically organizes files into folders by type:
  * Images, Documents, Videos, Music, Others
* Optional sorting by last modified date within each category
* Optional flattening of subdirectories into a single level before sorting

---

## Installation

### PyPI

To install from PyPI:

```bash
pip install sortium
```

To install from source:

```bash
git clone https://github.com/Sarthak-G0yal/Sortium.git
cd Sortium
pip install -e .
```

---

## Running Tests

To run the test suite with coverage reporting:

```bash
pytest src/tests --cov=src/sortium
```

Refer to the [Test Suite README](./src/tests/README.md) for test structure and guidelines.

---

## Author

**Sarthak Goyal**
Email: [sarthakgoyal487@gmail.com](mailto:sarthakgoyal487@gmail.com)

---

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

---

## Contributing

Contributions are welcome.

To contribute:

1. Fork the repository
2. Create a new branch (`feature/my-feature` or `fix/my-fix`)
3. Write tests for your changes
4. Commit with clear, conventional messages
5. Open a pull request with a description of your changes

Please follow the [Conventional Commits](https://www.conventionalcommits.org/) specification. Ensure all code is linted and tested before submitting.

---

## Documentation and Issues

This project uses [Sphinx](https://www.sphinx-doc.org/) for documentation.

* To build the documentation locally:

  ```bash
  cd docs
  make html
  ```

  View the generated files at `docs/_build/html/index.html`.

* Online documentation: [View Documentation](https://sarthak-g0yal.github.io/Sortium)

* For issues and feature requests: [Open an issue](https://github.com/Sarthak-G0yal/Sortium/issues)

---
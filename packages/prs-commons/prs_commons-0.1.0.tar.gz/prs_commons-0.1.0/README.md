# PRS Commons

A Python library containing common utilities and shared code for PRS microservices.

## Installation

### From Source (Development)

For development, clone and install in editable mode:

```bash
git clone https://<token>@github.com/IshaFoundationIT/prs-facade-common.git
cd prs-facade-common
pip install -e ".[dev]"  # Install with development dependencies
```

### From Private Package Repository

Add your private package repository to pip configuration and install:

```bash
# Configure pip to use your private repository
pip config set global.extra-index-url https://your.private.registry.com/simple/

# Install the package
pip install prs-commons
```

## Usage

```python
from prs_commons import MyClass

# Create an instance
obj = MyClass("User")

# Use the instance
print(obj.greet())  # Output: Hello, User!

# Get version
print(f"Library version: {MyClass.version()}")
```

## Development

### Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/) (recommended) or pip

### Setup

1. Clone the repository:
   ```bash
   git clone https://<token>@github.com/IshaFoundationIT/prs-facade-common.git
   cd prs-facade-common
   ```

2. Install dependencies:
   ```bash
   # Using Poetry
   poetry install --with dev

   # Or using pip
   pip install -e ".[dev]"
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=prs_commons --cov-report=term-missing
```

## Publishing New Versions

### Prerequisites

1. Set up your `~/.pypirc` file with your GitHub token:
   ```ini
   [distutils]
   index-servers =
       github

   [github]
   repository = https://upload.pypi.org/legacy/
   username = __token__
   password = your_github_token_here
   ```

   Replace `your_github_token_here` with a GitHub Personal Access Token with `write:packages` scope.

2. Update the version in `pyproject.toml`

3. Build the package:
   ```bash
   python -m build
   ```

4. Publish to GitHub Package Registry:
   ```bash
   python -m twine upload --repository github dist/*
   ```

### Installing from GitHub Package Registry

1. Create a personal access token with `read:packages` scope
2. Configure pip to use your token:
   ```bash
   pip install --index-url https://USERNAME:TOKEN@pkgs.dev.azure.com/ORGANIZATION/PROJECT/_packaging/REPOSITORY/pypi/simple/ --no-deps PACKAGE_NAME
   ```

   Or add to your `pip.conf`:
   ```ini
   [global]
   extra-index-url = https://USERNAME:TOKEN@pkgs.dev.azure.com/ORGANIZATION/PROJECT/_packaging/REPOSITORY/pypi/simple/
   ```

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and pre-commit checks
4. Submit a pull request

## License

MIT

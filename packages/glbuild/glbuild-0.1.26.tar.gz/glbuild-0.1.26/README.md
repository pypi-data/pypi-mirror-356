# glbuild

A lightweight library and CLI tool for historical GitLab build data and logs collection.

## Requirements

- [Python](https://www.python.org/downloads/) >= 3.10
- [Poetry](https://python-poetry.org/)

## Getting Started

Install dependencies

```bash
poetry install
```

Access virtual environment

```bash
poetry shell
```

Install pre-commit hook for static code analysis

```bash
pre-commit install
```

## Usage

### Installation

Install the `glbuild` package using [pip](https://pip.pypa.io/en/stable/installation/)

```bash
pip install glbuild
```

### Python library

```python
import glbuild

glb = glbuild.GitLabBuild(base_url="https://gitlab.com", token="******", projects=[1538, 5427])

glb.start(n_last=100)
```

### Command Line Interface (CLI)

```bash
glbuild --base-url https://gitlab.com --token ****** --output ./data --n-last 100 --project 1538 --project 5427
```

Contracted CLI command

```bash
glbuild -b https://gitlab.com -t ****** -o ./data -n 100 -p 1538 -p 5427
```

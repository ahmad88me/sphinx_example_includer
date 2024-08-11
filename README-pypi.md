# Sphinx Example Includer

[![PyPI version](https://badge.fury.io/py/sphinx-example-includer.svg)](https://badge.fury.io/py/sphinx-example-includer)

Build Sphinx docs for the package's source code and 
automatically gaenerate .rst files from examples folder for the sphinx documentation

![examples screenshot](https://github.com/ahmad88me/sphinx_example_includer/blob/main/examples-screenshot.png?raw=true)
## Installation
```
pip install sphinx_example_includer
```

## Usage
```
usage: Sphinx Example Includer [-h] [--debug] [--info] [--overwrite] [--files FILES [FILES ...]] [--dest-dir DEST_DIR]
                               [--toc-fname TOC_FNAME] [--build] [--conf CONF] [--docs-dir DOCS_DIR] [--project-dir PROJECT_DIR]
                               [--index INDEX]

A Sphinx docs generation tool

options:
  -h, --help            show this help message and exit
  --debug               Showing debug messages
  --info                Showing info messages
  --overwrite           Overwrite files that already exists
  --files FILES [FILES ...]
                        one or more files to be
  --dest-dir DEST_DIR   The output directory
  --toc-fname TOC_FNAME
                        The name of the toc file
  --build               Build Sphinx docs.
  --conf CONF           The configuration file (e.g., pyproject.toml)
  --docs-dir DOCS_DIR   The directory of the documentation
  --project-dir PROJECT_DIR
                        The path of the project's code
  --index INDEX         The name of the index file.

```

## Example
```
python -m sphinx_example_includer --info --build --project src --files examples/*example*.py --overwrite
```

## How to use it

### Assumptions
1. You have your example source code in `examples/`
2. Your code is documented so Sphinx can generate the docs for you.

### Generating the docs
1. Install the package `sphinx_example_includer`
2. In the directory of your project (that you want to document), run the command 
`python -m sphinx_example_includer --build`. Note that the `--build` is the flag responsible for generating 
the docs. You can also specify the directory of your code with the flag `--project`.
3. Include the examples into the docs. This can be done by running the same command with 
`--files` flag and you can choose multiple files using a pattern as shown in the example above.

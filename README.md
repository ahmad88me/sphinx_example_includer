# Sphinx Example Includer

![tests](../../actions/workflows/python-package.yml/badge.svg)


Automatically Generate .rst files from examples folder for the sphinx documentation


## Installation
```
pip install sphinx_example_includer
```

## Usage
```
options:
  -h, --help            show this help message and exit
  --debug               Showing debug messages
  --overwrite           Overwrite files that already exists
  --files FILES [FILES ...]
                        one or more files to be
  --dest_dir DEST_DIR   The output directory
```

## Example
```
python -m sphinx_example_includer  --files examples/*example*py --overwrite --dest docs/source/examples 
```


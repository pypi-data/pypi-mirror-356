# Git Timesheet Generator Examples

This directory contains examples of how to use the Git Timesheet Generator.

## Basic Usage

The `basic_usage.py` script demonstrates how to use the Git Timesheet Generator as a Python library:

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
pip install -e ..

# Run the example
python basic_usage.py
```

## Command-Line Examples

The `cli_examples.md` file contains examples of using the `ggts` command-line interface for various common tasks.

## Configuration Examples

The `config_examples.md` file provides examples of configuration files for the Git Timesheet Generator.

## Sample Outputs

This directory also includes sample outputs in different formats:

- `timesheet.txt`: Sample text output
- `timesheet.csv`: Sample CSV output
- `timesheet.md`: Sample markdown output

To generate these samples yourself, you can run:

```bash
# Generate text output
ggts --since="1 month ago" --output=text --output-file=timesheet.txt

# Generate CSV output
ggts --since="1 month ago" --output=csv --output-file=timesheet.csv

# Generate markdown output
ggts --since="1 month ago" --output=markdown --output-file=timesheet.md
```
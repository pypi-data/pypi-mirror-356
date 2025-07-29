# Git Timesheet Generator

A Python package to generate git timesheets from commit history, specifically filtering for commits by a particular author.

## Overview

This tool analyzes git commit history across multiple repositories and:

- Filters commits by author name/email
- Estimates time spent on each commit (in 15-minute increments)
- Adjusts time based on commit message keywords
- Groups work by day and week
- Formats output as a readable timesheet

## Requirements

- Python 3.8+
- pytz library
- click library

## Installation

### From PyPI

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
pip install git-timesheet
```

### From Source

```bash
# Clone the repository
git clone https://github.com/mcgarrah/git-timesheet.git
cd git-timesheet

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .
```

## Configuration

The tool supports configuration files to set default values. It looks for configuration files in the following locations (in order of precedence):

1. `.ggtsrc` in the current directory
2. `ggts.ini` in the current directory
3. `.ggtsrc` in the user's home directory
4. `ggts.ini` in the user's `.config` directory
5. `config.ini` in the user's `.config/git-timesheet` directory

You can create a configuration file using the `ggts init` command, or manually create one with the following format:

```ini
[defaults]
# Author pattern to filter commits
author = michael mcgarrah

# Default timezone for dates
timezone = US/Eastern

# Minutes between commits to consider them part of the same work session
session_timeout = 60
```

Command-line arguments always override values from configuration files.

## Usage

```bash
# Generate a timesheet (default command)
ggts [OPTIONS]
# or explicitly
ggts generate [OPTIONS]

# Initialize configuration
ggts --init
# or
ggts init
```

### Options

- `--base-dir PATH`: Base directory containing git repositories (default: current directory)
- `--since DATE`: Show commits more recent than a specific date (e.g., "2 weeks ago")
- `--until DATE`: Show commits older than a specific date
- `--repos REPO`: Specific repository names to include (can be used multiple times)
- `--output FORMAT`: Output format (text, csv, markdown, or md, default: text)
- `--author PATTERN`: Filter commits by author (default from config or "mcgarrah")
- `--timezone TIMEZONE`: Timezone for dates (default from config or "UTC")
- `--output-file PATH`: Write output to file instead of stdout
- `--session-timeout MINUTES`: Minutes between commits to consider them part of the same work session (default from config or 60)

## Examples

### Generate timesheet for the last 2 weeks

```bash
# Using default command
ggts --since="2 weeks ago"
# or explicitly
ggts generate --since="2 weeks ago"
```

### Generate timesheet for specific repositories

```bash
ggts generate --repos food_service_nutrition --repos food-intelligence-app --since="1 month ago"
```

### Generate timesheet for a specific date range

```bash
ggts generate --since="2023-01-01" --until="2023-01-31"
```

### Generate timesheet with specific author pattern

```bash
ggts generate --author="michael mcgarrah" --since="2 weeks ago"
```

### Generate timesheet in US Eastern timezone

```bash
ggts generate --since="1 month ago" --timezone="US/Eastern"
```

### Generate CSV output for spreadsheet import

```bash
ggts generate --since="1 month ago" --output=csv --output-file=timesheet.csv
```

### Generate markdown output for pretty formatting

```bash
ggts generate --since="1 month ago" --output=markdown --output-file=timesheet.md
```

### Initialize configuration

```bash
# Using the dedicated command
ggts init
# or using the flag
ggts --init
```

## Output Formats

### Text Format

Plain text output organized by weeks and days, showing detailed commit information with timezone abbreviations.

### CSV Format

Comma-separated values format suitable for importing into spreadsheet applications like Excel or Google Sheets. Includes timezone information for each entry.

### Markdown Format

Pretty markdown format with tables organized by week, suitable for viewing in markdown readers or converting to HTML. Includes time ranges and timezone abbreviations for each task to better understand work sessions.

## Time Estimation Logic

- Base time: 15 minutes per commit
- Bug fixes/issues: +15 minutes
- New features/implementations: +30 minutes
- Refactoring/improvements: +15 minutes
- Commits close together (within 60 minutes by default) are considered part of the same work session

## Timezone Support

The tool supports various timezone formats:

- IANA timezone names (e.g., "America/New_York")
- Common US timezone aliases (e.g., "US/Eastern")
- Short timezone abbreviations (e.g., "EST", "EDT")
- Prefixed short timezone abbreviations (e.g., "US/EST")

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/mcgarrah/git-timesheet.git
cd git-timesheet

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Testing

The project includes a comprehensive test suite using pytest. To run the tests:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=git_timesheet

# Run a specific test file
pytest tests/test_timezone.py
```

### Test Structure

- **Unit Tests**: Test individual functions in isolation
  - `test_timezone.py`: Tests for timezone conversion and abbreviation
  - `test_git_operations.py`: Tests for git repository detection and log retrieval
  - `test_formatting.py`: Tests for output formatting functions

- **Integration Tests**: Test the entire workflow
  - `test_integration.py`: End-to-end tests using temporary git repositories

### Building Documentation

```bash
pip install -e ".[docs]"
cd docs
make html
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
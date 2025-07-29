# Git Timesheet Generator CLI Examples

This document provides examples of using the `ggts` command-line interface for various common tasks.

## Basic Usage

### Initialize Configuration

Create a configuration file with your default settings:

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
pip install git-timesheet

# Initialize configuration
ggts --init
# or
ggts init
```

This will create a configuration file at `~/.config/git-timesheet/config.ini` with your default settings.

### Generate a Timesheet for the Last 2 Weeks

```bash
# Using default command
ggts --since="2 weeks ago"
# or explicitly
ggts generate --since="2 weeks ago"
```

### Generate a Timesheet for a Specific Date Range

```bash
ggts generate --since="2023-01-01" --until="2023-01-31"
```

## Output Formats

### Generate CSV Output for Spreadsheet Import

```bash
ggts generate --since="1 month ago" --output=csv --output-file=timesheet.csv
```

### Generate Markdown Output for Documentation

```bash
ggts generate --since="1 month ago" --output=markdown --output-file=timesheet.md
```

## Repository Selection

### Generate Timesheet for Specific Repositories

```bash
ggts generate --repos project1 --repos project2 --since="1 month ago"
```

### Generate Timesheet for All Repositories in a Directory

```bash
ggts generate --base-dir=/path/to/projects --since="1 month ago"
```

## Author and Timezone Options

### Generate Timesheet for a Specific Author

```bash
ggts generate --author="John Doe" --since="2 weeks ago"
```

### Generate Timesheet in a Specific Timezone

```bash
ggts generate --since="1 month ago" --timezone="US/Pacific"
```

## Advanced Options

### Customize Session Timeout

```bash
ggts generate --since="1 month ago" --session-timeout=30
```

This changes how commits are grouped into work sessions (default is 60 minutes).

### Combine Multiple Options

```bash
ggts generate --repos project1 --since="2 weeks ago" --timezone="US/Eastern" --output=csv --output-file=project1_timesheet.csv
```

## Using Configuration Files

You can create multiple configuration files:

1. `.ggtsrc` in your current directory
2. `ggts.ini` in your current directory
3. `.ggtsrc` in your home directory
4. `ggts.ini` in your `.config` directory
5. `config.ini` in your `.config/git-timesheet` directory

Example configuration file:

```ini
[defaults]
author = John Doe
timezone = US/Eastern
session_timeout = 45
```

With this configuration, you can simply run:

```bash
ggts --since="2 weeks ago"
```

And it will use your configured defaults for author, timezone, and session timeout.
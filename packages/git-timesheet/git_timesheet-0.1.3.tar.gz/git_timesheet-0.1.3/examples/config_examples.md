# Git Timesheet Generator Configuration Examples

This document provides examples of configuration files for the Git Timesheet Generator.

## Configuration File Locations

The Git Timesheet Generator looks for configuration files in the following locations (in order of precedence):

1. `.ggtsrc` in the current directory
2. `ggts.ini` in the current directory
3. `.ggtsrc` in your home directory
4. `ggts.ini` in your `.config` directory
5. `config.ini` in your `.config/git-timesheet` directory

## Basic Configuration

A basic configuration file looks like this:

```ini
[defaults]
author = John Doe
timezone = US/Eastern
session_timeout = 60
```

## Configuration with Multiple Authors

If you work with multiple identities, you can create different configuration files for different projects:

**Project A: ~/projectA/.ggtsrc**
```ini
[defaults]
author = John Doe
timezone = US/Eastern
session_timeout = 60
```

**Project B: ~/projectB/.ggtsrc**
```ini
[defaults]
author = john.doe@company.com
timezone = US/Pacific
session_timeout = 45
```

## Configuration with Different Timezones

If you work across multiple timezones, you can specify different timezone formats:

```ini
[defaults]
author = John Doe
timezone = America/New_York  # IANA timezone name
session_timeout = 60
```

Or using US timezone aliases:

```ini
[defaults]
author = John Doe
timezone = US/Eastern  # US timezone alias
session_timeout = 60
```

Or using abbreviations:

```ini
[defaults]
author = John Doe
timezone = EST  # Timezone abbreviation
session_timeout = 60
```

## Creating Configuration Files

You can create a configuration file using the `ggts init` command, which will guide you through the process:

```bash
ggts init
```

Or you can manually create a configuration file in any of the supported locations.

## Using Configuration Files

Once you have a configuration file, you can simply run:

```bash
ggts generate --since="2 weeks ago"
```

And it will use your configured defaults for author, timezone, and session timeout.

You can still override any configured values by specifying them on the command line:

```bash
ggts generate --since="2 weeks ago" --author="Different Author" --timezone="UTC"
```
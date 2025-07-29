#!/usr/bin/env python3
import os
import sys
import click
from pathlib import Path
from datetime import datetime

from .config import get_config
from .git_utils import get_git_repos, get_git_log, estimate_time_spent
from .formatters import format_timesheet
from . import __version__

@click.command()
@click.version_option(version=__version__)
@click.option('--base-dir', help='Base directory containing git repositories (default: current directory)')
@click.option('--since', help='Show commits more recent than a specific date (e.g., "2 weeks ago")')
@click.option('--until', help='Show commits older than a specific date')
@click.option('--repos', multiple=True, help='Specific repository names to include (can be used multiple times)')
@click.option('--output', type=click.Choice(['text', 'csv', 'markdown', 'md']), 
              help='Output format (text, csv, markdown, or md)')
@click.option('--author', help='Filter commits by author')
@click.option('--timezone', help='Timezone for dates (e.g., "US/Eastern", "EST")')
@click.option('--output-file', help='Write output to file instead of stdout')
@click.option('--session-timeout', type=int, help='Minutes between commits to consider them part of the same work session')
@click.option('--init', is_flag=True, help='Initialize configuration file')
def cli(base_dir, since, until, repos, output, author, timezone, output_file, session_timeout, init):
    """Generate Git Timesheet - Create timesheets from git commit history"""
    if init:
        initialize_config()
        return
    
    # Generate timesheet (default behavior)
    generate_timesheet(base_dir, since, until, repos, output, author, timezone, output_file, session_timeout)

def initialize_config():
    """Initialize configuration file"""
    config_dir = Path.home() / '.config'
    config_file = config_dir / 'ggts.ini'
    
    if not config_dir.exists():
        config_dir.mkdir(parents=True, exist_ok=True)
        click.echo(f"Created directory: {config_dir}")
    
    if config_file.exists():
        overwrite = click.confirm(f"Configuration file already exists at {config_file}. Overwrite?", default=False)
        if not overwrite:
            click.echo("Aborted.")
            return
    
    author = click.prompt("Default author pattern", default="mcgarrah")
    timezone = click.prompt("Default timezone", default="UTC")
    session_timeout = click.prompt("Default session timeout (minutes)", default=60, type=int)
    
    config_content = f"""[defaults]
# Author pattern to filter commits
author = {author}

# Default timezone for dates (e.g., US/Eastern, EST, America/New_York)
timezone = {timezone}

# Minutes between commits to consider them part of the same work session
session_timeout = {session_timeout}
"""
    
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    click.echo(f"Configuration file created at {config_file}")
    click.echo("You can now run 'ggts' to create timesheets.")

def generate_timesheet(base_dir, since, until, repos, output, author, timezone, output_file, session_timeout):
    """Generate a timesheet from git commit history"""
    # Load configuration
    config = get_config()
    
    # Use config values as defaults if not provided via command line
    base_dir = base_dir or os.getcwd()
    output_format = output or 'text'
    author_filter = author or config['author']
    timezone_str = timezone or config['timezone']
    session_timeout_minutes = session_timeout or int(config['session_timeout'])
    
    # Get all git repositories in the base directory
    all_repos = get_git_repos(base_dir)
    
    # Filter repositories if specified
    if repos:
        filtered_repos = []
        for repo_name in repos:
            matching_repos = [r for r in all_repos if os.path.basename(r) == repo_name]
            filtered_repos.extend(matching_repos)
        repos_to_process = filtered_repos
    else:
        repos_to_process = all_repos
    
    if not repos_to_process:
        click.echo("No git repositories found.")
        return
    
    click.echo(f"Found {len(repos_to_process)} repositories.")
    
    # Collect time entries from all repositories
    all_time_entries = []
    for repo in repos_to_process:
        repo_name = os.path.basename(repo)
        click.echo(f"Processing {repo_name}...")
        commits = get_git_log(repo, since, until, author_filter)
        time_entries = estimate_time_spent(commits, repo_name, session_timeout_minutes)
        all_time_entries.extend(time_entries)
    
    # Sort all entries by date
    all_time_entries.sort(key=lambda x: x['date'])
    
    # Format timesheet
    timesheet = format_timesheet(all_time_entries, output_format, timezone_str, author_filter)
    
    # Output the timesheet
    if output_file:
        with open(output_file, 'w') as f:
            f.write(timesheet)
        click.echo(f"Timesheet written to {output_file}")
    else:
        click.echo(timesheet)

def main():
    cli()

if __name__ == '__main__':
    main()
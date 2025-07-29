#!/usr/bin/env python3
"""
Basic usage example for Git Timesheet Generator.

This example demonstrates how to use the git_timesheet package directly
in your Python code to generate timesheets.
"""

import os
from datetime import datetime, timedelta
from git_timesheet.git_utils import get_git_repos, get_git_log, estimate_time_spent
from git_timesheet.formatters import format_timesheet

def main():
    # Configuration
    base_dir = os.path.expanduser("~/github")  # Change this to your git repositories directory
    since = "1 week ago"
    author = "your-name"  # Change this to your name or email
    timezone = "US/Eastern"  # Change this to your timezone
    output_format = "text"  # Options: text, csv, markdown
    
    print(f"Searching for git repositories in {base_dir}...")
    
    # Get all git repositories in the base directory
    repos = get_git_repos(base_dir)
    print(f"Found {len(repos)} repositories.")
    
    # Collect time entries from all repositories
    all_time_entries = []
    for repo in repos:
        repo_name = os.path.basename(repo)
        print(f"Processing {repo_name}...")
        commits = get_git_log(repo, since=since, author=author)
        time_entries = estimate_time_spent(commits, repo_name, session_timeout_minutes=60)
        all_time_entries.extend(time_entries)
    
    # Sort all entries by date
    all_time_entries.sort(key=lambda x: x['date'])
    
    # Format timesheet
    timesheet = format_timesheet(all_time_entries, output_format, timezone, author)
    
    # Output the timesheet
    print(timesheet)

if __name__ == "__main__":
    main()
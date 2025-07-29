#!/usr/bin/env python3
import os
from datetime import datetime, timedelta
from collections import defaultdict
from .timezone_utils import convert_to_timezone, get_timezone_abbr

def format_timesheet(time_entries, output_format='text', timezone_str='UTC', author_filter='mcgarrah'):
    """Format time entries into a weekly timesheet."""
    if not time_entries:
        return "No git activity found in the specified time period."
        
    # Filter for entries with author_filter in author name or email
    if author_filter:
        filtered_entries = [entry for entry in time_entries 
                        if author_filter.lower() in entry['author_name'].lower() or 
                            author_filter.lower() in entry['author_email'].lower()]
        
        if not filtered_entries:
            return f"No git activity found for the specified author in the given time period."
            
        time_entries = filtered_entries
    
    # Convert dates to specified timezone
    for entry in time_entries:
        entry['date'] = convert_to_timezone(entry['date'], timezone_str)
    
    # Group by week and day
    weeks = defaultdict(lambda: defaultdict(list))
    for entry in time_entries:
        date = entry['date']
        week_start = (date - timedelta(days=date.weekday())).strftime('%Y-%m-%d')
        day = date.strftime('%Y-%m-%d')
        weeks[week_start][day].append(entry)
    
    if output_format == 'text':
        return format_text(weeks)
    elif output_format == 'csv':
        return format_csv(weeks, time_entries)
    elif output_format in ['markdown', 'md']:
        return format_markdown(weeks)
    else:
        return format_text(weeks)  # Default to text

def format_text(weeks):
    """Format timesheet as plain text."""
    result = []
    
    for week_start, days in sorted(weeks.items()):
        result.append(f"\\nWeek of {week_start}")
        result.append("=" * 80)
        
        week_total = 0
        for day, entries in sorted(days.items()):
            day_date = datetime.strptime(day, '%Y-%m-%d')
            day_name = day_date.strftime('%A')
            day_total = sum(entry['minutes'] for entry in entries)
            week_total += day_total
            
            result.append(f"\\n{day_name}, {day} - Total: {day_total/60:.2f} hours")
            result.append("-" * 80)
            
            # Group by repository
            repos = defaultdict(list)
            for entry in entries:
                repos[entry['repo']].append(entry)
            
            for repo, repo_entries in sorted(repos.items()):
                repo_name = os.path.basename(repo)
                repo_total = sum(entry['minutes'] for entry in repo_entries)
                result.append(f"\\n  {repo_name} - {repo_total/60:.2f} hours")
                
                for entry in repo_entries:
                    time_str = f"{entry['minutes']/60:.2f}h"
                    commit_time = entry['date'].strftime('%H:%M')
                    tz_abbr = get_timezone_abbr(entry['date'])
                    result.append(f"    {commit_time} {tz_abbr} - {time_str} - {entry['message'][:60]} ({entry['commit'][:7]}) - {entry['author_name']}")
            
        result.append(f"\\nWeek Total: {week_total/60:.2f} hours\\n")
        result.append("=" * 80)
    
    return "\\n".join(result).replace('\\n', '\n')

def format_csv(weeks, time_entries):
    """Format timesheet as CSV."""
    output = []
    
    # Write to string buffer
    output.append("Date,Day,Week,Start Time,Timezone,Duration (min),Duration (hours),Repository,Commit,Message,Author")
    
    for entry in sorted(time_entries, key=lambda x: x['date']):
        date = entry['date']
        week_start = (date - timedelta(days=date.weekday())).strftime('%Y-%m-%d')
        day_name = date.strftime('%A')
        date_str = date.strftime('%Y-%m-%d')
        time_str = date.strftime('%H:%M')
        tz_abbr = get_timezone_abbr(date)
        repo_name = os.path.basename(entry['repo'])
        
        # Escape any commas in the message
        message = entry['message'].replace('"', '""')
        
        line = f'"{date_str}","{day_name}","{week_start}","{time_str}","{tz_abbr}",{entry["minutes"]},{entry["minutes"]/60:.2f},"{repo_name}","{entry["commit"][:7]}","{message}","{entry["author_name"]}"'
        output.append(line)
    
    return "\\n".join(output).replace('\\n', '\n')

def format_markdown(weeks):
    """Format timesheet as Markdown."""
    result = []
    
    result.append("# Git Activity Timesheet\\n")
    
    for week_start, days in sorted(weeks.items()):
        result.append(f"## Week of {week_start}\\n")
        
        # Create a table for the week
        result.append("| Day | Date | Time | TZ | Repository | Hours | Description |")
        result.append("|-----|------|------|-------|------------|-------|-------------|")
        
        week_total = 0
        
        # Sort days to ensure Monday-Sunday order
        sorted_days = sorted(days.items())
        
        for day, entries in sorted_days:
            day_date = datetime.strptime(day, '%Y-%m-%d')
            day_name = day_date.strftime('%A')
            day_total = sum(entry['minutes'] for entry in entries)
            week_total += day_total
            
            # Group by repository
            repos = defaultdict(list)
            for entry in entries:
                repos[entry['repo']].append(entry)
            
            # First row for the day includes the day name
            first_row = True
            
            for repo, repo_entries in sorted(repos.items()):
                repo_name = os.path.basename(repo)
                repo_total = sum(entry['minutes'] for entry in repo_entries)
                
                # Group entries by similar tasks
                tasks = defaultdict(list)
                for entry in repo_entries:
                    # Use first 30 chars of message as key
                    key = entry['message'][:30]
                    tasks[key].append(entry)
                
                for task_name, task_entries in tasks.items():
                    task_total = sum(entry['minutes'] for entry in task_entries)
                    task_desc = f"{task_name}... ({len(task_entries)} commits)"
                    
                    # Get the time of the first commit in this task group
                    first_commit = min(task_entries, key=lambda x: x['date'])
                    first_commit_time = first_commit['date'].strftime('%H:%M')
                    tz_abbr = get_timezone_abbr(first_commit['date'])
                    
                    if first_row:
                        result.append(f"| {day_name} | {day} | {first_commit_time} | {tz_abbr} | {repo_name} | {task_total/60:.2f} | {task_desc} |")
                        first_row = False
                    else:
                        result.append(f"|  | | {first_commit_time} | {tz_abbr} | {repo_name} | {task_total/60:.2f} | {task_desc} |")
            
            # Add day total
            result.append(f"| **Total** | | | | | **{day_total/60:.2f}** | |")
            result.append("| | | | | | | |")  # Empty row for readability
        
        # Add week total
        result.append(f"| **Week Total** | | | | | **{week_total/60:.2f}** | |")
        result.append("\\n")
    
    return "\\n".join(result).replace('\\n', '\n')
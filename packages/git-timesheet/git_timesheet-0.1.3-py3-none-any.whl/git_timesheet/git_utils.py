#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime
import re

def get_git_repos(base_dir):
    """Find git repositories in the specified directory."""
    repos = []
    
    # First check if the base_dir itself is a git repository
    if os.path.exists(os.path.join(base_dir, '.git')):
        repos.append(base_dir)
        return repos
    
    # If not, look for git repositories in subdirectories
    for item in os.listdir(base_dir):
        full_path = os.path.join(base_dir, item)
        if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, '.git')):
            repos.append(full_path)
    return repos

def get_git_log(repo_path, since=None, until=None, author=None):
    """Get git log for a repository with author date and commit message."""
    cmd = ['git', 'log', '--pretty=format:%ad|%an|%ae|%s|%h', '--date=iso']
    
    if since:
        cmd.append(f'--since={since}')
    if until:
        cmd.append(f'--until={until}')
    if author:
        cmd.append(f'--author={author}')
    
    try:
        result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip().split('\n') if result.stdout.strip() else []
        return []
    except Exception as e:
        print(f"Error getting git log for {repo_path}: {e}")
        return []

def estimate_time_spent(commits, repo_name, session_timeout_minutes=60):
    """Estimate time spent on commits based on commit messages and frequency."""
    if not commits:
        return []
    
    # Parse commit dates and messages
    parsed_commits = []
    for commit in commits:
        if not commit:
            continue
        parts = commit.split('|')
        if len(parts) >= 5:
            date_str, author_name, author_email, message, commit_hash = parts[0], parts[1], parts[2], parts[3], parts[4]
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S %z')
                parsed_commits.append((date, message, commit_hash, repo_name, author_name, author_email))
            except ValueError:
                continue
    
    # Sort commits by date
    parsed_commits.sort(key=lambda x: x[0])
    
    # Estimate time for each commit
    time_entries = []
    for i, (date, message, commit_hash, repo, author_name, author_email) in enumerate(parsed_commits):
        # Base time: 15 minutes per commit
        time_spent = 15
        
        # Adjust based on commit message
        if re.search(r'fix|bug|issue', message, re.I):
            time_spent += 15
        if re.search(r'feature|implement|add', message, re.I):
            time_spent += 30
        if re.search(r'refactor|clean|improve', message, re.I):
            time_spent += 15
        
        # Check time gap to next commit
        if i < len(parsed_commits) - 1:
            next_date = parsed_commits[i+1][0]
            time_gap = (next_date - date).total_seconds() / 60
            
            # If commits are close together (within the configured session timeout), they're likely part of the same work session
            if time_gap < session_timeout_minutes:
                time_spent = min(time_spent, time_gap)
        
        time_entries.append({
            'date': date,
            'repo': repo,
            'message': message,
            'commit': commit_hash,
            'minutes': time_spent,
            'author_name': author_name,
            'author_email': author_email
        })
    
    return time_entries
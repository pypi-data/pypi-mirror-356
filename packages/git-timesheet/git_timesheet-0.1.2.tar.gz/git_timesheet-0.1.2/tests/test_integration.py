#!/usr/bin/env python3
import sys
import os
import pytest
import subprocess
from datetime import datetime, timedelta

# Add parent directory to path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from git_timesheet.git_utils import get_git_repos, get_git_log, estimate_time_spent
from git_timesheet.formatters import format_timesheet

class TestIntegration:
    """Integration tests using real git repositories"""
    
    def test_repo_detection(self, temp_git_repo):
        """Test that the script can detect a git repository"""
        repos = get_git_repos(temp_git_repo)
        assert len(repos) == 1
        assert repos[0] == temp_git_repo
    
    def test_multiple_repos(self, temp_git_repos):
        """Test that the script can detect multiple git repositories"""
        base_dir, repo_dirs = temp_git_repos
        repos = get_git_repos(base_dir)
        assert len(repos) == 2
        assert set(repos) == set(repo_dirs)
    
    def test_git_log_retrieval(self, temp_git_repo):
        """Test retrieving git log from a repository"""
        # Make a new commit
        with open(os.path.join(temp_git_repo, 'test.txt'), 'a') as f:
            f.write('\nAdditional content')
        
        subprocess.run(['git', 'add', 'test.txt'], cwd=temp_git_repo, check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'Add more content'], cwd=temp_git_repo, check=True, capture_output=True)
        
        # Get git log
        log = get_git_log(temp_git_repo)
        
        # Should have two commits
        assert len(log) == 2
        assert 'Initial commit' in log[1]
        assert 'Add more content' in log[0]
    
    def test_end_to_end(self, temp_git_repo):
        """Test the entire workflow from git log to formatted output"""
        # Configure git to use a matching author name for the test
        subprocess.run(['git', 'config', 'user.name', 'Michael McGarrah'], cwd=temp_git_repo, check=True, capture_output=True)
        subprocess.run(['git', 'config', 'user.email', 'test@mcgarrah.com'], cwd=temp_git_repo, check=True, capture_output=True)
        
        # Make multiple commits with different types of messages
        file_path = os.path.join(temp_git_repo, 'test.txt')
        
        # Bug fix commit
        with open(file_path, 'a') as f:
            f.write('\nFix a bug')
        subprocess.run(['git', 'add', 'test.txt'], cwd=temp_git_repo, check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'Fix critical bug'], cwd=temp_git_repo, check=True, capture_output=True)
        
        # Feature commit
        with open(file_path, 'a') as f:
            f.write('\nAdd a feature')
        subprocess.run(['git', 'add', 'test.txt'], cwd=temp_git_repo, check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'Implement new feature'], cwd=temp_git_repo, check=True, capture_output=True)
        
        # Refactor commit
        with open(file_path, 'a') as f:
            f.write('\nRefactor code')
        subprocess.run(['git', 'add', 'test.txt'], cwd=temp_git_repo, check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'Refactor for better performance'], cwd=temp_git_repo, check=True, capture_output=True)
        
        # Get git log
        log = get_git_log(temp_git_repo)
        
        # Estimate time spent
        repo_name = os.path.basename(temp_git_repo)
        time_entries = estimate_time_spent(log, repo_name)
        
        # Format as text
        output = format_timesheet(time_entries, 'text', 'UTC')
        
        # Check output
        assert 'Fix critical bug' in output
        assert 'Implement new feature' in output
        assert 'Refactor for better performance' in output
        
        # Format as CSV
        csv_output = format_timesheet(time_entries, 'csv', 'UTC')
        assert 'Date,Day,Week,Start Time,Timezone' in csv_output
        assert 'Fix critical bug' in csv_output
        
        # Format as markdown
        md_output = format_timesheet(time_entries, 'markdown', 'UTC')
        assert '# Git Activity Timesheet' in md_output
        assert 'Fix critical bug' in md_output
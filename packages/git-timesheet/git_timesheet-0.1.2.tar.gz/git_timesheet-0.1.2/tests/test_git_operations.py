#!/usr/bin/env python3
import sys
import os
import pytest
from unittest.mock import patch, MagicMock
import subprocess
from datetime import datetime

# Add parent directory to path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from git_timesheet.git_utils import get_git_repos, get_git_log, estimate_time_spent

class TestGitOperations:
    """Test git repository operations"""
    
    def test_get_git_repos_current_dir(self):
        """Test finding git repository in current directory"""
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.listdir') as mock_listdir:
            
            # Mock the current directory as a git repo
            mock_exists.return_value = True
            mock_isdir.return_value = True
            mock_listdir.return_value = []
            
            repos = get_git_repos('/fake/path')
            
            # Should return the base directory itself
            assert len(repos) == 1
            assert repos[0] == '/fake/path'
    
    def test_get_git_repos_subdirs(self):
        """Test finding git repositories in subdirectories"""
        with patch('os.path.exists') as mock_exists, \
             patch('os.path.isdir') as mock_isdir, \
             patch('os.listdir') as mock_listdir:
            
            # Mock the current directory as NOT a git repo
            mock_exists.side_effect = lambda path: '.git' in path and 'repo1/.git' in path or 'repo2/.git' in path
            mock_isdir.return_value = True
            mock_listdir.return_value = ['repo1', 'repo2', 'not_a_repo']
            
            repos = get_git_repos('/fake/path')
            
            # Should find two repos in subdirectories
            assert len(repos) == 2
            assert '/fake/path/repo1' in repos
            assert '/fake/path/repo2' in repos
    
    def test_get_git_log(self):
        """Test getting git log"""
        with patch('subprocess.run') as mock_run:
            # Mock successful git log command
            mock_process = MagicMock()
            mock_process.returncode = 0
            mock_process.stdout = "2023-06-01 12:00:00 +0000|Author Name|author@example.com|Commit message|abc123\n" \
                                 "2023-06-02 13:00:00 +0000|Author Name|author@example.com|Another commit|def456"
            mock_run.return_value = mock_process
            
            log = get_git_log('/fake/repo', since='1 week ago', author='Author')
            
            # Should return two log entries
            assert len(log) == 2
            assert 'Commit message' in log[0]
            assert 'Another commit' in log[1]
            
            # Check that subprocess.run was called with correct arguments
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert 'git' in args[0]
            assert 'log' in args[0]
            assert '--since=1 week ago' in args[0]
            assert '--author=Author' in args[0]
    
    def test_estimate_time_spent(self):
        """Test time estimation logic"""
        # Create sample commit data
        commits = [
            "2023-06-01 12:00:00 +0000|Author Name|author@example.com|Fix bug in login|abc123",
            "2023-06-01 12:30:00 +0000|Author Name|author@example.com|Implement new feature|def456",
            "2023-06-01 14:00:00 +0000|Author Name|author@example.com|Refactor code|ghi789"
        ]
        
        time_entries = estimate_time_spent(commits, 'test-repo')
        
        # Should have three entries
        assert len(time_entries) == 3
        
        # Check time estimates based on commit messages
        assert time_entries[0]['minutes'] == 30  # Fix bug (15 base + 15 for bug fix)
        assert time_entries[1]['minutes'] == 45  # Implement feature (15 base + 30 for feature)
        assert time_entries[2]['minutes'] == 30  # Refactor (15 base + 15 for refactor)
        
        # Check other fields
        assert time_entries[0]['repo'] == 'test-repo'
        assert time_entries[0]['message'] == 'Fix bug in login'
        assert time_entries[0]['commit'] == 'abc123'
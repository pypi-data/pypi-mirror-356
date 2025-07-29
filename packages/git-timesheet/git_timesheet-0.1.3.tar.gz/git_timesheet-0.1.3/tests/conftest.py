#!/usr/bin/env python3
import pytest
import os
import sys
import tempfile
import shutil
import subprocess
from datetime import datetime, timedelta

# Add parent directory to path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def temp_git_repo():
    """Create a temporary git repository for testing"""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Initialize git repo
        subprocess.run(['git', 'init'], cwd=temp_dir, check=True, capture_output=True)
        
        # Configure git user for commits
        subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=temp_dir, check=True, capture_output=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=temp_dir, check=True, capture_output=True)
        
        # Create a test file
        with open(os.path.join(temp_dir, 'test.txt'), 'w') as f:
            f.write('Initial content')
        
        # Add and commit the file
        subprocess.run(['git', 'add', 'test.txt'], cwd=temp_dir, check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=temp_dir, check=True, capture_output=True)
        
        # Yield the directory path
        yield temp_dir
    
    finally:
        # Clean up
        shutil.rmtree(temp_dir)

@pytest.fixture
def temp_git_repos():
    """Create multiple temporary git repositories for testing"""
    # Create a temporary directory to hold repos
    base_dir = tempfile.mkdtemp()
    repo_dirs = []
    
    try:
        # Create two repositories
        for repo_name in ['repo1', 'repo2']:
            repo_path = os.path.join(base_dir, repo_name)
            os.makedirs(repo_path)
            
            # Initialize git repo
            subprocess.run(['git', 'init'], cwd=repo_path, check=True, capture_output=True)
            
            # Configure git user for commits
            subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=repo_path, check=True, capture_output=True)
            subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=repo_path, check=True, capture_output=True)
            
            # Create a test file
            with open(os.path.join(repo_path, 'test.txt'), 'w') as f:
                f.write(f'Initial content for {repo_name}')
            
            # Add and commit the file
            subprocess.run(['git', 'add', 'test.txt'], cwd=repo_path, check=True, capture_output=True)
            subprocess.run(['git', 'commit', '-m', f'Initial commit for {repo_name}'], cwd=repo_path, check=True, capture_output=True)
            
            repo_dirs.append(repo_path)
        
        # Yield the base directory and repo directories
        yield base_dir, repo_dirs
    
    finally:
        # Clean up
        shutil.rmtree(base_dir)
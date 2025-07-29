#!/usr/bin/env python3
import os
import configparser
from pathlib import Path

def get_config():
    """Load configuration from file and return merged config with defaults"""
    # Default config values
    defaults = {
        'author': 'mcgarrah',
        'timezone': 'UTC',
        'session_timeout': '60'
    }
    
    # Config file locations to check (in order of precedence)
    config_paths = [
        Path.cwd() / '.ggtsrc',                      # Current directory rc file
        Path.cwd() / 'ggts.ini',                     # Current directory ini file
        Path.home() / '.ggtsrc',                     # User's home directory rc file
        Path.home() / '.config' / 'ggts.ini',        # XDG config directory
        Path.home() / '.config' / 'git-timesheet' / 'config.ini',  # New XDG config directory
    ]
    
    # Create config parser with defaults
    config = configparser.ConfigParser()
    config.add_section('defaults')
    for key, value in defaults.items():
        config['defaults'][key] = str(value)
    
    # Try to read config from files
    found_configs = config.read([str(p) for p in config_paths if p.exists()])
    
    if found_configs:
        print(f"Loaded configuration from: {found_configs[0]}")
    
    return config['defaults']
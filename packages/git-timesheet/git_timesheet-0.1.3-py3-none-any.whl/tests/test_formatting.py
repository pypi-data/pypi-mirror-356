#!/usr/bin/env python3
import sys
import os
import pytest
from datetime import datetime
import pytz
from collections import defaultdict

# Add parent directory to path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from git_timesheet.formatters import format_text, format_csv, format_markdown, format_timesheet

class TestFormatting:
    """Test output formatting functions"""
    
    @pytest.fixture
    def sample_entries(self):
        """Create sample time entries for testing"""
        entries = [
            {
                'date': datetime(2023, 6, 1, 10, 0, 0, tzinfo=pytz.UTC),
                'repo': 'test-repo',
                'message': 'Fix login bug',
                'commit': 'abc1234',
                'minutes': 30,
                'author_name': 'Test Author',
                'author_email': 'test@example.com'
            },
            {
                'date': datetime(2023, 6, 1, 14, 0, 0, tzinfo=pytz.UTC),
                'repo': 'test-repo',
                'message': 'Add new feature',
                'commit': 'def5678',
                'minutes': 45,
                'author_name': 'Test Author',
                'author_email': 'test@example.com'
            },
            {
                'date': datetime(2023, 6, 2, 9, 0, 0, tzinfo=pytz.UTC),
                'repo': 'another-repo',
                'message': 'Update documentation',
                'commit': 'ghi9012',
                'minutes': 15,
                'author_name': 'Test Author',
                'author_email': 'test@example.com'
            }
        ]
        return entries
    
    def test_format_text(self, sample_entries):
        """Test text output format"""
        # Group entries by week and day
        weeks = defaultdict(lambda: defaultdict(list))
        for entry in sample_entries:
            date = entry['date']
            week_start = (date - pytz.timezone('UTC').localize(datetime(1970, 1, 1, 0, 0, 0)).resolution * date.weekday()).strftime('%Y-%m-%d')
            day = date.strftime('%Y-%m-%d')
            weeks[week_start][day].append(entry)
        
        output = format_text(weeks)
        
        # Check that output contains expected elements
        assert 'Week of' in output
        assert '2023-06-01' in output
        assert '2023-06-02' in output
        assert 'Fix login bug' in output
        assert 'Add new feature' in output
        assert 'Update documentation' in output
        assert 'test-repo' in output
        assert 'another-repo' in output
        assert 'Total:' in output
    
    def test_format_csv(self, sample_entries):
        """Test CSV output format"""
        # Group entries by week and day
        weeks = defaultdict(lambda: defaultdict(list))
        for entry in sample_entries:
            date = entry['date']
            week_start = (date - pytz.timezone('UTC').localize(datetime(1970, 1, 1, 0, 0, 0)).resolution * date.weekday()).strftime('%Y-%m-%d')
            day = date.strftime('%Y-%m-%d')
            weeks[week_start][day].append(entry)
        
        output = format_csv(weeks, sample_entries)
        
        # Check that output contains expected elements
        assert 'Date,Day,Week,Start Time,Timezone,Duration (min),Duration (hours)' in output
        assert '2023-06-01' in output
        assert '2023-06-02' in output
        assert 'Fix login bug' in output
        assert 'Add new feature' in output
        assert 'Update documentation' in output
        assert 'test-repo' in output
        assert 'another-repo' in output
        assert '30' in output  # Duration in minutes
        assert '0.50' in output  # Duration in hours
    
    def test_format_markdown(self, sample_entries):
        """Test markdown output format"""
        # Group entries by week and day
        weeks = defaultdict(lambda: defaultdict(list))
        for entry in sample_entries:
            date = entry['date']
            week_start = (date - pytz.timezone('UTC').localize(datetime(1970, 1, 1, 0, 0, 0)).resolution * date.weekday()).strftime('%Y-%m-%d')
            day = date.strftime('%Y-%m-%d')
            weeks[week_start][day].append(entry)
        
        output = format_markdown(weeks)
        
        # Check that output contains expected elements
        assert '# Git Activity Timesheet' in output
        assert '## Week of' in output
        assert '| Day | Date | Time | TZ | Repository | Hours | Description |' in output
        assert '2023-06-01' in output
        assert '2023-06-02' in output
        assert 'Fix login bug' in output
        assert 'Add new feature' in output
        assert 'Update documentation' in output
        assert 'test-repo' in output
        assert 'another-repo' in output
        assert '**Total**' in output
        assert '**Week Total**' in output
    
    def test_format_timesheet_filtering(self, sample_entries):
        """Test timesheet formatting with author filtering"""
        # Add an entry with a different author
        different_author = {
            'date': datetime(2023, 6, 3, 10, 0, 0, tzinfo=pytz.UTC),
            'repo': 'test-repo',
            'message': 'Should be filtered out',
            'commit': 'jkl3456',
            'minutes': 30,
            'author_name': 'Different Author',
            'author_email': 'different@example.com'
        }
        entries = sample_entries + [different_author]
        
        # Test with default mcgarrah filter (should return no entries)
        output = format_timesheet(entries, 'text', 'UTC')
        assert "No git activity found for the specified author" in output
        
        # Test with matching author filter
        for entry in entries:
            if 'mcgarrah' not in entry['author_name'].lower():
                entry['author_name'] = 'Michael McGarrah'  # Add matching name
        
        output = format_timesheet(entries, 'text', 'UTC')
        assert "No git activity found" not in output
        assert "Fix login bug" in output
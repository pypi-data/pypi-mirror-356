#!/usr/bin/env python3
import sys
import os
import pytest
from datetime import datetime
import pytz

# Add parent directory to path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from git_timesheet.timezone_utils import convert_to_timezone, get_timezone_abbr

class TestTimezoneHandling:
    """Test timezone conversion and abbreviation functions"""
    
    def test_convert_to_timezone_standard(self):
        """Test conversion to standard timezone formats"""
        # Create a UTC datetime
        dt_utc = datetime(2023, 6, 1, 12, 0, 0, tzinfo=pytz.UTC)
        
        # Test conversion to America/New_York
        dt_ny = convert_to_timezone(dt_utc, 'America/New_York')
        assert dt_ny.tzinfo is not None
        assert dt_ny.tzinfo.zone == 'America/New_York'
        
        # Time should be different (UTC-4 or UTC-5 depending on DST)
        assert dt_ny.hour != dt_utc.hour
    
    def test_convert_to_timezone_aliases(self):
        """Test conversion using timezone aliases"""
        dt_utc = datetime(2023, 6, 1, 12, 0, 0, tzinfo=pytz.UTC)
        
        # Test US/Eastern alias
        dt_eastern = convert_to_timezone(dt_utc, 'US/Eastern')
        assert dt_eastern.tzinfo is not None
        assert dt_eastern.tzinfo.zone == 'America/New_York'
        
        # Test short abbreviation
        dt_est = convert_to_timezone(dt_utc, 'EST')
        assert dt_est.tzinfo is not None
        assert dt_est.tzinfo.zone == 'America/New_York'
        
        # Test prefixed short abbreviation
        dt_us_est = convert_to_timezone(dt_utc, 'US/EST')
        assert dt_us_est.tzinfo is not None
        assert dt_us_est.tzinfo.zone == 'America/New_York'
    
    def test_convert_to_timezone_invalid(self):
        """Test handling of invalid timezone"""
        dt_utc = datetime(2023, 6, 1, 12, 0, 0, tzinfo=pytz.UTC)
        
        # Should fall back to UTC with warning
        dt_invalid = convert_to_timezone(dt_utc, 'InvalidTimezone')
        assert dt_invalid.tzinfo is not None
        assert dt_invalid.tzinfo.zone == 'UTC'
        assert dt_invalid == dt_utc
    
    def test_get_timezone_abbr(self):
        """Test getting timezone abbreviation"""
        # Summer time (DST)
        # dt_summer = datetime(2023, 6, 1, 12, 0, 0, tzinfo=pytz.timezone('America/New_York'))
        ny_tz = pytz.timezone('America/New_York')
        dt_summer = ny_tz.localize(datetime(2023, 6, 1, 12, 0, 0))
        assert get_timezone_abbr(dt_summer) == 'EDT'
        
        # Winter time (standard time)
        # dt_winter = datetime(2023, 1, 1, 12, 0, 0, tzinfo=pytz.timezone('America/New_York'))
        ny_tz = pytz.timezone('America/New_York')
        dt_winter = ny_tz.localize(datetime(2023, 1, 1, 12, 0, 0))
        assert get_timezone_abbr(dt_winter) == 'EST'
        
        # UTC
        dt_utc = datetime(2023, 6, 1, 12, 0, 0, tzinfo=pytz.UTC)
        assert get_timezone_abbr(dt_utc) == 'UTC'
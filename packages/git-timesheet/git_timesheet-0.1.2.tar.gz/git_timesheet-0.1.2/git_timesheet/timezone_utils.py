#!/usr/bin/env python3
import pytz
from datetime import datetime

def convert_to_timezone(date, timezone_str='UTC'):
    """Convert datetime to specified timezone."""
    if date.tzinfo is None:
        date = date.replace(tzinfo=pytz.UTC)
    
    # Handle common timezone aliases
    timezone_aliases = {
        # US timezone aliases
        'US/Eastern': 'America/New_York',
        'US/Central': 'America/Chicago',
        'US/Mountain': 'America/Denver',
        'US/Pacific': 'America/Los_Angeles',
        'US/Alaska': 'America/Anchorage',
        'US/Hawaii': 'Pacific/Honolulu',
        
        # Short timezone abbreviations
        'EST': 'America/New_York',
        'EDT': 'America/New_York',
        'CST': 'America/Chicago',
        'CDT': 'America/Chicago',
        'MST': 'America/Denver',
        'MDT': 'America/Denver',
        'PST': 'America/Los_Angeles',
        'PDT': 'America/Los_Angeles',
        
        # Prefixed short timezone abbreviations
        'US/EST': 'America/New_York',
        'US/EDT': 'America/New_York',
        'US/CST': 'America/Chicago',
        'US/CDT': 'America/Chicago',
        'US/MST': 'America/Denver',
        'US/MDT': 'America/Denver',
        'US/PST': 'America/Los_Angeles',
        'US/PDT': 'America/Los_Angeles'
    }
    
    # Use the alias if available
    tz_name = timezone_aliases.get(timezone_str, timezone_str)
    
    try:
        target_tz = pytz.timezone(tz_name)
    except pytz.exceptions.UnknownTimeZoneError:
        print(f"Warning: Unknown timezone '{timezone_str}'. Falling back to UTC.")
        target_tz = pytz.UTC
        
    return date.astimezone(target_tz)

def get_timezone_abbr(date):
    """Get timezone abbreviation (like EDT, EST, CST) from a datetime object."""
    return date.strftime('%Z')
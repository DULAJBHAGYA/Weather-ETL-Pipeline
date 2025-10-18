"""
Unit tests for the configuration module.
"""
import os
import tempfile
from src.config import Config

def test_config_defaults():
    """Test that config defaults are set correctly."""
    # Test default values
    assert Config.SCHEDULE_INTERVAL_HOURS == 1
    assert Config.MAX_RETRIES == 3
    assert Config.RETRY_DELAY_SECONDS == 5
    assert Config.MIN_TEMP_C == -100
    assert Config.MAX_TEMP_C == 100
    assert Config.OWM_API_TIMEOUT == 20
    assert Config.OWM_API_BASE_URL == "https://api.openweathermap.org/data/2.5/weather"

def test_database_url():
    """Test database URL generation."""
    # Test database URL
    expected_url = f"sqlite:///{Config.SQLITE_DB}"
    assert Config.get_database_url() == expected_url

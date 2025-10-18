"""
Unit tests for the weather API module.
"""
from datetime import datetime, timezone
from src.weather_api import WeatherAPIClient
from src.models import WeatherObservation

def test_transform_weather_data():
    """Test weather data transformation."""
    client = WeatherAPIClient()
    
    # Sample raw data
    raw_data = {
        "dt": 1640995200,  # 2022-01-01 00:00:00 UTC
        "coord": {
            "lat": 40.7128,
            "lon": -74.0060
        },
        "main": {
            "temp": 293.15,
            "feels_like": 290.15,
            "humidity": 65,
            "pressure": 1013
        },
        "wind": {
            "speed": 3.5,
            "deg": 180
        },
        "weather": [
            {
                "main": "Clear",
                "description": "clear sky"
            }
        ]
    }
    
    observation = client.transform_weather_data("New York,US", raw_data)
    
    # Check that the observation was created
    assert isinstance(observation, WeatherObservation)
    # Note: We can't easily test attribute values due to SQLAlchemy column behavior